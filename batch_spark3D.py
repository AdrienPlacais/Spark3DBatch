# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:44:12 2014

@author: JH218595
"""
from spark3d import *

project_path = '/home/sccp/gchf/JH218595/Desktop/Zone_Travail/Spark3D/Simple_Waveguide_WR284_3.7GHz'
data_file = 'data_HFSS/SimpleWaveguideFields_72.14x22mm_50mm_V2.dsp'  
spk = Spark3d(project_path, data_file)

counter = 0
while counter < 100:
    spk.run()
    # Append the results to a text file
    freq, power =spk.get_results()
    with open('RESULTS.txt','a') as f_handle:
        np.savetxt(f_handle, [power])
    counter = counter + 1