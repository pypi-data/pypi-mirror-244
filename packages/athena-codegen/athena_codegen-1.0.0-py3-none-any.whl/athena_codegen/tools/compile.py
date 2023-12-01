import os
import requests
import json
from dotenv import load_dotenv  
from pathlib import Path  

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x

current_file = Path(__file__).resolve()  
current_dir = current_file.parent
parent_dir = current_dir.parent
env_path = parent_dir / '.env'  
load_dotenv(dotenv_path=env_path, verbose=True)  


def compile_error():
    url_prefix = os.getenv('assistantToolsUrl', '')
    path = "/compileCheck/compile"
    url = "/".join([url_prefix.rstrip("/"), path.lstrip("/")])  

    pomHome = os.getenv('pomHome', "xxx")
    pomHome = pomHome.replace("\\", "\\\\") 

    payload = json.dumps({
        "mvnHome": "ABC",
        "pomHome": pomHome
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        if response.json()['success'] == False:  
            errors = []  
            for error in response.json()['errors']:  
                error_dict = {}  
                error_dict['Source Code'] = error['sourceCode']    
                error_dict['Error Details'] = error['errorDetails']    
                errors.append(error_dict) 
            return errors
        else:
            print(colored("compile no error", 'green'))
            return False
    else:  
        print(colored(response.text, 'red'))
        return False
    

# Call the function  
# print(compile_error())

