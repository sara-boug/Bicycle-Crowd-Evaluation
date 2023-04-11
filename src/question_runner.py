import os 

from src.config import output_path, ref_path, input_path
from src.data_loader import DataLoder
from src.questions.question1 import Question1
from src.questions.question2 import Question2
from src.questions.question3 import Question3
from src.questions.question4 import Question4

def preprocess():
    data_loader = DataLoder(input_path, output_path, ref_path)
    data_loader.preload_ref()
    data_loader.preload_data()
    
def question1():
    question1 = Question1(output_path)
    question1.prepare_data()
    question1.annotators_disag()
    question1.annotation_time()
    question1.annotators_avg_answ()
    question1.visualize()
     
def question2():
    question2 = Question2(output_path)
    question2.prepare_data()
    question2.get_annotation_trend()
    question2.visualise()
    
def question3():
    question3 = Question3(ref_path)
    question3.prepare_data()
    question3.get_ref_balanced()
    question3.visualise()

def question4():
    question4 = Question4(output_path)
    question4.prepare_data()
    question4.get_bad_annotators()
    question4.visualise()
