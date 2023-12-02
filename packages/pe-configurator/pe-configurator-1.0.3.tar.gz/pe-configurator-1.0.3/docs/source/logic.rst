PEconfigurator settings
=======================



Introduction
------------

This document outlines the logic behind the ``peconfigurator``
recommendations, and presents choices that must be addressed.

Recall that ``peconfigurator`` takes as input the following:

-  A set of PE samples in a format readable by ``pesummary``. Normally
   would be online PE

-  ``flow`` - the minimum frequency for likelihood integration

-  ``f_ref`` - the reference frequency (at which e.g. spins are defined)

-  ``ell_max`` - the maximum :math:`\ell` to use when computing the
   required sampling rate

It provides the recommendations for the following:

-  Updated prior bounds (for chirp mass, mass ratio and luminosity
   distance)

-  Segment length to be analysed

-  Sampling rate to use

-  Updated reference frequency to use

-  Updated lower bound for likelihood integral

-  Starting frequency for template generation

Note that once the recommendations are generated, their use in Asimov is
guided by additional logic, e.g. to take into account additional
information coming from detchar, etc.

The following sections describe in detail how the various
recommendations are created. We first describe the logic when no
additional constraints are imposed and then describe what happens when
things like DetChar recommendations force certain parameter values.

Prior bounds changes
--------------------

The configurator examines the following quantities for railing and
creates suggestions if railing is detected:

-  Chirp mass (lower+upper)

-  Mass ratio (lower only)

-  distance (upper only)

If railing in the quantity of interest :math:`x` is detected, an
ad-hoc procedure is used to define the new bounds. It is motivated by
very naive assumptions, since in general the exact shape of railing is
difficult to predict apriori. In particular:

1. :math:`x` is binned using ``np.histogram`` and the prescribed
   number of bins (default is 50) and ``density=True`` so the resulting
   values represent density.

2. The “relative” support for edge bins is computed as
   :math:`q_{l}=100 p_{0}/p_{\rm max}` and
   :math:`q_{h}=100 p_{N}/p_{\rm max}`. Where
   :math:`p_{\rm max}=\max p_{i}` in all the bins.

3. Define :math:`x_l=\min(x)`, :math:`x_{h}=\max(x)`.

4. If the railing is at lower edge then the new bound is defined as

   .. math::

      x_{l}^{*} = [1-f(q_{l})]x_l, {\rm with}\ f(q) = \frac{\alpha}{1+\exp(-c_{1}(q_{l}-s))}

   Here :math:`\alpha` and :math:`c_{1}` and :math:`s` are the
   parameters of the sigmoid :math:`f(q)`, with default values 0.66,
   0.03 and 30 respectively.

   If the railing is at the upper edge, then

.. math::

    x_{h}^{*} = [1+f(q_h)]x_{h}

The motivation for this procedure is simply that the sigmoid provides a
useful “ramp-on” and “ramp-off” function suitable for changing the lower
and upper bounds of the prior. The following shows a couple of
artificial examples which nonetheless are qualitatively similar to the
railing one encounters in chirp mass and mass ratio.

.. figure:: images/fake_chirpmass_railing.png
   :alt: fake_chirpmass_railing

   fake_chirpmass_railing

.. figure:: images/fake_mass_ratio_rail_low.png
   :alt: fake_mass_ratio_rail_low

   fake_mass_ratio_rail_low

Chirp mass determination
~~~~~~~~~~~~~~~~~~~~~~~~

If no railing is found, the proposed bounds are computed depending on
the width of the chirp mass posterior
:math:`\Delta\mathcal{M}=\mathcal{M}_{\rm max}-\mathcal{M}_{\rm min}`.
If the width is greater than :math:`30M_{\odot}`, then the proposed
bounds are given by
:math:`[(1-f)\mathcal{M}_{\rm min},(1+f)\mathcal{M}_{\rm max}]` where
:math:`f` is a free parameter, given by the option ``--bounds_tol``
with the default value of **0.2**. If the width is smaller than
:math:`30M_{\odot}`, then the bound are given by
:math:`[\mathcal{M}_{\rm min}-f\Delta\mathcal{M},\mathcal{M}_{\rm max}+f\Delta\mathcal{M}f]`.
This is done so that for posteriors where the chirp mass is well
measured one does not create new prior bounds which are too broad
(e.g. for BNS). If railing is detected than the appropriate bounds in
the above are overwritten by the railing suggestions.

Mass ratio determination
~~~~~~~~~~~~~~~~~~~~~~~~

Mass ratio priors are only changed if railing is detected. The
suggestion made by the configurator is based on the same ad-hoc formula.

Distance recommendation
~~~~~~~~~~~~~~~~~~~~~~~

Distance recommendation is provided both for upper and lower bound but
in practice only the upper bound recommendation is used. It is based on
the same ad-hoc formula

Settings
--------

Many of the settings depend on the masses of the binary and are thus
affected by proposed changes to the chirp mass prior described above.
For every setting, we generate 2 estimates: one coming directly from the
samples and a conservative one, which takes into account the wider chirp
mass prior. In particular, the following strategy is adopted:

1. Estimate the quantity of interest from the samples.
2. Pick the most extreme value of the quantity of interest (e.g. max
   seglen or min :math:`f_{\rm start}`) and find its parameters (mass
   ratio and spins)
3. Use either the lower or upper proposed chirp mass bounds (as
   appropriate) and the mass ratio from step 2 to estimate a new total
   mass
4. Use this total mass along with the other params (as appropriate) to
   produce a new estimate of the quantity of interest

Reference frequency
~~~~~~~~~~~~~~~~~~~

``peconfigurator`` computes the MECO frequency from all the samples and
checks that the *input* ``f_ref`` is less than :math:`0.97` times the
lowest MECO frequency. If this is not the case, then ``f_ref`` is
adjusted to be that value. There is an additional check that the MECO
test passes with the expanded chirp mass prior for cases where there was
railing against the upper bound of the chirp mass. If the MECO test
fails, the value ``f_ref`` is adjusted again.

Sampling rate
~~~~~~~~~~~~~

The sampling rate is determined by the requirement that it’s high enough to
resolve the highest frequency we are interested in. This is generally given by
the frequency of the highest :math:`(\ell,m)` mode in the ringdown. This is
estimated by using the QNM frequencies computed in ``SEOBNRv4HM`` routines. The
user is given control which :math:`\ell` is used for this Nyquist frequency
check via the option ``--ell-max``. To be precise, the sampling rate is computed
as :math:`2f_{\rm max}` and then rounded up to the next power of 2.

Starting frequency
~~~~~~~~~~~~~~~~~~

The starting frequency (which corresponds to the frequency of the (2,2)
mode) has to be such that the desired :math:`(\ell,m)` mode is present
at the provided ``flow``. The script uses the PN relation (valid in the
inspiral) that :math:`f_{\ell m}=\frac{m}{2}f_{22}` to determine this.
Note that by construction, for any :math:`m>2`, the starting frequency
will be less than ``flow``. In case the reference frequency did not pass
the MECO test, and it is lower than the starting frequency, the starting
frequency will be overiden to the reference frequency.

The segment length
~~~~~~~~~~~~~~~~~~

The raw segment length is determined by the following formula
:math:`t = T(1+s)+t_{\rm pad}+t_{\rm rollon}`, where :math:`T` is an
estimate of the duration of the waveform, including inspiral, merger and
ringdown; :math:`s` is a safety factor (default value of 0.03),
:math:`t_{\rm pad}` is padding (default is 2 seconds) and
:math:`t_{\rm rollon}` is the Tukey window roll on duration (default
is 0.4 seconds). The duration :math:`T` is taken to be a function of
the 2 component masses :math:`m_{i}`, the z-components of the
dimensionless spin :math:`\chi_{i}`. It also requires a choice of the
frequency from which to compute the duration.

Additional logic in the Asimov part
-----------------------------------

There is additional logic that is applied in the ``asimov`` part.

Prior changes
~~~~~~~~~~~~~

-  For changes to the mass ratio lower bound, the prior choice already
   used by Asimov is only overwritten if:

   a. the recommendation by the configurator is *lower* than this value
   b. or no default value exists

-  For changes to the distance upper bound, the prior choice already
   used by Asimov is only overwritten if:

   a. the recommendation by the configurator is *larger* than this value
   b. or no default value exists




Choices for logic
---------------------------

The idea is that basically everything is as self-consistent as possible.

- **The sampling rate**  is set using:

  * ``ell_max=3`` by default
  * ``ell_max=2`` for BNS
  * ``ell_max=4`` for total mass > 200 MSun
  * Be capped at 16384 Hz

-  **The starting frequency of the waveform generation** (``f_start``) is set from ``flow`` using:

  * ``ell_max=3`` by default
  * ``ell_max=2`` for BNS
  * ``ell_max=4`` for total mass > 200
  *  If there is a detchar recommendation of the segment length, see below.

- **The segment duration** is computed from
  ``f_start``, as defined above, unless there is detchar recommentdation on the segment length, see below.

Detchar recommendations logic
-----------------------------

Detchar can impose some restrictions on segment duration and minimum frequency (for each detector), based on data quality considerations, which implies additional checks in the configurator:

- If the maximum allowed duration is shorter than the recommended by the
  configurator, the input ``flow`` might be inconsistent with the new duration,
  i.e it might allow templates for which not even the (2,2) mode fits the
  segment length. In this case, we will iterate ``f_start`` until the template
  duration is less than the detchar recommended segment length. If ``f_start >
  f_low``, ``f_low=f_start``.  The reference frequency ``f_ref`` is set to
  ``f_start``.

- If there is an additional detchar recommendation on minimum frequency for each
  detector, we check if the detchar recommendation on ``flow``  is  lower than the
  ``flow`` proposed by  ``get_settings.py`` for each detector and in this case
  overwrite the value with the configurator recommendation, to satisfy the
  segment length requirements (see bullet point above). ``f_fref`` is set to
  ``f_start=f_low``.
