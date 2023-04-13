import json 
import re
import os
import shutil
import logging

import pandas as pd 

from src.utils import Utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DataLoder:    
    _mem_data = [] # Contains the accumulated data
    _ref_data = {} # Contains all references data
    _file_index = 0 # keeps track of the created file index 
        
    def __init__(self,intput_path:str, output_path:str, ref_path:str) -> None:
        if not os.path.exists(intput_path) or not os.path.exists(ref_path):
           raise Exception("The path to the data is not found")
        self._input_file = open(intput_path, 'r')
        self._output_path =output_path
        self.__setup_csv(output_path)
        self._ref_path = ref_path
        
    @staticmethod
    def __setup_csv(output_path:str):
        if os.path.exists(output_path): shutil.rmtree(output_path)
        os.mkdir(output_path)       
    
    def preload_ref(self)->None: 
        """ 
            Loads the reference file 
        """
        f = open(self._ref_path)
        self._ref_data = json.load(f)
    
       
    def preload_data(self)-> None: 
        """ 
          Reads the input file by chunks and processes each individually
        """
        remaining ="";                 
        while True: 
            chunk = self._input_file.read(500)
            remaining+=chunk 
            chunk_data = remaining
            remaining  = self.process_chunk(chunk_data)
            if not chunk: 
               self.write_to_csv()
               break

    def process_chunk(self, chunk:str)->str:
        """ 
        Parse a string chunk and extract the necessary paramters

        Args:
            chunk (str): The intended string for parsing

        Returns:
            str: The remaining chunk after the parsing
        """
        # 1 - Extract first the part matching the regex 
        match = re.search(r'{"t{0,1}ask_{0,1}inp{0,1}ut{0,1}":.*"project_root_node_input_id"\s*:\s*"([0-9]|[a-z]|-)*"}', chunk)
        if not match:  
            return chunk
        try:
            # 2- Transforms the matched string into a json
            json_data = json.loads(match.group())
            self.process_json(json_data, is_valid=True)

        except json.decoder.JSONDecodeError as err:
            # 3- In case where the string corresponds to an invalid json 
            # then the parameter extraction needs to be done manually
            json_data = Utils.extract_from_invalid_json(match.group())
            self.process_json(json_data, is_valid=False)            
        
        # return the remaining
        remaining = chunk[match.end():-1]
        
        return remaining
        
        
    def process_json(self, json:str, is_valid:bool)-> None:
        """ 
        Process a string and extracts the necessary parameters 
          
        Args:
            json (str): The string to pe processed
            is_valid(bool): Whether the string passed is a valid json
        """
        try:
            row = {}
            if is_valid:
                # extract the image id based on its url
                image_id = Utils.extract_image_id(json["root_input"]["image_url"])
                row ={
                "image_id":image_id ,
                "ref": self._ref_data[image_id]["is_bicycle"]
                }
                row.update(Utils.extract_param(json))
            else: 
                
                json["ref"] =self._ref_data[json["image_id"]]["is_bicycle"]
                row=json
       
            self._mem_data.append(row)
            # Data is wrote to the file per 3000 rows
            if len(self._mem_data) == 3000:
                self.write_to_csv()
             
        except KeyError as err:
            logger.error("Error occurred while accessing the key. The error {}".format(err))
        
    def write_to_csv(self,):
        """
          Write the accumulated data to a csv file 
          A new file is generated upon each write
        """
        file_index = str(self._file_index).zfill(2)
        file_path = os.path.join(self._output_path, "output_{}.csv".format(file_index))
        df = pd.DataFrame(self._mem_data,)
        df.to_csv(file_path, mode='w',)
        # clear the accumulated data
        self._mem_data.clear()
        logger.info("File {} is downloaded locally".format(file_index))
        self._file_index +=1
        
    
        
    
        
        
    
    
                                
        
        
        
        
    
            
        
        
            