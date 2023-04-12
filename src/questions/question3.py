import pandas as pd 
import matplotlib.pyplot as plt

from src.questions.question import Question


class Question3(Question): 
    ref_true = 0 # The number of times where it is true
    ref_false= 0 # The number of times where it is false
    def __init__(self, ref_path) -> None:
        super().__init__(ref_path=ref_path)
    
    
    def get_ref_balanced(self) -> None: 
        """
          Compares the percentage of each possible value in the reference dataset
        """
        size = self.ref_true + self.ref_false
        pie_data = [ 
                    self.ref_true/size,
                    self.ref_false/size,
                    ]
        plt.pie(pie_data, autopct="%1.1f%%", colors=['thistle', 'darkslateblue'])
        plt.title("True vs False is_bicycle", loc ="center")
        plt.legend(labels=["True : {}".format(self.ref_true), "False : {}".format(self.ref_false)])
        
        
    def prepare_data(self) -> None:
        ref_df = pd.read_json(self.ref_path)
        is_bicycle_arr = ref_df.loc["is_bicycle"].to_numpy()
        arr_size = is_bicycle_arr.shape[0]
        self.ref_true =  is_bicycle_arr.sum()
        self.ref_false = arr_size - self.ref_true
        del ref_df
         