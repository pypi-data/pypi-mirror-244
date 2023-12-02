import matplotlib.pyplot as plt
import numpy as np
from peconfigurator.auxiliary.plotting import (
    get_prior_bounds_from_chirp_mass,
    get_prior_bounds_from_total_mass,
    plot_nrsur_constraints,
)


def test_get_prior_bounds_chirp_mass():
    n_points = 10
    q_min = 0.1
    q_max = 1.0
    bounds = get_prior_bounds_from_chirp_mass(
        chirpmass_min=20.0,
        chirpmass_max=50.0,
        q_min=q_min,
        q_max=q_max,
        n_points=n_points,
    )
    assert bounds.shape == (2, 4 * n_points)
    # Assert m1 >= m2
    assert np.all(bounds[0] >= bounds[1])
    # Assert q_min is respected
    assert np.all((bounds[1]  / bounds[0]) >= q_min)


def test_get_prior_bounds_total_mass():
    n_points = 10
    q_min = 0.16666667
    q_max = 1.0
    bounds = get_prior_bounds_from_total_mass(
        totalmass_min=60.0,
        totalmass_max=400.0,
        q_min=q_min,
        q_max=q_max,
        n_points=n_points,
    )
    assert bounds.shape == (2, 4 * n_points)
    # Assert m1 >= m2
    assert np.all(bounds[0] >= bounds[1])
    # Assert q_min is respected
    assert np.all((bounds[1]  / bounds[0]) >= q_min)


def test_plot_nrsur_constraints():
    posterior_samples = {
        "mass_1": [10.0, 20.0],
        "mass_2": [8.0, 18.0],
    }
    fig = plot_nrsur_constraints(
        20.0,
        50.0,
        0.1,
        n_points=10,
        posterior_samples=posterior_samples,
    )
    assert fig is not None
    plt.close("all")
