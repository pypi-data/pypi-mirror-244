#!/usr/bin/env python3

import argparse
from copy import deepcopy
import datetime
import json
import subprocess as sp
import bilby

import click
import numpy as np
import pandas as pd
from pesummary.gw.file.read import read
from tqdm import tqdm

from .get_settings import *
from .auxiliary.make_report import make_report
from .auxiliary.run_analyzer import railing_check, highmass_check,NS_check



# This script will iterate through a repository and check for a preferred run,
# use that to determine the seglen, srate and amp-order for Production runs,
# and Check the ini files for those


def eta_from_q(q):
    """Compute the symmetric mass ratio from the mass ratio"""
    return q / (1.0 + q) ** 2


def mt_from_eta_mc(eta, mc):
    """Compute total mass from symmetric mass ratio and chirp mass"""
    return mc / eta ** (3.0 / 5)


def mc_from_eta_mt(eta, mt):
    """Compute chirp mass from symmetric mass ratio and total mass"""
    return mt * eta ** (3.0 / 5)

# Compute a power of two less than or equal to `n`
def findPreviousPowerOf2(n):

    # do till only one bit is left
    while (n & n - 1):
        n = n & n - 1       # unset rightmost bit

    # `n` is now a power of two (less than or equal to `n`)
    return n


def check_railing(samples, label, nbins, tolerance, checks, recommendations=None, minimum_distance=None):

    if label == "distance":
        rail_low, rail_high, recommendation, bounds = railing_check(
            samples, nbins, tolerance, label, input_min_edge=minimum_distance
        )
    else:
        rail_low, rail_high, recommendation, bounds = railing_check(
            samples, nbins, tolerance, label
        )
    if rail_low or rail_high:
        click.echo(
            f"Checking for railing in {label}: " + click.style("FAILED", fg="red")
        )
        click.secho(
            f"WARNING: Found railing in {label}, please examine the posterior visually!",
            fg="red",
        )
        checks[label] = False

        recommendations[label] = recommendation
    else:
        click.echo(
            f"Checking for railing in {label}: " + click.style("PASSED", fg="green")
        )
        checks[label] = True
        recommendations[label] = ""
    return bounds


def create_json_output(recommended_settings, output_name, args):
    """Write the results to a json file to allow for easy injections"""
    metadata = dict(date=str(datetime.datetime.now()), command_line_args=str(args))
    dc = deepcopy(recommended_settings)
    dc.update(metadata=metadata)

    with open(f"{args.output_dir}/{output_name}", "w") as json_file:
        json.dump(dc, json_file, indent=4)


def get_preferred_result(file_path):
    """
    Return a pesummary object for the repo
    """
    try:
        sumfile = read(file_path)
    except FileNotFoundError:
        print(f"Could not find the samples file, {file_path}!")
        raise
    return sumfile

def get_reference_time_and_frame(pesummary_object, label):

    # Get detectors
    idx_label = np.argwhere(np.array(pesummary_object.labels,dtype='str')==label)[0,0]
    detectors = pesummary_object.detectors[idx_label]

    # Get SNR medians
    samples_dict = pesummary_object.samples_dict[label]
    mf_snr_keys = [ f'{det}_matched_filter_snr' for det in detectors ]
    snr_medians  = [ np.median(np.array(samples_dict[key])) for key in mf_snr_keys ]

    # Sort detectors by SNR
    best_to_worst = np.argsort(snr_medians)[::-1]
    sorted_detectors = [detectors[idx] for idx in best_to_worst]

    # Get detector with max SNR: reference time will be set according to this
    reference_time = sorted_detectors[0]

    # Reference frame. Same procedure as in https://git.ligo.org/lscsoft/bilby_pipe/-/blob/master/bilby_pipe/gracedb.py#L264
    if len(sorted_detectors) > 1:
        reference_frame = "".join(sorted_detectors[:2])
    else:
        reference_frame = "sky"

    return reference_time, reference_frame


def main():
    parser = argparse.ArgumentParser(
        description="Set up / confirm config files for O4a",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "samples_file",
        metavar="samples_file",
        type=str,
        help="path to file with samples",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        help="The dataset inside the samples file that should be used",
    )
    parser.add_argument(
        "--output_dir", type=str, help="Directory where to place output", default="./"
    )
    parser.add_argument(
        "--HM",
        default=False,
        action="store_true",
        help="Do checks with higher modes enabled",
    )
    parser.add_argument(
        "--q-min",
        default=None,
        type=float,
        help="The lower bound of the q-prior to be used for production",
    )
    parser.add_argument(
        "--dL-max",
        default=None,
        type=float,
        help="The upper bound of the dL-prior to be used for production",
    )
    parser.add_argument(
        "--ell-max", help="The ell to use for HM Nyquist check for EOB", default=3
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        help="Tolerance used when checking for railing",
        default=2.0,
    )
    parser.add_argument(
        "--nbins",
        type=int,
        help="Number of bins used when checking for railing",
        default=50,
    )
    parser.add_argument(
        "--flow",
        type=float,
        help="The frequency used for lower bound of likelihood integral [Hz]",
        default=20.0,
    )
    parser.add_argument(
        "--f_ref", type=float, help="The reference frequency [Hz]", default=20.0
    )
    parser.add_argument(
        "--bounds_tol",
        type=float,
        help="Tolerance to use when suggesting bounds for prior",
        default=0.2,
    )
    parser.add_argument(
        "--json_file",
        type=str,
        help="If supplied write the recommended settings to this json file",
    )
    parser.add_argument(
        "--report_file", type=str, help="If supplied, create a report with plots"
    )
    parser.add_argument(
        "--override_safeties",
        action="store_true",
        help="Disregard all warnings and generate json file anyway. USE AT OWN RISK!",
    )
    parser.add_argument("--debug", action="store_true", help="For debugging")
    parser.add_argument(
        "--include_dL_recommendations",
        action="store_true",
        help="Including recommendations for distance in output",
    )
    parser.add_argument(
        "--override_fstart",
        type=float,
        help="Overrides the recommended f_start with the value provided by the user",
        default=-1,
    )
    parser.add_argument(
        "--detchar_seglen",
        type=float,
        help="Maximum segment length allowed by detchar analysis. If provided, seglen recommendations above this value will be ignored.",
        default=-1,
    )
    parser.add_argument(
        "--enforce_ellmax",
        action="store_true",
        help="Enforce that the input ell-max is employed, regardless of the mass of the system",
    )
    parser.add_argument("--legacy",action="store_true",help="If true, f_start takes into account EOB limitations. Note that for high total mass if the segment length is based on f_start, this may result in very long segments. **Use with caution**")
    args = parser.parse_args()

    pesum = get_preferred_result(args.samples_file)

    try:
        samples = pesum.samples_dict[args.dataset]
    except KeyError:
        k = list(pesum.samples_dict.keys())[-1]
        click.secho(
            f"Pesum object in {args.samples_file} did not contain {args.dataset}, exiting!",
            fg="red",
        )
        exit(1)
    
    try:
        click.echo(f"Reading prior for {args.dataset} analysis.")
        analytic_prior = pesum.priors["analytic"][args.dataset]
    except KeyError:
        click.secho(
            f"Pesum object in {args.samples_file} did not contain prior dict for {args.dataset}, exiting!",
            fg="red",
        )
        exit(1)

    try:
        input_prior = bilby.gw.prior.PriorDict(analytic_prior)
        input_prior_dl_minimum = input_prior["luminosity_distance"].minimum
        input_prior_dl_maximum = input_prior["luminosity_distance"].maximum
        input_prior_q_minimum = input_prior["mass_ratio"].minimum
    except:
        input_prior_dl_minimum = float(str(analytic_prior["luminosity_distance"]).split("minimum=")[1].split(",")[0])
        input_prior_dl_maximum = float(str(analytic_prior["luminosity_distance"]).split("maximum=")[1].split(",")[0])
        input_prior_q_minimum = float(str(analytic_prior["mass_ratio"]).split("minimum=")[1].split(",")[0])
    

    mtot = np.array(samples["total_mass"])
    q = np.array(samples["mass_ratio"])
    chi1z = np.array(samples["spin_1z"])
    chi2z = np.array(samples["spin_2z"])
    dist = np.array(samples["luminosity_distance"])
    chirp_mass = np.array(samples["chirp_mass"])

    # Check if we are likely dealing with BNS
    # If so set ell_max=2
    _,is_BNS = NS_check(samples,alert=True)
    if is_BNS and not args.enforce_ellmax:
        click.echo("Event consistent with BNS! Using (ell,m)=(2,2) for all calculations")
        args.ell_max = 2

    dc = {
        "total mass": mtot,
        "q": q,
        "Mc": chirp_mass,
        "chi1z": chi1z,
        "chi2z": chi2z,
        "dL": dist,
    }
    df = pd.DataFrame(dc)

    # Round to multiples of 5
    mtot_max = 5 * (float(mtot.max()) // 5 + 1)
    mtot_min = 5 * (float(mtot.min()) // 5)

    # Round up to nearest Gpc
    dist_max = 1000 * (dist.max() // 1000 + 1)

    # Check if we are likely dealing with a high mass system
    # If so set ell_max=4
    _,is_highmass = highmass_check(samples,alert=True,enforce_ellmax=args.enforce_ellmax)
    if is_highmass and not args.enforce_ellmax:
        click.echo("Event consistent with total mass greater than 200! Using (ell,m)=(4,4) for all calculations")
        args.ell_max = 4

    # Proposed chirp mass bounds

    chirpmass_min = np.percentile(chirp_mass, 0.1)
    chirpmass_max = np.percentile(chirp_mass, 99.9)
    chirpmass_width = chirpmass_max - chirpmass_min

    if chirpmass_width > 30.0:
        chirpmass_min_bound = (1 - args.bounds_tol) * chirpmass_min
        chirpmass_max_bound = (1 + args.bounds_tol) * chirpmass_max
    else:
        chirpmass_min_bound = chirpmass_min - args.bounds_tol * chirpmass_width
        chirpmass_max_bound = chirpmass_max + args.bounds_tol * chirpmass_width

    # If chirp mass is railing, update the bounds with recommendation
    checks = {}
    recs = {}
    mchirp_railing_high = False
    new_mchirp_bounds = check_railing(
        chirp_mass,
        "chirp_mass",
        args.nbins,
        args.tolerance,
        checks,
        recommendations=recs,
    )
    if new_mchirp_bounds[0] is not None:
        click.echo(f"Estimating chirp mass lower bound to be {new_mchirp_bounds[0]}$M_{{\odot}}$. Please inspect visually if the recommendation is sensible.")
        chirpmass_min_bound = new_mchirp_bounds[0]
    if new_mchirp_bounds[1] is not None:
        click.echo(f"Estimating chirp mass upper bound to be {new_mchirp_bounds[1]}$M_{{\odot}}$. Please inspect visually if the recommendation is sensible.")
        chirpmass_max_bound = new_mchirp_bounds[1]
        mchirp_railing_high = True


    # Check if mass-ratio is railing
    bounds_massratio = check_railing(
        q, "mass_ratio", args.nbins, args.tolerance, checks, recommendations=recs
    )

    massratio_railing = False
    q_min = float(q.min())
    if bounds_massratio[0] is not None:
        massratio_railing = True
        if q_min > bounds_massratio[0]:
            q_min = bounds_massratio[0]
    #if args.q_min is not None:
    #    if args.q_min > q_min:
    #        q_min = args.q_min

    eta_min = q_min / (1 + q_min) ** 2

    click.echo("Processing....")

    # f_start section
    # The f_start based on preliminary samples
    click.echo("Estimating f_start based on posterior samples")
    seobp_amporder, f_start, hm_dominated = get_amp_order(
        mtot_max, f_low=args.flow, HM=args.HM,m_HM=args.ell_max,
        legacy=args.legacy
    )
    click.echo(f"f_start estimated is {f_start}")

    click.echo("Checking this f_start works with the proposed upper chirp mass bound")
    # The f_start taking into account the proposed change to chirp mass bounds
    # The change can only happen if the total mass is so high that EOB can
    # no longer generate a waveform. If that's the case, we adjust the starting
    # frequency accordingly
    # Use the heaviest samples parameters
    idx = np.argmax(mtot)
    q_max = q[idx]
    eta_max = eta_from_q(q_max)
    mtot_max_adj = mt_from_eta_mc(eta_max, chirpmass_max_bound)
    seobp_amporder_adj, f_start_adj, hm_dominated_adj = get_amp_order(
        mtot_max_adj, f_low=args.flow, HM=args.HM,m_HM=args.ell_max,
        legacy=args.legacy
    )
    if f_start_adj < f_start:
        f_start = f_start_adj
        seobp_amporder = seobp_amporder_adj
        click.echo(
            "The start frequency had to be adjusted to accommodate the changed chirp mass"
        )
    else:
        click.echo("No adjustment necessary!")



    click.echo("Estimating seglen based on posterior samples")

    # seglen section
    # Compute the seglen from the actual samples
    safelens, fulllens, seglens = zip(
        *[
            estimate_seglen(f_start, mt, q=1.0 / qp, chi1z=s1z, chi2z=s2z)
            for mt, qp, s1z, s2z in tqdm(list(zip(mtot, q, chi1z, chi2z)))
        ]
    )
    nopad_len = np.max(safelens)
    max_seglen = np.max(seglens)

    # Compute a conservative estimate for seglen
    # This is constructed as follows:
    # 1. We find the sample that gives the longest waveform
    # 2. Compute the total mass from this sample's q and proposed lower chirp mass bound
    # 3. Use this total mass and the other params from step 2. to compute the seglen
    # This procedure should overestimate the seglen and therefore be relatively safe.
    idx_max = np.argmax(fulllens)
    q_max = q[idx_max]
    eta_max = eta_from_q(q_max)
    # Given the lower bound of recommended chirp mass compute the corresponding total mass
    mt_lower_bound = mt_from_eta_mc(eta_max, chirpmass_min_bound)
    nopad, full, pof2 = estimate_seglen(
        f_start,
        mt_lower_bound,
        q=1 / q_max,
        chi1z=chi1z[idx_max],
        chi2z=chi2z[idx_max],
    )
    # Store the actual value we computed for logging
    pof2_log = pof2

    detchar_checks = {}  # Store useful input for make_report
    detchar_checks["consistent_seglen"] = True

    flow_aux = args.flow # Store flow to not overwrite args if needed later

    if args.detchar_seglen > 0:
        # Check if detchar recommendation is a power of two, and if not compute previous power of two
        detchar_seglen_pof2 = findPreviousPowerOf2(int(np.floor(args.detchar_seglen)))

        # Check if estimated seglen is greater than detchar recommendation
        if pof2 > detchar_seglen_pof2:
            click.echo(
                f"Estimated seglen of {pof2}s is greater than detchar recommendation of {detchar_seglen_pof2}s."
            )
            click.secho(
                f"Overriding segment length to {detchar_seglen_pof2}s.", fg="red"
            )
            pof2 = detchar_seglen_pof2  # Override with detchar recommendation
            detchar_checks["consistent_seglen"] = False

            # Input minimum might be incompatible with new recommended segment length
            # Find if this is the case and report a new recommended minimum frequency
            _, _, aux_pof2 = estimate_seglen(
                f_start,
                mt_lower_bound,
                q=1 / q_max,
                chi1z=0.99,
                chi2z=0.99,
            )
            while aux_pof2 > pof2:
                f_start = (
                    f_start + 0.05
                )  # We increment total mass until we find an allowed value
                _, _, aux_pof2 = estimate_seglen(
                    f_start,
                    mt_lower_bound,
                    q=1 / q_max,
                    chi1z=0.99,
                    chi2z=0.99,
                )

            # Overwrite f_start for this special case.
            if flow_aux < f_start:
                flow_aux = f_start
                click.secho(
                    f"Overriding minimum frequency flow to {flow_aux}Hz to satisfy duration restriction.", fg="red"
                )


    # seglen section ends

    # srate section
    # Compute sampling rate from the samples
    click.echo("Estimating srate based on posterior samples")
    click.secho(f"Using ell = {args.ell_max} for Nyquist check", bold=True)
    real_srates, srates = zip(
        *[
            min_sampling_rate_EOB(
                mt, q=1.0 / qp, HM=args.HM, chi1z=s1z, chi2z=s2z, ell_max=args.ell_max
            )
            for mt, qp, s1z, s2z in tqdm(list(zip(mtot, q, chi1z, chi2z)))
        ]
    )
    max_srate = np.max(srates)
    max_real_rate = np.max(real_srates)

    click.echo("Checking this srate works with the proposed lower chirp mass bound")
    # We do the following:
    # 1.  Find the sample that gives the highest srate
    # 2. Use that samples's q to and lower chirp mass bound to compute a new total mass
    # 3. Use this total mass and other params from the sample to recompue the srate
    mx_config = np.argmax(real_srates)
    q_max = q[mx_config]
    eta_max = eta_from_q(q_max)
    mtot_est = mt_from_eta_mc(eta_max, chirpmass_min_bound)

    real_srate_adj, srate_adj = min_sampling_rate_EOB(
        mtot_est,
        q=1.0 / q[mx_config],
        HM=args.HM,
        chi1z=chi1z[mx_config],
        chi2z=chi2z[mx_config],
        ell_max=args.ell_max,
    )

    if srate_adj > max_srate:
        click.secho(
            "Adjusting the sampling rate to take into account proposed chirp mass bounds"
        )
        max_srate = srate_adj
        max_real_rate = real_srate_adj
    else:
        click.secho("No adjustment necessary!")

    # Cap the sampling rate at 16kHz, since that is the highest sampling rate the actual
    # data can have
    if max_srate > 16384:
        click.echo(f"WARNING: the recommended sampling rate was {max_srate} > 16kHz. Setting the sampling rate to 16kHz ")
        max_srate = 16384.0

    # srate section ends



    click.echo("Done processing")
    click.echo()
    click.echo("#" * 30 + " SUMMARY " + 30 * "#")
    click.echo("Posterior parameters")
    click.echo("--" * 20)
    print(df.describe())
    click.echo("--" * 20)
    click.echo("Sanity checks")

    checks_passed = True

    # Railing checks
    bounds_distance = check_railing(
        dist, "distance", args.nbins, args.tolerance, checks, recommendations=recs, minimum_distance=input_prior_dl_minimum
    )
    # End railing checks

    # MECO check section
    new_checks = checks.copy()
    f_ref = args.f_ref
    f_ref_buffer = 0.97

    f_MECOs = np.array(
        [
            MECO_freq(mt, 1 / qp, s1z, s2z)
            for mt, qp, s1z, s2z in list(zip(mtot, q, chi1z, chi2z))
        ]
    )

    f_MECO_min = np.min(f_MECOs)
    if f_ref >= 0.97 * f_MECO_min:
        click.echo(
            "Checking that f_ref is not above f_MECO: "
            + click.style("FAILED", fg="red")
        )
        checks["f_ref"] = False
        f_ref = np.floor(f_ref_buffer * f_MECO_min)
        new_checks["f_ref"] = True
        click.secho(
            f"WARNING: the reference frequency is too close to the MECO frequency, f_MECO = {f_MECO_min}, overwritting reference frequency to f_ref={f_ref}",
            fg="red",
        )

    else:
        click.echo(
            "Checking that f_ref is not above f_MECO: "
            + click.style("PASSED", fg="green")
        )
        checks["f_ref"] = True
        new_checks["f_ref"] = True

    # Do we pass the MECO check with the expanded chirp mass? Yes, if there is railing in the upper bound of the chirp mass posterior
    if mchirp_railing_high:
        idx_min = np.argmin(f_MECOs)
        q_min = q[idx_min]
        eta_min = eta_from_q(q_min)
        mtot_min_adj = mt_from_eta_mc(eta_min, chirpmass_max_bound)
        f_meco = MECO_freq(mtot_min_adj, 1 / q_min, chi1z[idx_min], chi2z[idx_min])
        click.echo(
            "Checking that f_ref is not above f_MECO for the recommended chirp mass prior range."
        )
        if f_ref >= f_ref_buffer * f_meco:
            checks["f_ref"] = False
            f_ref = np.floor(f_ref_buffer * f_meco)
            new_checks["f_ref"] = True
            click.secho(
                f"The reference frequency is too close to the new MECO frequency, {f_meco} Hz, overwritting reference frequency to f_ref={f_ref}",
                fg="red",
            )

    # Try to override f_start is requested by the user
    # Process will fail if the MECO test is not satisfied for the new f_start
    if args.override_fstart > 0:
        if args.override_fstart <= f_ref:
            f_start = args.override_fstart
            click.secho(
                f"WARNING: Overriding f_start to the request value of {f_start}Hz. Notice that some power may be lost in the higher harmonics!",
                fg="red",
            )
        else:
            raise ValueError(
                f"Requested f_start of {args.override_fstart}Hz is greater than 0.97*f_MECO={f_ref_buffer*f_meco} Hz. This can produce pathological waveform generation. Please consider to request a lower value."
            )

    # We need to check if f_ref and f_start are consistent
    # If f_start was updated due to a detchar_seglen recommendation,
    # f_ref must be overwritten to match f_start
    # Otherwise, f_start should be updated to match f_ref, provided the
    # resulting seglen is not an issue
    if f_ref < f_start:
        if not detchar_checks.get('consistent_seglen',True):
            # f_start was forced by segment length recommendation
            click.secho(
                f"The reference frequency ({f_ref} Hz) is lower than the starting waveform generation frequency, {f_start} Hz, overwritting reference frequency to f_start.",
                fg="red",
            )

            f_ref = f_start
            checks["f_ref"] = False
            new_checks["f_ref"] = True
        else:
            # f_start wasn't forced
            # Recompute the segment length from f_ref

            nopad_aux, full_aux, aux_pof2 = estimate_seglen(
                f_ref,
                mt_lower_bound,
                q=1 / q_max,
                chi1z=0.99,
                chi2z=0.99,
            )
            # Check if the new segment length is longer than the detchar seglen
            # If it is, that means we can't start at f_low, overwrite f_ref
            # to f_start
            if args.detchar_seglen > 0 and aux_pof2 > args.detchar_seglen:
                click.secho(
                    f"The reference frequency ({f_ref} Hz) is lower than the starting waveform generation frequency, {f_start} Hz, and the segment length from f_ref > detchar segment length. Overwriting f_ref to f_start",
                    fg="red",
                )

                f_ref = f_start
                checks["f_ref"] = False
                new_checks["f_ref"] = True
            else:
                # No detchar seglen recommendation OR the resulting segment length is less than detchar recommendation
                # so we can set f_start = f_ref and use new segment legnth
                click.secho(f"The starting frequency ({f_start} Hz) is higher than the reference frequency ({f_ref} Hz), overwriting f_start to match f_ref")
                # Overwrite f_start
                f_start = f_ref

                # Overwrite everything to do with seglen
                pof2 = aux_pof2
                pof2_log = aux_pof2
                nopad = nopad_aux
                full = full_aux

    # MECO check section ends

    # Write the suggested settings to the log
    click.echo()
    click.echo(30 * "+" + " Suggested settings " + 30 * "+")
    # Sampling rate
    click.echo(f"Real required srate  {max_real_rate}, as power of 2: {max_srate}")

    # Segment length
    seglen_msg = f"Real seglen: {nopad}, with padding+rollon: {full}, as power of 2: {pof2_log}"
    # Take into account detchar recommendation
    if pof2_log > pof2:
        seglen_msg += f" overwritten by detchar recommendation to {pof2}"

    click.echo(seglen_msg)
    click.echo("Check from samples:")
    click.echo(
        f"Real seglen: {nopad_len}, with padding+rollon: {np.max(fulllens)}, as power of 2: {max_seglen}"
    )

    # Starting frequency
    click.echo(f"f_start: {f_start}")
    # Chirp mass bounds
    click.echo(
        f"Real bounds on chirp mass: [{chirpmass_min},{chirpmass_max}], suggested bounds: [{chirpmass_min_bound},{chirpmass_max_bound}]"
    )
    click.echo(f"Real distance max: {dist_max}")

    # Reference frames
    time_reference, reference_frame = get_reference_time_and_frame(pesum,args.dataset)
    click.echo(f"Recommended time reference: {time_reference}")
    click.echo(f"Recommended reference frame: {reference_frame}")

    recommended_settings = dict(
        srate=int(max_srate),
        f_start=round(f_start,2),
        f_ref=round(f_ref,2),
        seglen=pof2,
        chirpmass_min=chirpmass_min_bound,
        chirpmass_max=chirpmass_max_bound,
        meco_status=str(checks["f_ref"]),
        time_reference=time_reference,
        reference_frame=reference_frame
    )
    if args.debug:
        recommended_settings.update(
            seglen_conservative=full,
            seglen_liberal=np.max(fulllens),
            real_srate=max_real_rate,
            srate_adjusted=srate_adj,
            real_srate_adj=real_srate_adj,
            start_frequency_adj=f_start_adj,
            f_MECO=f_MECO_min,
            f_MECO_adj=f_meco,
        )
    if args.include_dL_recommendations:
        if bounds_distance[0] is not None:
            recommended_settings.update(dL_min=bounds_distance[0])
        else:
            recommended_settings.update(dL_min=input_prior_dl_minimum)

        if bounds_distance[1] is not None:
            recommended_settings.update(dL_max=bounds_distance[1])
        else:
            recommended_settings.update(dL_max=input_prior_dl_maximum)

    # Include mass-ratio recommendations
    # We always provide a q-min recommendation, to later update the priors if needed
    if massratio_railing:
        recommended_settings.update(q_min=bounds_massratio[0])
    else:
        recommended_settings.update(q_min=input_prior_q_minimum)

    if flow_aux > args.flow: #This only happens if flow has been recomputed
        recommended_settings.update(f_low=round(flow_aux,2))

    # np.savetxt("liberal_seglens.dat",fulllens)
    # Did all the checks pass?
    checks_passed = all(new_checks.values())
    click.echo(80 * "+")
    click.echo()

    click.echo("Creating machine-readable json file")
    if args.override_safeties:
        click.secho("Overriding safeties as requested!", fg="yellow")
    # If requested, make the json file with output
    if args.json_file is not None and (checks_passed or args.override_safeties):
        create_json_output(recommended_settings, args.json_file, args)

    click.echo("Creating a more detailed report with plots")

    # If requested, make a detailed report with plots
    if args.report_file is not None:
        make_report(
            args.samples_file,
            recommended_settings,
            args,
            f_ref,
            checks=checks,
            recommendations=recs,
            analysis=args.dataset,
            filename=args.report_file,
            outdir=args.output_dir,
            detchar_checks=detchar_checks,
        )
        sp.call(
            f"jupyter nbconvert --output-dir={args.output_dir} --no-input --to html  --execute --ExecutePreprocessor.timeout=900 {args.output_dir}/{args.report_file}",
            shell=True,
        )


if __name__ == "__main__":
    main()
