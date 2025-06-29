#!/usr/bin/env python3
"""Provide an example main script.

.. todo::
    Fix paths with importlib

"""
from pathlib import Path

import numpy as np
import spark3dbatch.spark3d as sp
from spark3dbatch.helper import fmt_array
from spark3dbatch.xml_parser import SparkXML

# First simple option: provide a ``SPKX`` file
project = Path("/home/placais/Documents/simulation/python/Spark3DBatch/data/")
args = ("Coax_filter_CST(M, C, Eigenmode).spkx",)
kwargs = {}

# Second option, more complex: provide a ``XML`` and a field map.
#   ``XML`` can be generated by 'unzip project.spkx' and modified afterwards
#   field map can be .f3e, .dsp or .mfe
# project = "/home/placais/Documents/Simulation/work_spark3d/swell"
# args = ("my_Project.xml", "field.f3e")
# kwargs = {"new_project_name": "my_very_new_project.spkx"}

if __name__ == "__main__":
    spk = sp.Spark3D(project, *args, **kwargs)

    # Simulation parameters
    # mode = "--list"
    # mode = "--validate"
    mode = "--config"
    config = {
        "project": 1,
        "model": 1,
        "confs": 1,
        "em_conf": 1,
        "discharge_conf": 1,
        "video": -1,
    }

    selection = 0

    # =========================================================================
    # Simple run
    # =========================================================================
    if selection == 0:
        spk.run(mode, config)
        if mode == "--config":
            my_power, my_time = spk.get_full_results()

    # =========================================================================
    # Same run over and over for convergence
    # =========================================================================
    elif selection == 1:
        counter = 0
        while counter < 10:
            spk.run("--config", config)
            my_freq, my_power = spk.get_results()

            with open("batch_results.txt", "a+", encoding="utf-8") as f_handle:
                np.savetxt(f_handle, [my_power])

            counter += 1

    # =========================================================================
    # Other studies, manually modify the xml
    # =========================================================================
    elif selection == 2:
        assert (
            ".xml" in args[0]
        ), "The edition of the simulation properties requires a ``XML`` + "
        "field map input."

        xml = SparkXML(project / args[0])
        xml_conf = xml.get_config(**config)

        new_power = fmt_array(np.linspace(1e-2, 1e2, 5))
        alter_conf = {
            "initialNumberElectrons": 100,
            "pathRelativePrecision": 0.1,
            "PowerSweep/sweepPoints": new_power,
        }
        # Warning, save=True will overwrite previous ``XML``.
        xml.edit(xml_conf, save=True, **alter_conf)
        spk.run("--validate", config)

        counter = 0
        while counter < 4:
            xml.edit(xml_conf, save=True, **alter_conf)
            spk.run("--config")
            my_freq, my_power = spk.get_results()

            with open("sweep_results.txt", "a+", encoding="utf-8") as f_handle:
                np.savetxt(f_handle, [my_power])

            counter += 1
            alter_conf["initialNumberElectrons"] += 10
