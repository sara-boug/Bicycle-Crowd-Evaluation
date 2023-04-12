import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from src.questions.question import Question


class Question1(Question): 

    data_abc = {} # The extracted data for question abc
    data_d = {} # The extracted data for question d 
    
    def __init__(self, input_path) -> None:
        super().__init__(input_path)
        self.fig, self.ax = plt.subplots(2)

    
    def get_annotators_number(self,) -> int:
        # Reflects the number of unique user ids 
        return len(self.data_abc.keys())
    
    
    def get_annotation_time(self)->None:
        """ 
             Generates a linechart describing the min,max,average duration time per user
        """
        list_min = []
        list_max = []
        list_avg = []
        
        for key in self.data_abc: 
            
            durations = self.data_abc[key]["durations"]
            durations= np.array(durations) 
             
            list_min.append(np.min( durations))
            list_max.append(np.max( durations))               
            list_avg.append(np.mean(durations)) 
               
        self.ax[0].plot(np.array(list_min),color='thistle', label="min" )
        self.ax[0].plot( np.array(list_max),color='mediumslateblue', label= "max")
        self.ax[0].plot(np.array(list_avg),color='darkslateblue', label="avg")
        
        self.ax[0].set_xlabel("User indices")
        self.ax[0].set_ylabel("Durations (ms)")
        self.ax[0].set_ylim(ymax=6000, ymin=0)
        self.ax[0].legend(loc="upper right")
        self.ax[0].grid()
        self.ax[0].set_title("Avg, min, max duration per annotator")
    
    def get_annotators_avg_answ(self): 
        """ 
             Generated a line-chart describing the amount of answers provided per user
        """
        answers = []
        for key in self.data_abc: 
            answer = self.data_abc[key]["answer"]
            answers.append(answer)
            
        self.ax[1].plot(answers,color='mediumslateblue')
        self.ax[1].set_xlabel("User indices")
        self.ax[1].set_ylim(ymax=100, ymin=0)
        self.ax[1].set_ylabel("Amount of answers")
        self.ax[1].grid()
        self.ax[0].set_title("Amount of answers per annotator")

    def get_annotators_disag(self):
        """ 
           Generates a bar-chart describing the yes/No answers for the images with high disagreement
        """
        fig, ax = plt.subplots()
        yes_list = []
        no_list = []
        indices = []
        
        for key in self.data_d: 
            yes=self.data_d[key]["yes"]
            no=self.data_d[key]["no"]
            
            if yes ==0 or no ==0:
               continue
            else:
                min_v = min(yes,no)
                max_v = max(yes,no)
                ratio = min_v/max_v
                # Higher ratio between yes and no describes high disagreement
                if 1>=ratio>0.7: 
                   yes_list.append(yes)
                   no_list.append(no)
                   indices.append(key)
                   
        self.data_d.clear()
        print(len(indices))
        x =np.arange(len(indices))
        width =0.3
        ax.bar(indices, yes_list, color='thistle', width =width,label="yes")
        ax.bar(x+width, no_list, color='darkslateblue', width=width, label="no")
        ax.set_xlim(xmax=15, xmin=-1)
        ax.set_title("Images with the highest disagreement (yes/no ratio)")
        plt.xticks(rotation=45, ha='right')
        ax.grid()
        ax.legend()

          
    def visualize(self)->None:
        self.data_abc.clear()
        plt.show()
        
    def prepare_data(self)->None:
        for file_path in self.file_paths: 
            df = pd.read_csv(file_path)   
            self.__process_df_abc(df) 
            self.__process_df_d(df) 
                  
    def __process_df_abc(self,dataFrame:pd.DataFrame):
        # This allows extracting the data per user and getting insight about each individual user
        # The durations will be accumulated per individual user in an array 
        # The number of answers are summed per user 
        dfs =  dataFrame.groupby("user_id")
        for state, frame in dfs : 
            durations= frame["duration_ms"].to_list()
            answer= len(frame["duration_ms"]) 
            
            if state not in self.data_abc: 
                self.data_abc[state] =  {"durations": durations, "answer":answer}
            else:
                self.data_abc[state]["durations"] =self.data_abc[state]["durations"] + durations
                self.data_abc[state]["answer"] =self.data_abc[state]["answer"] + answer
           
           
    def __process_df_d(self,dataFrame:pd.DataFrame):
        # The data in this question is grouped by the image id
        # Then per image id the yes/No are accumulated 
        dfs =  dataFrame.groupby("image_id")
        for state, frame in dfs : 
            init = {"yes":0, "no":0}
            temp_values = frame["answer"].value_counts().to_dict()
            init.update(temp_values)
             
            yes= init["yes"]
            no= init["no"]
             
            if state not in self.data_d: 
                self.data_d[state] =  { "yes": yes, "no":no}
            else:
                self.data_d[state]["yes"] = self.data_d[state]["yes"] + yes
                self.data_d[state]["no"] = self.data_d[state]["no"] + no
        

                   
           