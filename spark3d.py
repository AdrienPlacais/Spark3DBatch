# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 16:49:00 2014

@author: JH218595
"""
import os
import numpy as np 

class Spark3d(object):
    """
    SPARK3D simulation object
    
    """
    BIN_PATH = '/Applications/SPARK3D.1.1/dist/spark3d'

    
    def __init__(self, project_path, data_file, file_type='hfss', output_path='results/', tmp_path='/tmp/SPKTMP'):
        """
        Constructor.
        
        Arguments
        ---------
         project_path : absolute path (important!) of the project. 
         data_file : relative path of the data file
         [file_type : {'hfss' (default),'cst','csv'}]
         [output_path: relative path of the output dir (default: "results/")]
         [tmp_path: temporary file absolute path (default: '/tmp/SPKTMP')]
        
        """
        self.project_path = project_path
        self.data_file = data_file
        self.file_type = file_type
        self.tmp_path = tmp_path
        self.config_file = 'config.min'
        self.output_path = output_path
    
    def run(self):
        """
        Run the SPARK3D modeling. 
        
        """
        try:
            os.system(self.__get_run_command__())
        except OSError as e:
            print('Error ! '+e)
        
    def __get_run_command__(self):
        cmd = self.BIN_PATH + \
              ' --mode=multipactor' + \
        	  ' --project_path='+self.project_path + \
        	  ' --tmp_path='+self.tmp_path + \
        	  ' --config_file='+self.config_file + \
        	  ' --output_path='+self.output_path + \
        	  ' --data_file='+self.data_file + \
              ' --file_type='+self.file_type
              
        return(cmd)
    
    def get_results(self):
        """
        Returns the SPARK3D run results
        
        Arguments
        ----------
         none
        
        Returns
        ----------
         freq: array of frequency
         power: array of breakdown power
         
        """
        freq, power = np.loadtxt(self.project_path+'/'+self.output_path+'/general_results.txt', 
                           skiprows=1, 
                           delimiter='\t', 
                           usecols=(3,4), # use only columns 3 and 4
                           unpack=True)
        return(freq, power)     

    def set_config(self):
        pass
           
if __name__ == "__main__":  
    project_path = '/home/sccp/gchf/JH218595/Desktop/Zone_Travail/Spark3D/Simple_Waveguide_WR284_3.7GHz'
    data_file = 'data_HFSS/SimpleWaveguideFields_72.14x22mm_100mm.dsp'  
    spk = Spark3d(project_path, data_file)     
    spk.run()
    freq, power =spk.get_results()
    print(freq, power)
    with open('RESULTS.txt','a') as f_handle:
        np.savetxt(f_handle, [power])