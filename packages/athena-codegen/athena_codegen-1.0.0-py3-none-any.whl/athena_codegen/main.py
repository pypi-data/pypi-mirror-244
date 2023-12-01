from dotenv import set_key 
from pathlib import Path  
import warnings
try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x
warnings.filterwarnings("ignore")


def start(inputdir:str, outputdir:str, appid:str, llm:str, toolurl:str):
    current_file = Path(__file__).resolve()  
    current_dir = current_file.parent
    env_path = current_dir / '.env' 

    if inputdir is None or outputdir is None:
        print(colored("命令参数inputdir和outputdir必需", 'red'))
        raise BaseException
    else:
        if set_key(env_path, 'specHome', inputdir)[0]:
            print(colored(f"inputdir规格目录:  {inputdir}", 'green')) 
        else:
            print(colored(f"specHome: {inputdir} set_env error", 'red'))
            raise BaseException
        
        if set_key(env_path, 'projectHome', outputdir)[0]:
            print(colored(f"outputdir输出目录:  {outputdir}", 'green')) 
        else:
            print(colored(f"projectHome: {outputdir} set_env error", 'red'))
            raise BaseException

    if appid:
        if set_key(env_path, 'appId', appid)[0]:
            print(colored(f"项目名称id:  {appid}", 'green')) 
        else:
            print(colored(f"appid: {appid} set_env error", 'red'))
            raise BaseException
    if llm:
        if set_key(env_path, 'LLM', llm)[0]:
            print(colored(f"LLM:  {llm}", 'green')) 
        else:
            print(colored(f"LLM: {llm} set_env error", 'red'))
            raise BaseException
    if toolurl:
        if set_key(env_path, 'assistantToolsUrl', toolurl)[0]:
            print(colored(f"assistantToolsUrl:  {toolurl}", 'green')) 
        else:
            print(colored(f"assistantToolsUrl: {toolurl} set_env error", 'red'))
            raise BaseException

    from .flow import flowrun
    flowrun()
    print(colored("\nCompleted\n", 'green'))


if __name__ == "__main__":
    import argparse
    # 创建解析器
    parser = argparse.ArgumentParser()
    # 添加参数
    parser.add_argument('--inputdir', help='输入的规格存放目录')
    parser.add_argument('--outputdir', help='输出的项目工程存放目录')
    parser.add_argument('--appid', help='项目名称')
    parser.add_argument('--llm', help='Azure GPT模型')
    parser.add_argument('--toolurl', help='assistantToolsUrl地址,ip+port,like "http://127.0.0.1:8085"')
    # 解析命令行参数
    args = parser.parse_args()

    inputdir = args.inputdir
    outputdir = args.outputdir
    appid = args.appid if args.appid else 'dap-demo'
    llm = args.llm if args.llm else 'GPT4'
    # toolurl = "http://"+socket.gethostbyname(socket.gethostname())+":8085"
    toolurl = args.toolurl if args.llm else 'http://localhost:8085'

    start(inputdir, outputdir, appid, llm, toolurl)
