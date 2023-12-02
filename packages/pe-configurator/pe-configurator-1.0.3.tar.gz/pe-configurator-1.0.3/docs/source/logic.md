# PEconfigurator settings
[[_TOC_]]

## Introduction
This document outlines the logic behind the `peconfigurator` recommendations, and presents choices that must be addressed.

Recall that `peconfigurator` takes as input the following:

- A set of PE samples in a format readable by `pesummary`. Normally would be online PE

- `flow` - the minimum frequency for likelihood integration

- `f_ref` - the reference frequency (at which e.g. spins are defined)

- `ell_max` - the maximum $\ell$ to use when computing the required sampling rate

It provides the recommendations for the following:

- Updated prior bounds (for chirp mass, mass ratio and luminosity distance)

- Segment length to be analysed

- Sampling rate to use

- Updated reference frequency to use

- Updated lower bound for likelihood integral

- Starting frequency for template generation

Note that once the recommendations are generated, their use in Asimov is guided by additional logic, e.g. to take into account additional information coming from detchar, etc.

The following sections describe in detail how the various recommendations are created. We first describe the logic when no additional constaints are imposed and then describe what happens when things like DetChar recommendations force certain parameter values.

## Prior bounds changes

The configurator examines the following quantities for railing and creates suggestions if railing is detected:

- Chirp mass (lower+upper)

- Mass ratio (lower only)

- distance (upper only)

If railing in the quantity of interest $`x`$ is detected, an ad-hoc procedure is used to define the new bounds. It is motivated by very naive assumptions, since in general the exact shape of railing is difficult to predict apriori.   In particular:

1. $`x`$ is binned using `np.histogram` and the prescribed number of bins (default is 50) and `density=True` so the resulting values represent density.

2. The "relative" support for edge bins is computed as $`q_{l}=100 p_{0}/p_{\rm max}`$ and $`q_{h}=100 p_{N}/p_{\rm max}`$. Where $`p_{\rm max}=\max p_{i}`$ in all the bins.

3. Define $`x_l=\min(x)`$, $`x_{h}=\max(x)`$.

4. If the railing is at lower edge then the new bound is defined as

   ```math
   x_{l}^{*} = [1-f(q_{l})]x_l, {\rm with}\ f(q) = \frac{\alpha}{1+\exp(-c_{1}(q_{l}-s))}
   ```

   Here $\alpha$ and $c_{1}$ and $s$ are the parameters of the sigmoid $f(q)$, with default values 0.66, 0.03 and 30 respectively.

   If the railing is at the upper edge, then

  ```math
   x_{h}^{*} = [1+f(q_h)]x_{h}
  ```

The motivation for this procedure is simply that the sigmoid provides a useful "ramp-on" and "ramp-off" function suitable for changing the lower and upper bounds of the prior. The following shows a couple of artificial examples which nonetheless are qualitatively similar to the railing one encounters in chirp mass and mass ratio.

![fake_chirpmass_railing](uploads/d0f7db823f4a71a59aa4368414f55bb8/fake_chirpmass_railing.png)

![fake_mass_ratio_rail_low](uploads/a1ff3ea62ac310e1f39badabf443ae8e/fake_mass_ratio_rail_low.png)

### Chirp mass determination

If no railing is found, the proposed bounds are computed depending on the width of the chirp mass posterior $`\Delta\mathcal{M}=\mathcal{M}_{\rm max}-\mathcal{M}_{\rm min}`$. If the width is greater than $`30M_{\odot}`$, then the proposed bounds are given by $`[(1-f)\mathcal{M}_{\rm min},(1+f)\mathcal{M}_{\rm max}]`$ where $`f`$ is a free parameter, given by the option `--bounds_tol` with the default value of **0.2**. If the width is smaller than $`30M_{\odot}`$, then the bound are given by $`[\mathcal{M}_{\rm min}-f\Delta\mathcal{M},\mathcal{M}_{\rm max}+f\Delta\mathcal{M}f]`$. This is done so that for posteriors where the chirp mass is well measured one does not create new prior bounds which are too broad (e.g. for BNS).  If railing is detected than the appropriate bounds in the above are overwritten by the railing suggestions.

### Mass ratio determination

Mass ratio priors are only changed if railing is detected. The suggestion made by the configurator is based on the same ad-hoc formula.

### Distance recommendation

Distance recommendation is provided both for upper and lower bound but in practice only the upper bound recommendation is used.  It is based on the same ad-hoc formula

## Settings

 Many of the settings depend on the masses of the binary and are thus affected by proposed changes to the chirp mass prior described above.  For every setting, we generate 2 estimates: one coming directly from the samples and a conservative one, which takes into account the wider chirp mass prior. In particular,  the following strategy is adopted:

1. Estimate the quantity of interest from the samples.
2. Pick the most extreme value of the quantity of interest (e.g. max seglen or min $f_{\rm start}$) and find its parameters (mass ratio and spins)
3. Use either the lower or upper proposed chirp mass bounds (as appropriate) and the mass ratio from step 2 to estimate a new total mass
4. Use this total mass along with the other params (as appropriate) to produce a new estimate of the quantity of interest

### Reference frequency

`peconfigurator` computes the MECO frequency from all the samples and checks that the _input_ `f_ref` is less than $0.97$ times the lowest MECO frequency. If this is not the case, then `f_ref` is adjusted to be that value. There is an additional check that the MECO test passes with the expanded chirp mass prior for cases where there was railing against the upper bound of the chirp mass. If the MECO test fails, the value `f_ref` is adjusted again.

### Sampling rate

The sampling rate is determined by the requirement that it's high enough to resolve the highest frequency we are interested in. This is generally given by the frequency of the highest $`(\ell,m)`$ mode in the ringdown. This is estimated by using the QNM frequencies computed in `SEOBNRv4HM` routines.  The user is given control which $`\ell`$ is used for this Nyquist frequency check via the option `--ell-max`. By default it is set to **3**.  To be precise, the sampling rate is computed as $`2f_{\rm max}`$ and then rounded up to the next power of 2.

### Starting frequency

The starting frequency (which corresponds to the frequency of the (2,2) mode) has to be such that the desired $`(\ell,m)`$ mode is present at the provided `flow`. The script uses the PN relation (valid in the inspiral) that $`f_{\ell m}=\frac{m}{2}f_{22}`$ to determine this. Note that by construction, for any $`m>2`$, the starting frequency will be less than `flow`. In case the reference frequency did not pass the MECO test, and it is lower than the starting frequency, the starting frequency will be overiden to the reference frequency.

### The segment length

The raw segment length is determined by the following formula
$`t = T(1+s)+t_{\rm pad}+t_{\rm rollon}`$, where $`T`$ is an estimate of the duration of the waveform, including inspiral, merger and ringdown; $`s`$ is a safety factor (default value of 0.03), $`t_{\rm pad}`$ is padding (default is 2 seconds) and $`t_{\rm rollon}`$ is the Tukey window roll on duration (default is 0.4 seconds).  The duration $`T`$ is taken to be a function of the 2 component masses $`m_{i}`$, the z-components of the dimensionless spin $`\chi_{i}`$. It also requires a choice of the frequency from which to compute the duration. The choice in O3 (currently the default) is to use `flow`. This implies that the analysis segment is only guaranteed to contain the $\ell=2$ modes.  Finally the seglen is rounded to the next power of 2.

## Additional logic in the Asimov part
There is additional logic that is applied in the `asimov` part.

### Prior changes

- For changes to the mass ratio lower bound, the prior choice already used by Asimov is only overwritten if:
  a. the recommendation by the configurator is _lower_ than this value
  b. or no default value exists
- For changes to the distance upper bound, the prior choice already used by Asimov is only overwritten if:
  a. the recommendation by the configurator is _larger_ than this value
  b. or no default value exists

# Important choices that have to be finalized

## Segment length

One key choice is which **frequency is used in the calculation of the segment length**. There are several considerations that come in. With the current setup, where `flow` is used, $`t_{\rm segment}<t_{\rm template}`$, which has the following implications:

- The _signal_ itself might be missing higher mode content at `flow`
- Since the duration of the segment determines the $\Delta f$ in FD:
  - `SimInspiralFD` will **truncate** the template to make it match the segment length, _after_ it has been conditioned which can result in additional noise of the FFT of the template (and wasting computing cycles)
  - Potentially the higher mode content might be under-resolved
- RIFT developers mentioned that they IFFT FD approximants which will wrap around since the higher modes are longer in TD when started from the same frequency

Choices:

1. Simply set `f_start=flow`. This will solve the `SimInspiralFD` issue and somewhat alleviate missing higher mode content issue for TD approximants. However, it would not solve the others.
2. Use `f_start` to determine the segment length. This would ensure that at least the mode that was used to pick `f_start` (e.g. $`\ell=3`$) would fit inside the segment. This would solve the `SimInspiralFD` issue for TD waveforms and partially alleviate the rest (indeed if one was to only include modes with $`\ell\leq3`$ this would be entirely consistent)
   The following plot shows the segment length that would result for different choices of frequency used in estimation for all events in GWTC2.1, assuming `flow=20`Hz, as computed by `peconfigurator`:


![seglens](uploads/e33ab421065cbbd90666f9c67ca46f72/seglens.png)

Essentially, resolving each successive $`m`$ mode doubles the length of the segment that needs to be analyzed. From the plot, it seems to be quite infeasible to analyze things while starting at 10 Hz, but starting at $`13.333`$ Hz might be quite doable.

## Starting frequency

A closely connected choice is which modes should be in band at `flow`. In O3, things were chosen so that the $`(3,3)`$ mode is in band. Is this choice still appropriate?

## Sampling rate

The sampling rate is determine by the highest $(\ell,m)$ mode we want to resolve. In O3 this was chosen to be the $`(3,3)`$ mode.  Is this choice still appropriate?

### Additional considerations
- If the component masses from the preliminary run are consistent with BNS, should `ell_max` be set to 2, since for BNS we don't have higher modes anyway?

## Proposal (to be signed off)
The following settings are proposed. The idea is that basically everything is as self-consistent as possible.

It is proposed that **the sampling rate** will be set using:
- `ell_max=3` by default
- `ell_max=2` for BNS
- `ell_max=4` for total mass > 200 MSun
- Be capped at 16384 Hz

It is proposed that **the starting frequency of the waveform generation** (`f_start`) will be set from `flow` using:
- `ell_max=3` by default
- `ell_max=2` for BNS
- `ell_max=4` for total mass > 200 MSun

It is proposed that **the segment duration** will be computed always from `f_start`, as defined above.


# Managing detchar recommendations (to be finalized)

Detchar can impose some restrictions on segment duration and minimum frequency (for each detector), based on data quality considerations, which implies additional checks in the configurator:

- If the maximum allowed duration is shorter than the recommended by the configurator, the input `flow` might be inconsistent with the new duration, i.e it might allow templates for which not even the (2,2) mode fits the segment length. In this case, a minimum allowed `flow` is computed such that the resulting (2,2)-mode template fit the segment length. The starting frequency `f_start` is also set to the new computed value.

- If there is an additional detchar recommendation on minimum frequency for each detector, Asimov should check if the new recommendation is less restrictive (lower frequency) than the configurator recommendation, for each detector, and in this case overwrite the value with the configurator recommendation, to satisfy the segment length requirements.
