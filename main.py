import os

from src.data_loader import DataLoder
from src.question1 import Question1
from src.question2 import Question2
from src.question3 import Question3

ouput_path = os.path.join(os.getcwd(),"data","output")
ref_path = os.path.join(os.getcwd(),"data","references.json")


def preprocess():
    input_path = os.path.join(os.getcwd(),"data","anonymized_project.json")
    data_loader = DataLoder(input_path, ouput_path, ref_path)
    data_loader.preload_ref()
    data_loader.preload_data()
    
def question1():
    question1 = Question1(ouput_path)
    question1.prepare_data()
    question1.annotators_disag()
    question1.annotation_time()
    question1.annotators_avg_answ()
    question1.visualize()
     
def question2():
    question2 = Question2(ouput_path)
    question2.prepare_data()
    question2.get_annotation_trend()
    question2.visualise()
    
def question3():
    question3 = Question3(ref_path)
    question3.prepare_data()
    question3.get_ref_balanced()
    question3.visualise()


if __name__ == '__main__':
   question3()

