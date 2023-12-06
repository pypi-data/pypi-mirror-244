import warnings
warnings.filterwarnings("ignore")
import os,sys
from datetime import datetime
import logging

def logger(name):
    
    LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

    folder=name
    log_path=os.path.join(os.getcwd(),folder)

    os.makedirs(log_path,exist_ok=True)

    LOGFILEPATH=os.path.join(log_path,LOG_FILE)

    logging.basicConfig(level=logging.INFO,
                        filename=LOGFILEPATH,
                        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s")



class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return "Error occured in script name  [{0}] at line no [{1}] error message is [{2}]".format(
            self.file_name,self.lineno,str(self.error_message))