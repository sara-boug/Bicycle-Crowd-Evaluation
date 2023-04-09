from src.data_loader import DataLoder
from src.question1 import Question1

import os

ouput_path = os.path.join(os.getcwd(),"data","output")

def preprocess():
    input_path = os.path.join(os.getcwd(),"data","anonymized_project.json")
    data_loader = DataLoder(input_path, ouput_path)
    data_loader.preload()
    
def question1():
    question1 = Question1(ouput_path)
    question1.prepare_data()
    question1.annotation_time()
    
    
if __name__ == '__main__':
   question1()

