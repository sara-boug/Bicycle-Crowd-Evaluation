from difflib import SequenceMatcher
import os 
import re

class Utils:
    
    @staticmethod
    def clear_str(data_str:str)->str:
        new_str = data_str.replace("\'", '\"')
        new_str = data_str.replace('\"\"','\"')
        new_str = data_str.replace("fase", "false")
        
        return new_str
    
    @staticmethod
    def clear_str_json(str:str)->str:
        new_str = str.replace("\"", "")
        new_str = new_str.replace("}", "")
        new_str = new_str.replace("{", "")
        new_str = new_str.replace(",", "")
        
        return new_str
        
    @staticmethod
    def extract_image_id(url:str)->str:         
        basename = os.path.basename(url)
        basename = basename.replace(".jpg","")
        return basename
    
    @staticmethod
    def extract_task_output_info(dict:dict)->float:
        task_output_dict = {}
        user = {}
        output = {}
        ratio = 0.8
        for key in dict: 
            if SequenceMatcher(None, key, "task_output").ratio() >=ratio:
               task_output_dict = dict[key]
            if SequenceMatcher(None, key, "project_node_input_id").ratio() >=ratio:
               output["project_id"] = dict[key]
            if SequenceMatcher(None, key, "loss").ratio() >=ratio:
               output["loss"] = dict[key]
            if SequenceMatcher(None, key, "user").ratio() >=ratio:
               user = dict[key]

               
        for key in task_output_dict:
            if SequenceMatcher(None, key, "answer").ratio() >=ratio:
               output["answer"]= task_output_dict[key]
            if SequenceMatcher(None, key, "cant_solve").ratio() >=ratio:
               output["cant_solve"]= task_output_dict[key]
            if SequenceMatcher(None, key, "corrupt_data").ratio() >=ratio:
               output["corrupt_data"]= task_output_dict[key]    
            if SequenceMatcher(None, key, "duration_ms").ratio() >=ratio:
               output["duration_ms"]= task_output_dict[key] if "ms" in key else task_output_dict[key] *1000          
        
        for key in user: 
            if SequenceMatcher(None, key, "id").ratio() >=ratio:
               output["user_id"]= user[key]
        
        return output 
    
    
    @staticmethod
    def extract_from_invalid_json(data:str)->dict:
        output = {}
        ratio = 0.75
        all_matches = re.finditer(r'"\S*\"*|\"*\S*"|[a-z]+|([0-9]+(\.[0-9]*){0,1})', data)        
        for match in all_matches:
            match = match.group()
            if SequenceMatcher(None, match, '"id"').ratio() >=ratio:
               output["user_id"] =Utils.clear_str_json( next(all_matches).group())
            if SequenceMatcher(None, match, "project_node_input_id").ratio() >=ratio:
               output["project_id"] =Utils.clear_str_json(  next(all_matches).group())
            if SequenceMatcher(None, match, "answer").ratio() >=ratio:
               output["answer"] = Utils.clear_str_json(  next(all_matches).group())
            if SequenceMatcher(None, match, "loss").ratio() >=ratio:
               output["loss"] = Utils.clear_str_json(  next(all_matches).group())
            if SequenceMatcher(None, match, "cant_solve").ratio() >=ratio:
               output["cant_solve"] =Utils.clear_str_json(  next(all_matches).group())
            if SequenceMatcher(None, match, "corrupt_data").ratio() >=ratio:
               output["corrupt_data"] =Utils.clear_str_json(  next(all_matches).group())
            if SequenceMatcher(None, match, "duration_ms").ratio() >=ratio:
               duration =  Utils.clear_str_json(  next(all_matches).group())
               duration = float(duration)
               output["duration_ms"] =  duration if "ms" in match else duration *1000     
            if SequenceMatcher(None, match, "image_url").ratio() >=ratio:
               output["image_id"] =Utils.clear_str_json( Utils.extract_image_id(next(all_matches).group()))
        return output
        
 
        