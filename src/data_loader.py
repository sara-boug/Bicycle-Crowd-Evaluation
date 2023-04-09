import pandas as pd 

import json 
import re
import os
import shutil



class DataLoder:    
    _mem_data = []     
    _file_index = 0
    
    def __init__(self,intput_path:str, output_path:str) -> None:
        self._input_file = open(intput_path, 'r')
        self._output_path =output_path
        self.__setup_csv(output_path)
        
    @staticmethod
    def __setup_csv(output_path:str):
        if os.path.exists(output_path): shutil.rmtree(output_path)
        os.mkdir(output_path)       

    def preload(self)-> None: 
        remaining ="";                 
        while True: 
            chunk = self._input_file.read(500)
            remaining+=chunk 
            chunk_data = remaining
            remaining  = self.process_chunk(chunk_data)
            if not chunk: 
               self.write_to_csv()
               break

    def process_chunk(self, chunk:str)->None:
        chunk = self._clear_str(chunk)
        print("############################################ \n")
        match = re.search(r'{"t{0,1}ask_{0,1}inp{0,1}ut{0,1}":.*"project_root_node_input_id"\s*:\s*"([0-9]|[a-z]|-)*"}', chunk)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++ \n")
        
        if not match:  
            print("No match found")
            print(chunk)
            return chunk
        try:
            json_data = json.loads(match.group())
            self.process_json(json_data)

        except json.decoder.JSONDecodeError as err:
            print("Error decoding json")
            print(match.group())
            print(err)
        
        remaining = chunk[match.end():-1]
        
        return remaining
        
        
    def process_json(self, json:str)-> None:
        try:
            row ={
               "user_id": json["user"]["id"],
               "image_id": self._extract_image_id(json["root_input"]["image_url"]),
               "project_id": json["project_node_input_id"],
               "answer": json["task_output"]["answer"],
               "cant_solve": json["task_output"]["cant_solve"],
               "corrupt_data": json["task_output"]["corrupt_data"],
               "duration_ms": self._extract_duration(json["task_output"]),
               "loss" : self._extract_loss(json),
            }
            self._mem_data.append(row)
            print(len(self._mem_data))
            if len(self._mem_data) == 3000:
                self.write_to_csv()
             
        except KeyError as err:
            print("Key not found in the JSON")
            print(json)
            print(err)
            
        
    @staticmethod
    def _extract_image_id(url:str)->str:         
        basename = os.path.basename(url)
        basename = basename.replace(".jpg","")
        return basename
    
    @staticmethod
    def _extract_duration(dict:dict)->float:
        if "duration_ms" in dict:
          return dict["duration_ms"]
        if "duration_s" in dict:
            return dict["duration_s"]* 1000 
        
    @staticmethod
    def _extract_loss(dict:dict)->float:
        if "loss" in dict:
            return dict["loss"]
        if "oss" in dict:
            return dict["oss"]
        
    @staticmethod
    def _clear_str(data_str:str)->str:
        new_str = data_str.replace("'", '"')
        new_str = data_str.replace('""','"')
        new_str = data_str.replace("fase", "false")
        
        return new_str
    
    def write_to_csv(self,):
        file_index = str(self._file_index).zfill(2)
        file_path = os.path.join(self._output_path, "output_{}.csv".format(file_index))
        df = pd.DataFrame(self._mem_data,)
        df.to_csv(file_path, mode='w',)
        self._mem_data.clear()
        self._file_index +=1
        
        
    
    
                                
        
        
        
        
    
            
        
        
            