# flow.py
"""
1.必须先启动AssistantTools服务
2.设定好环境参数appId(应用名称ID)、projectHome(项目工程目录)、specHome(API规格存放目录)
3.运行
"""

from .tools.globals import global_vars
import requests
import json
import os
import socket
from dotenv import main, dotenv_values, set_key 
from pathlib import Path  
import warnings

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x

warnings.filterwarnings("ignore")
current_file = Path(__file__).resolve()  
current_dir = current_file.parent
env_path = current_dir / '.env' 
# load_dotenv(dotenv_path=env_path, verbose=True)  
env_vars = dotenv_values(dotenv_path=env_path) 

# 通过环境变量设置初始化变量
def init_env():
    # 读取变量  
    assistantToolsUrl = env_vars.get("assistantToolsUrl")
    projectHome = env_vars.get("projectHome")
    specHome = env_vars.get("specHome")  
    projectHome = env_vars.get("projectHome")  
    appId = env_vars.get("appId")  
    appToken = env_vars.get("appToken")  
    apiVersion = env_vars.get("apiVersion")  
    

    # 检查变量是否存在  
    if assistantToolsUrl is not None:  
        global_vars.update_var("assistantToolsUrl", assistantToolsUrl)  # 更新assistantToolsUrl变量的值  
    else:
        raise main.DotenvValueError("assistantToolsUrl variable is missing in .env file") 
    
    if specHome is not None:  
        global_vars.update_var("specHome", specHome)  # 更新specHome变量的值  
    else:
        raise main.DotenvValueError("specHome variable is missing in .env file")  
    
    if projectHome is not None:
        global_vars.update_var("projectHome", projectHome)  # 更新projectHome变量的值 
    else:  
        raise main.DotenvValueError("projectHome variable is missing in .env file") 

    if assistantToolsUrl is not None:
        global_vars.update_var("assistantToolsUrl", assistantToolsUrl)  # 更新projectHome变量的值 
    else:  
        raise main.DotenvValueError("assistantToolsUrl variable is missing in .env file") 
    
    if appId is not None:
        global_vars.update_var("appId", appId)  # 更新appId变量的值 
    if appToken is not None:
        global_vars.update_var("appToken", appToken)  # 更新appToken变量的值 
    if apiVersion is not None:
        global_vars.update_var("apiVersion", apiVersion)  # 更新apiVersion变量的值  
    
    print(colored(f"projectHome:  {global_vars.projectHome}", 'green')) 
    print(colored(f"specHome:  {global_vars.specHome}", 'green'))  


# 初始化项目工程
def init_project():
    url_prefix = global_vars.assistantToolsUrl 
    path = "/init"
    url = "/".join([url_prefix.rstrip("/"), path.lstrip("/")])  

    payload = json.dumps({
        "projectHome": global_vars.projectHome,
        "appId": global_vars.appId,
        "appToken": global_vars.appToken,
        "apiVersion": global_vars.apiVersion
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200 and response.json()['success'] == True:
        global_vars.update_var("srcHome", response.json()['srcHome'])  # 更新srcHome变量的值 
        global_vars.update_var("basePackageName", response.json()['basePackageName'])  # 更新basePackageName变量的值
        if set_key(env_path, 'srcHome', global_vars.srcHome)[0]:
            print(colored(f"srcHome:  {global_vars.srcHome}", 'green')) 
        else:
            print(colored(f"srcHome: {global_vars.srcHome} set_env error", 'red'))
            raise BaseException
        print(colored(f"basePackageName:  {global_vars.basePackageName}", 'green'))
        return True
    else:
        return False


# 开发服务入口
def generate_impl():
    url_prefix = global_vars.assistantToolsUrl
    path = "/generate"
    url = "/".join([url_prefix.rstrip("/"), path.lstrip("/")])  

    payload = json.dumps({
        "specHome": global_vars.specHome,
        "srcHome": global_vars.srcHome,
        "basePackageName": global_vars.basePackageName
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200 and response.json()['success'] == True:
        global_vars.update_var("pomHome", response.json()['pomHome'])  # 更新pomHome变量的值 
        if response.json()['data']:
            # TODO 批量时拆出来做生成器
            for item in response.json()['data']:
                if item["success"] and item["dtoPath"] and item["serviceImplName"]:
                    global_vars.update_var("apiId", item['apiId'])  # 更新apiId变量的值
                    global_vars.update_var("dtoPath", item['dtoPath'])  # 更新dtoPath变量的值
                    global_vars.update_var("serviceImplName", item['serviceImplName'])  # 更新serviceImplName变量的值
                    implpath_prefix = global_vars.basePackageName
                    implpath_prefix = implpath_prefix.replace('.', '\\')
                    global_vars.serviceImplPath = os.path.join(implpath_prefix, global_vars.serviceImplPath)  
                    # TODO 新增global_vars.apiIdList
                    
                    print("生成服务入口\n")
                else:
                    error = item["errorMessage"]
                    print(colored(f"step2服务生成错误: {error}", 'red'))
                    raise BaseException
        else:
            print(colored(f"step2服务生成data为空?", 'red'))
            raise BaseException

        if set_key(env_path, 'apiId', global_vars.apiId)[0]:
            print(colored(f"apiId:  {global_vars.apiId}", 'green')) 
        else:
            print(colored(f"apiId: {global_vars.apiId} set_env error", 'red'))
            raise BaseException
        
        if set_key(env_path, 'dtoPath', global_vars.dtoPath)[0]:
            print(colored(f"dtoPath:  {global_vars.dtoPath}", 'green')) 
        else:
            print(colored(f"dtoPath: {global_vars.dtoPath} set_env error", 'red'))
            raise BaseException
        
        if set_key(env_path, 'serviceImplPath', global_vars.serviceImplPath)[0]:
            print(colored(f"serviceImplPath:  {global_vars.serviceImplPath}", 'green')) 
        else:
            print(colored(f"serviceImplPath: {global_vars.serviceImplPath} set_env error", 'red'))
            raise BaseException
        
        if set_key(env_path, 'serviceImplName', global_vars.serviceImplName)[0]:
            print(colored(f"serviceImplName:  {global_vars.serviceImplName}", 'green')) 
        else:
            print(colored(f"serviceImplName: {global_vars.serviceImplName} set_env error", 'red'))
            raise BaseException
        
        if set_key(env_path, 'pomHome', global_vars.pomHome)[0]:
            print(colored(f"pomHome:  {global_vars.pomHome}", 'green')) 
        else:
            print(colored(f"pomHome: {global_vars.pomHome} set_env error", 'red'))
            raise BaseException
        
        return True
    else:
        return False


def flowrun():
    spec_home = env_vars.get("specHome")
    spec_list = os.listdir(spec_home)
    if not spec_list:
        error = f"规格文档目录下没存放规格文件,请检查规格目录{spec_home}"
        print(colored(error, 'red'))
        raise BaseException
    if len(spec_list) > 1:
        error = f"规格文档目录下超过了1份规格文件,目前不支持批量生成,请检查规格目录{spec_home}"
        print(colored(error, 'red'))
        raise BaseException
    

    print(colored("创建项目工程=======>", 'yellow'))
    init_env()
    step1_res = init_project()
    if step1_res:
        print(colored(">=======创建项目工程完成\n", 'green'))
    else:
        print(colored(">=======创建项目工程失败\n", 'red'))

    
    print(colored("开发服务入口=======>", 'yellow'))
    step2_res = generate_impl()
    if step2_res:
        print(colored(">=======开发服务入口完成\n", 'green'))
    else:
        print(colored(">=======开发服务入口失败\n", 'red'))   

    
    print(colored("开发处理逻辑=======>", 'yellow'))
    from .apidev import read_excel_to_get_content, code
    # 获取规格中【处理逻辑】内容
    excel_name = os.path.join(spec_home, spec_list[0])
    print(excel_name)
    task_content = read_excel_to_get_content(excel_name)
    # 代码生成
    code(task=task_content)
    print(colored(">=======开发处理逻辑完成\n", 'green'))

    print(colored(f'digi-service: {{"name":"{global_vars.apiId}"}}', 'green'))


if __name__ == "__main__":
    flowrun()
