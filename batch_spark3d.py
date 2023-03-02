#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:13:54 2023

@author: A. Plaçais
fork from J. Hillairet JH218595
"""
import numpy as np

import spark3d as sp


# WARNING! No special characters are allowed as they mess with bash
# Examples of paths to avoid:
#   spaces in: /Documents/spark3d workspace 2023/
#   parenthesis in: ExportToSPARK3D(1).f3e

# First simple option: provide a .spkx file
# PROJECT = "/home/placais/Documents/Simulation/work_spark3d"
# args = ("coax_filter_correct_name.spkx", )
# kwargs = {}

# Second option, more complex: provide a .xml and a field map.
#   .xml can be generated by 'unzip project.spkz' and modified afterwards
#   field map can be .f3e, .dsp or .mfe
PROJECT = "/home/placais/Documents/Simulation/work_spark3d/swell"
args = ("Project.xml", "field.f3e")
kwargs = {"new_project_name": "my_very_new_project.spkx"}

# Create objects
spk = sp.Spark3D(PROJECT, *args, **kwargs)

# Simulation parameters
# CONFIG = "--list"
# CONFIG = "--validate"
CONFIG = "--config"
D_CONF = {"project": 1, "model": 1, "confs": 1, "em_conf": 1,
          "discharge_conf": 1, "video": -1}
# TODO implement Video Multipactor, Corona, Video Corona

# Run the Spark3D Simulation
BATCH = True

if not BATCH:
    spk.run(CONFIG, D_CONF)
    if CONFIG == "--config":
        my_power, my_time = spk.get_full_results()

else:
    counter = 0
    while counter < 10:
        spk.run("--config", D_CONF)
        my_freq, my_power = spk.get_results()
        with open('batch_results.txt', 'a+', encoding="utf-8") as f_handle:
            np.savetxt(f_handle, [my_power])
        counter += 1