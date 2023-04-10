import pandas as pd 
import matplotlib.pyplot as plt

from src.question import Question


class Question3(Question): 
    ref_true = 0
    ref_false= 0
    def __init__(self, ref_path) -> None:
        super().__init__(ref_path=ref_path)
    
    
    def get_ref_balanced(self) -> None: 
        size = self.ref_true + self.ref_false
        pie_data = [ 
                    self.ref_true/size,
                    self.ref_false/size,
                    ]
        plt.pie(pie_data, labels=["True : {}".format(self.ref_true), "False : {}".format(self.ref_false)], autopct="%1.1f%%", colors=['skyblue', 'tomato'])
        plt.title("True vs False is_bicycle")
        
        
    def prepare_data(self) -> None:
        ref_df = pd.read_json(self.ref_path)
        is_bicycle_arr = ref_df.loc["is_bicycle"].to_numpy()
        arr_size = is_bicycle_arr.shape[0]
        self.ref_true =  is_bicycle_arr.sum()
        self.ref_false = arr_size - self.ref_true
        del ref_df
         
    def visualise(self) -> None:
        plt.show()