import json 
import re
import os
import shutil

import pandas as pd 

from src.utils import Utils


class DataLoder:    
    _mem_data = []     
    _ref_data = {}
    _file_index = 0
        
    def __init__(self,intput_path:str, output_path:str, ref_path:str) -> None:
        self._input_file = open(intput_path, 'r')
        self._output_path =output_path
        self.__setup_csv(output_path)
        self._ref_path = ref_path
        
    @staticmethod
    def __setup_csv(output_path:str):
        if os.path.exists(output_path): shutil.rmtree(output_path)
        os.mkdir(output_path)       
    
    def preload_ref(self)->None: 
        f = open(self._ref_path)
        self._ref_data = json.load(f)
    
        
    def preload_data(self)-> None: 
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
        chunk = Utils.clear_str(chunk)
        match = re.search(r'{"t{0,1}ask_{0,1}inp{0,1}ut{0,1}":.*"project_root_node_input_id"\s*:\s*"([0-9]|[a-z]|-)*"}', chunk)
        
        if not match:  
            print("No match found")
            print(chunk)
            return chunk
        try:
            json_data = json.loads(match.group())
            self.process_json(json_data, is_valid=True)

        except json.decoder.JSONDecodeError as err:
            print("Error decoding json")
            json_data = Utils.extract_from_invalid_json(match.group())
            self.process_json(json_data, is_valid=False)            
            print(err)
        
        remaining = chunk[match.end():-1]
        
        return remaining
        
        
    def process_json(self, json:str, is_valid:bool)-> None:
        try:
            row = {}
            if is_valid:
                image_id = Utils.extract_image_id(json["root_input"]["image_url"])
                row ={
                "image_id":image_id ,
                "ref": self._ref_data[image_id]["is_bicycle"]
                }
                row.update(Utils.extract_task_output_info(json))
            else: 
                json["ref"] =self._ref_data[json["image_id"]]["is_bicycle"]
                row=json
       
            self._mem_data.append(row)
            if len(self._mem_data) == 3000:
                self.write_to_csv()
             
        except KeyError as err:
            print("Key not found in the JSON")
            print(json)
            print(err)
        
    def write_to_csv(self,):
        file_index = str(self._file_index).zfill(2)
        file_path = os.path.join(self._output_path, "output_{}.csv".format(file_index))
        df = pd.DataFrame(self._mem_data,)
        df.to_csv(file_path, mode='w',)
        self._mem_data.clear()
        self._file_index +=1
        
    
        
    
        
        
    
    
                                
        
        
        
        
    
            
        
        
            