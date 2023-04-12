# Bicycle Crowd Evaluation 

## How to run the program 

### initial constraints 
All the dataset should be unzipped and put in this folder **[project_dir]/data/**  
The name or the path of the folder could be changed from the config file found in **[poject_dir]/src/config.py**  
The name of the two files should be __references.json__ and __anonymized_project.json__. 
If you choose to use a different filename, it could be modified in **[poject_dir]/src/config.py**

The code has been developed using Python3 on an ubuntu operating systems 

--------------------------------
Initially, run the following command: 
``` 
python3 main.py -pre
```
This performs the initial preprocessing of the data, the generated files are found in the **data/output** folder. the questions can not be run, if the preprocessing is not performed

Each question can be run independently from the other:

* To run question 1
``` 
python3 main.py -q1
```
* To run question 2
``` 
python3 main.py -q2
```
* To run question 3
``` 
python3 main.py -q3
```
* To run question 4
``` 
python3 main.py -q4
```

