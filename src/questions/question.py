from abc import abstractmethod, ABC
import os

import matplotlib.pyplot as plt 

class Question(ABC): 
    def __init__(self, input_path=None, ref_path=None) -> None:
        if input_path != None:
            self.file_paths =[os.path.join(input_path, file) for file in  os.listdir(input_path)]
            if len(self.file_paths) == 0 :
                raise Exception("No data found, ensure that the preprocessing is run first")
            self.file_paths.sort()
        if ref_path!= None:
            if  not os.path.exists(ref_path): 
                raise Exception("Reference file not found")
            self.ref_path =ref_path
    
    @abstractmethod
    def prepare_data(self)->None:
        """ 
           Iterates through all the files and process each file individually 
        """
        pass
    
    def visualize(self)->None:
        plt.show()        
        

    
    
