PEconfigurator examples
=======================

``peconfigurator`` can be employed to obtain updated recommended settings on existing analysis like the public Gravitational Wave Transient Catalogues (GWTCs) or OnlinePE results. In this example we will analyze some parameter estimation results from `GWTC-2.1 <https://zenodo.org/record/6513631>`_ and `GWTC-3 <https://zenodo.org/record/5546663>`_.

Vanilla BBH: GW150914
----------------------

In this example we analyze the posterior samples from GW150914 as a prototype case of vanilla BBH system. After downloading the corresponding PESummary file from the GWTC-2.1 release, peconfigurator can be run on it as:

.. code-block:: console
    :linenos:

    peconfigurator /PATH-TO-GWTC-FILES/IGWN-GWTC2p1-v2-GW150914_095045_PEDataRelease_mixed_cosmo.h5 \
    --dataset C01:IMRPhenomXPHM \
    --q-min 0.05 \
    --HM \
    --include_dL_recommendations \
    --override_safeties \
    --json_file GW150914.json \
    --report_file GW150914.ipynb

This will produce some output while it runs, mainly with information about the different checks that are performed on the samples, and the suggested settings for this analysis. This suggested settings are also encoded in a json file, which in our case will be ``GW150914.json``, with the following structure:

.. code-block:: json
    :linenos:

    {
        "srate": 1024,
        "f_start": 13.33,
        "f_ref": 20.0,
        "seglen": 8.0,
        "chirpmass_min": 24.98652353704537,
        "chirpmass_max": 34.98256463854806,
        "meco_status": "True",
        "metadata": {
            "date": "2023-07-03 08:35:22.580931",
            "command_line_args": "Namespace(samples_file='gwtc-files-peconf/IGWN-GWTC2p1-v2-GW150914_095045_PEDataRelease_mixed_cosmo.h5', dataset='C01:IMRPhenomXPHM', output_dir='./', HM=True, q_min=0.05, dL_max=None, ell_max=3, tolerance=2.0, nbins=50, flow=20.0, f_ref=20.0, bounds_tol=0.2, json_file='GW150914.json', report_file='GW150914.ipynb', override_safeties=True, debug=False, include_dL_recommendations=True, override_fstart=-1, detchar_seglen=-1, enforce_ellmax=False, legacy=False)"
        }
    }

In this case, since distance and mass-ratio posteriors are sane in the input file, the only prior recommendation that is given is the chirp-mass bounds. Notice also that the ``metadata`` field contains all arguments employed, for reproducibility.

One can compare the ``peconfigurator`` recommended settings with the settings employed in GWTC-2.1, in particular the segment duration has increased from 4 secons to 8 seconds. This is due to the fact the the current version of the ``peconfigurator`` employs as default the ``l=3, m=3`` mode for computing the duration of the templates, and set the segment duration accordingly for allowing the templates to fit in.


High-mass BBH: GW190521
-----------------------

GW190521 is a good example case for high total mass BBH systems:

.. code-block:: console
    :linenos:

    peconfigurator /PATH-TO-GWTC-FILES/IGWN-GWTC2p1-v2-GW190521_030229_PEDataRelease_mixed_cosmo.h5 \
    --dataset C01:IMRPhenomXPHM \
    --q-min 0.05 \
    --HM \
    --include_dL_recommendations \
    --override_safeties \
    --json_file GW190521.json \
    --report_file GW190521.ipynb

For high total mass systems, where the merger and ringdown stages of the signal might dominate, it becomes important to resolve well the higher-order mode content of the signal, and therefore ``peconfigurator`` set the highest higher-mode employed for the analysis from ``l=3, m=3`` to ``l=4, m=4``. This affects the sampling frequency estimation, as well the signal duration, which now will be based on the length of the longest template containing the ``l=4, m=4`` mode:

.. code-block:: json
    :linenos:

    {
        "srate": 1024,
        "f_start": 10.0,
        "f_ref": 11.0,
        "seglen": 8.0,
        "chirpmass_min": 36.213576075797505,
        "chirpmass_max": 186.74943843596762,
        "meco_status": "False",
        "metadata": {
            "date": "2023-07-03 11:04:42.438823",
            "command_line_args": "Namespace(samples_file='gwtc-files-peconf/IGWN-GWTC2p1-v2-GW190521_030229_PEDataRelease_mixed_cosmo.h5', dataset='C01:IMRPhenomXPHM', output_dir='./', HM=True, q_min=0.05, dL_max=None, ell_max=4, tolerance=2.0, nbins=50, flow=20.0, f_ref=20.0, bounds_tol=0.2, json_file='GW190521.json', report_file='GW190521.ipynb', override_safeties=True, debug=False, include_dL_recommendations=True, override_fstart=-1, detchar_seglen=-1, enforce_ellmax=False, legacy=False)"
        }
    }

Notice the ``ell_max=4`` option recorded in the ``metadata`` field. If one wants to disable this automated check of the appropiate ``ell_max``, one can employ the ``--enforce_ellmax`` option, which will enforce to employ the input ``ell_max`` (3 as default, but can be specified to another value using the ``ell_max`` option).

For high total mass systems, it might happen that the default reference frequency (20Hz) is higher than the MECO (minimum energy circular orbit) frequency estimated from the input samples. In this case, the value will be overwritten to a safe value. For this particular case, we can notice that it has been overwritten, as warned in the output:

.. code-block:: console
    
    Checking that f_ref is not above f_MECO: FAILED
    WARNING: the reference frequency is too close to the MECO frequency, f_MECO = 11.766386019306152, overwritting reference frequency to f_ref=11.0

In the detailed report generated ``GW190521.html``, we can see the estimated posterior for the MECO frequency from the input samples, as well as the default value and the new recommended value:

.. figure:: images/MECO_gw190521.png
   :alt: MECO_gw190521

Binary neutron star: GW190425
-----------------------------

For an example of binary neutron-star systems, we can analyze the posterior samples from GW190425:

.. code-block:: console
    :linenos:

    peconfigurator /PATH-TO-GWTC-FILES/IGWN-GWTC2p1-v2-GW190425_081805_PEDataRelease_mixed_cosmo.h5 \
    --dataset C01:IMRPhenomPv2_NRTidal:HighSpin \
    --q-min 0.05 \
    --HM \
    --include_dL_recommendations \
    --override_safeties \
    --json_file GW190425.json \
    --report_file GW190425.ipynb

For binary neutron-star systems, ``peconfigurator`` overwrites ``ell_max=2`` since the higher-mode high frequency content is typically not in the detector's band, and also to not increase dramatically the segment duration recommendation, since higher-modes during the inspiral typically are negligible for this kind of systems. As with the high total-mass systems, this behaviour can be disabled using the ``--enforce_ellmax`` option.

Additionally, even with ``ell_max=2``, the recommended sampling rate might be higher than 16384Hz, the highest sampling rate at which detector data is sampled, and therefore in such situations the ``peconfigurator`` overwrites its value to 16384Hz.

Incorporating detector-characterization (detchar) recommendations
-----------------------------------------------------------------

If there are recommendations on maximum segment duration or minimum allowed frequency based on data quality considerations, these can be added to the analysis using the ``--detchar_seglen`` and ``--flow`` options. For example, consider than for the previous example we are recommended to not employ more than 36 seconds of data. Therefore, analyzing with this recommendation:

.. code-block:: console
    :linenos:

    peconfigurator /PATH-TO-GWTC-FILES/IGWN-GWTC2p1-v2-GW190425_081805_PEDataRelease_mixed_cosmo.h5 \
    --dataset C01:IMRPhenomPv2_NRTidal:HighSpin \
    --q-min 0.05 \
    --HM \
    --include_dL_recommendations \
    --override_safeties \
    --detchar_seglen 36 \
    --json_file GW190425.json \
    --report_file GW190425.ipynb

will trigger a new estimation of ``f_start`` (and consequently reference frequency a minimum frequency ``f_low``) to be consistent with the new suggested duration, as we can see in the output:

.. code-block:: console
    
    Estimated seglen of 128.0s is greater than detchar recommendation of 32s.
    Overriding segment length to 32s.
    Overriding minimum frequency flow to 34.050000000000054Hz to satisfy duration restriction.

    The reference frequency (20.0) is lower than the starting waveform generation frequency, 34.050000000000054 Hz, overwritting reference frequency to f_start.

as well as in the recommendations json file and the detailed report (notice that segment recommendation has been rounded to the previous power of two, since this is typically need for parameter estimation analysis).