import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import os


class Question1: 
    data = {}
    
    def __init__(self, input_path) -> None:
        self._intput_path = input_path
        self._file_paths =[os.path.join(input_path, file) for file in  os.listdir(input_path)]
        self._file_paths.sort()
    
    def annotators_number(self,) -> int:
        return len(self.data.keys())
    
    def annotation_time(self)->None:
        list_min = []
        list_max = []
        list_avg = []
        
        for key in self.data: 
            durations = self.data[key]["durations"]
            durations= np.array(durations)/1000
             
            list_min.append(np.min( durations))
            list_max.append(np.max( durations))               
            list_avg.append(np.mean(durations)) 
               
        plt.figure()
        plt.plot(np.array(list_min),color='thistle', label="min" )
        plt.plot( np.array(list_max),color='mediumslateblue', label= "max")
        plt.plot(np.array(list_avg),color='darkslateblue', label="Avg")
        
        plt.xlabel("User indices")
        plt.ylabel("Durations (ms)")
        plt.ylim(ymax=6, ymin=0)
        plt.legend(loc="upper right")
        plt.grid()
        plt.show()
    
    def prepare_data(self)->None:
        for file_path in self._file_paths: 
            df = pd.read_csv(file_path)   
            self.process_df(df) 
            
    
    def process_df(self,dataFrame:pd.DataFrame):
        dfs =  dataFrame.groupby("user_id")
        for state, frame in dfs : 
            self.add_to_data(state, frame["duration_ms"].to_list(),frame["answer"].to_list() )          
                
    def add_to_data(self, key, durations,answer,  ):
        if key not in self.data: 
           self.data[key] =  {"durations": durations, "answer":answer}
        else:
           self.data[key]["durations"] =self.data[key]["durations"] + durations
           self.data[key]["answer"] =self.data[key]["answer"] + answer
           