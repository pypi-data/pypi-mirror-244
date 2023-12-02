import matplotlib
import matplotlib.pyplot as plt
import bilby
import numpy as np
from typing import Mapping, Optional
import warnings

# Hardcoded constraints for NRSur7Dq4
# See https://git.ligo.org/pe/O4/asimov-review/-/wikis/Asimov-v0.5.3#waveform-argument-links
NRSUR_CONSTRAINTS = dict(
    totalmass_min=60.0,
    totalmass_max=400.0,
    q_min=0.16666667,
    q_max=1.0,
)


def get_prior_bounds_from_chirp_mass(
    chirpmass_min: float,
    chirpmass_max: float,
    q_min: float,
    q_max: float = 1.0,
    n_points: int = 100,
) -> np.ndarray:
    """
    Get an array of component mass values that delineate the prior bounds
    given chirp mass and mass ratio ranges.

    Parameters
    ----------
    chirpmass_min
        Minimum total mass
    chirpmass_max
        Maximum total mass
    q_min
        Minimum mass ratio
    q_max
        Maximum mass ratio. Defaults to 1.
    n_points :
        The number of points in the lines for each of the sides of the prior.

    Returns
    -------
    numpy.ndarray
        An array of shape (2, 4*n_points) containing the component masses.
    """
    q_vec = np.linspace(q_min, q_max, n_points)
    chirpmass_vec = np.linspace(chirpmass_min, chirpmass_max, n_points)
    prior_bounds = np.concatenate(
        [
            bilby.gw.conversion.chirp_mass_and_mass_ratio_to_component_masses(
                chirpmass_max, q_vec
            ),
            bilby.gw.conversion.chirp_mass_and_mass_ratio_to_component_masses(
                chirpmass_vec[::-1], q_max
            ),
            bilby.gw.conversion.chirp_mass_and_mass_ratio_to_component_masses(
                chirpmass_min, q_vec[::-1]
            ),
            bilby.gw.conversion.chirp_mass_and_mass_ratio_to_component_masses(
                chirpmass_vec, q_min
            ),
        ],
        axis=1,
    )
    return prior_bounds


def get_prior_bounds_from_total_mass(
    totalmass_min: float,
    totalmass_max: float,
    q_min: float,
    q_max: float = 1.0,
    n_points: int = 100,
) -> np.ndarray:
    """
    Get an array of component mass values that delineate the prior bounds
    given total mass and mass ratio ranges.

    Parameters
    ----------
    totalmass_min
        Minimum total mass
    totalmass_max
        Maximum total mass
    q_min
        Minimum mass ratio
    q_max
        Maximum mass ratio. Defaults to 1.
    n_points
        The number of points in the lines for each of the sides of the prior.

    Returns
    -------
    numpy.ndarray
        An array of shape (2, 4*n_points) containing the component masses.
    """
    q_vec = np.linspace(q_min, q_max, n_points)
    totalmass_vec = np.linspace(totalmass_min, totalmass_max, n_points)
    prior_bounds = np.concatenate(
        [
            bilby.gw.conversion.total_mass_and_mass_ratio_to_component_masses(
                q_vec, totalmass_min
            ),
            bilby.gw.conversion.total_mass_and_mass_ratio_to_component_masses(
                q_max, totalmass_vec
            ),
            bilby.gw.conversion.total_mass_and_mass_ratio_to_component_masses(
                q_vec[::-1], totalmass_max
            ),
            bilby.gw.conversion.total_mass_and_mass_ratio_to_component_masses(
                q_min, totalmass_vec[::-1]
            ),
        ],
        axis=1,
    )
    return prior_bounds


def plot_nrsur_constraints(
    chirpmass_min: float,
    chirpmass_max: float,
    q_min: float,
    q_max: float = 1.0,
    n_points: int = 100,
    posterior_samples: Optional[Mapping[str, np.ndarray]] = None,
) -> matplotlib.figure.Figure:
    """
    Plot the prior bounds given the chirp mass and mass ratio ranges alongside
    the constraints for NRSur7Dq4.

    Parameters
    ----------
    chirpmass_min
        Minimum total mass
    chirpmass_max
        Maximum total mass
    q_min
        Minimum mass ratio
    q_max
        Maximum mass ratio. Defaults to 1.
    n_points
        The number of points in the lines for each of the sides of the prior.
    posterior_samples
        Posterior samples to include in the plot. Must include mass_1 and
        mass_2.

    Returns
    -------
    matplotlib.figure.Figure
        The figure showing the prior bounds and NRSur constraints.
    """

    m1_bounds, m2_bounds = get_prior_bounds_from_chirp_mass(
        chirpmass_min=chirpmass_min,
        chirpmass_max=chirpmass_max,
        q_min=q_min,
        q_max=q_max,
        n_points=n_points,
    )

    m1_totalmass_bounds, m2_totalmass_bounds = get_prior_bounds_from_total_mass(
        totalmass_min=NRSUR_CONSTRAINTS["totalmass_min"],
        totalmass_max=NRSUR_CONSTRAINTS["totalmass_max"],
        q_min=NRSUR_CONSTRAINTS["q_min"],
        q_max=NRSUR_CONSTRAINTS["q_max"],
        n_points=n_points,
    )

    fig, axs = plt.subplots()
    chirp_mass_q_kwargs = dict(
        c="C0",
        ls="-",
    )
    total_mass_kwargs = dict(
        c="C1",
        ls="--",
    )

    posterior_samples_kwargs = dict(
        s=1,
        c="gray",
    )

    axs.plot(
        m1_bounds,
        m2_bounds,
        label="Proposed prior\n bounds",
        **chirp_mass_q_kwargs
    )

    axs.plot(
        m1_totalmass_bounds,
        m2_totalmass_bounds,
        label="NRSur7Dq4\n constraints",
        **total_mass_kwargs
    )

    axs.set_xlabel(r"$m_1\;(M_{\odot})$")
    axs.set_ylabel(r"$m_2\;(M_{\odot})$")

    if posterior_samples is not None:
        axs.scatter(
            posterior_samples["mass_1"],
            posterior_samples["mass_2"],
            label="Posterior\n samples",
            **posterior_samples_kwargs
        )

    axs.legend()
    return fig
