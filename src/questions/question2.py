import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from src.questions.question import Question

class Question2(Question): 
    dataframe:pd.DataFrame  = pd.DataFrame({})
    
    def __init__(self, input_path) -> None:
        super().__init__(input_path)
    
    
    def get_annotation_trend(self)->None: 
        """ 
         Generates a bar-chart for each data 
        """
        corrupt_count_dict = self.dataframe["corrupt_data"].value_counts().to_dict() 
        corrupt_count =   corrupt_count_dict[True] 
        cantsolve_count_dict = self.dataframe["cant_solve"].value_counts().to_dict() 
        cantsolve_count =  cantsolve_count_dict[True] 
        print(corrupt_count)
        print(cantsolve_count)
        
         
        cant_solve_arr = []
        corrupt_arr = []
        
        for state, frame in self.dataframe.groupby(["user_id", ]): 
            cant_solve =len(frame[(frame["cant_solve"]==True)])
            corrupt =len(frame[(frame["corrupt_data"]==True)])
            
            cant_solve_arr.append(cant_solve if cant_solve>0 else -0.5)
            corrupt_arr.append(corrupt if corrupt > 0 else -0.5)
        
        del self.dataframe # clear the dataframe
        
        
        #visualize the bars
        x =np.arange( len(cant_solve_arr))
        width =0.2
        plt.bar(x, cant_solve_arr, color='thistle', width =width,label="cant solve")
        plt.bar(x+width, corrupt_arr, color='darkslateblue', width=width, label="corrupt data")
        plt.title("Annotators trend")
        plt.xlabel("Individual user indices")
        plt.ylabel("occurrences")
        plt.legend()
        plt.grid(linestyle=':')
    
                 
    def prepare_data(self)->None:
        for file_path in self.file_paths: 
            df = pd.read_csv(file_path)
            self.__process_df(df)
              
    
    def __process_df(self,df:pd.DataFrame)->None:
        # The row where cant_solve and corrupt_data are true, they are appended with each other
        cantsolve_df = df[ (df["cant_solve"]==True)]
        corrupt_df = df[ (df["corrupt_data"]==True)]
        self.dataframe=  self.dataframe.append(cantsolve_df) 
        self.dataframe= self.dataframe.append(corrupt_df) 
        
                
        
        
            
        
        
    
    