import argparse

import src.question_runner  as runner 

if __name__ == '__main__':
    
   parser = argparse.ArgumentParser()
   
   parser.add_argument("-pre", help="Preprocess the available data", action="store_true")
   parser.add_argument("-q1", help="Runs question 1",action="store_true")
   parser.add_argument("-q2", help="Runs question 2",action="store_true")
   parser.add_argument("-q3", help="Runs question 3",action="store_true")
   parser.add_argument("-q4", help="Runs question 4",action="store_true")
   
   args = parser.parse_args()
   
   if args.pre:
      runner.preprocess()
   if args.q1 :
      runner.question1()
   if args.q2 :
      runner.question2()
   if args.q3 :
      runner.question3()
   if args.q4 :
      runner.question4()
       
   
   
   
   
   

