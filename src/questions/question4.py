import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from src.questions.question import Question

class Question4(Question): 
    data = {}
    def __init__(self, input_path) -> None:
        super().__init__(input_path)
    
    def get_bad_annotators(self)-> None: 
        mse_err = []
        mse_err_only =[]
        for key in self.data: 
            mse_err.append( self.data[key])
            if self.data[key]>=0.1:
               mse_err_only.append(self.data[key])
        
        
        fig, ax = plt.subplots(2)
 
        ax[0].set_title("Histogram of annotators mse error")
        ax[0].hist(mse_err, bins=40,  )
        
        counts, bins = np.histogram(mse_err_only)
        pie_data =counts/ counts.sum()
        labels = ["{:.1f}".format(bin) for bin in bins[:-1] ] 
        ax[1].pie(pie_data,labeldistance=1.2 )
        ax[1].legend(labels,loc="lower right")
        ax[1].set_title("MSE error > 0.1")
                   
    def prepare_data(self)->None:
        for file_path in self.file_paths: 
            df = pd.read_csv(file_path)
            self.__process_df(df)
            
                
    def __process_df(self,dataFrame:pd.DataFrame)->None: 
        dfs =  dataFrame.groupby("user_id")
        for state, frame in dfs : 
            answer= (frame["answer"].to_numpy() == "yes") *1
            ref = frame["ref"].to_numpy() *1
            
            mse = np.square(ref-answer).mean()            
            if state not in self.data: 
                self.data[state] =  mse
            else:
                self.data[state] = (self.data[state] + mse)/2
                
 
            
    
