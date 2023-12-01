from typing import Callable, Dict, Union
from autogen.agentchat.agent import Agent
from .prompt.code_sys import admin_sys, coder_sys, code_initiate_mess
from .prompt.plan_sys import user_sys, plan_init_sys, dispatcher_sys, critic_sys
from .tools.save_code import extract_code, save_code_blocks, colored
from .tools.compile import compile_error
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv  
from pathlib import Path  
import warnings
warnings.filterwarnings("ignore")

current_file = Path(__file__).resolve()  
current_dir = current_file.parent
env_path = current_dir / '.env' 
load_dotenv(dotenv_path=env_path, verbose=True)  

if os.getenv('COST', False):
    from .tools.customagent.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
else:
    from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

config_list = [
    {
        'model': os.getenv('LLM', 'GPT4'), 
        'api_key': '42267778dbec4aa6b73176b0951a2a90', 
        'api_base': 'https://digiwinai2.openai.azure.com', 
        'api_type': 'azure', 
        'api_version': '2023-07-01-preview'
    }
]

SEED = os.getenv('SEED')
WORKDIR = os.getenv('srcHome', os.path.join(os.getcwd(), "extensions"))

llm_config={
    "seed": SEED,
    "config_list": config_list,
    "request_timeout": 600,
    "temperature": 0,
}

class SaveableAssistantAgent(AssistantAgent):
    def __init__(
        self, 
        name: str, 
        system_message: str | None = ..., 
        llm_config: Dict | bool | None = None, 
        is_termination_msg: Callable[[Dict], bool] | None = None, 
        max_consecutive_auto_reply: int | None = None, 
        human_input_mode: str | None = "NEVER", 
        code_execution_config: Dict | bool | None = False, 
        work_dir: str = None,
        **kwargs
    ):
        self.work_dir = work_dir
        super().__init__(name, system_message, llm_config, is_termination_msg, max_consecutive_auto_reply, human_input_mode, code_execution_config, **kwargs)

    def _message_to_str(self, message: Union[Dict, str]):
        if isinstance(message, Dict):
            return message.get('content','')
        else:
            return message

    def send(self, message: Dict | str, recipient: Agent, request_reply: bool | None = None, silent: bool | None = False) -> bool:
        message_content = self._message_to_str(message)
        extracted = extract_code(message_content)
        if extracted:
            print(colored("代码保存"+self.name, "green"))
            exitcode, logs = save_code_blocks(extracted, self.work_dir)
            if not exitcode:
                print(colored(logs, "green"))
            else:
                message = message_content + '\n代码中可能存在错误,请指出这个错误给我修正' + logs
                print(colored(logs, "red"))
            print('==================')
        return super().send(message, recipient, request_reply, silent)



llm_config_code={
    "seed": SEED,
    "config_list": config_list,
    "request_timeout": 600,
    "temperature": 0.2,
}


def read_excel_to_get_content(excel_name):
    # 读取Excel文件
    data = pd.read_excel(excel_name,sheet_name=5,dtype=str)
    all_data=list(np.array(data.fillna('')))
    all_content=''
    # global add_str
    key_flag=0
    for i in range(len(all_data)):
        all_data_contact='\t'.join(all_data[i])
        if "處理邏輯" in all_data_contact or "处理逻辑" in all_data_contact:
            key_flag=i
            break
    for content_i in range(key_flag,len(all_data)):
        new_lst = list(filter(lambda x: x != '', all_data[content_i]))
        if len(new_lst)==1:
            add_str=new_lst[0]+'\n'
            all_content += add_str
        if len(new_lst)>1:
            add_str='\t'.join(all_data[content_i])+'\n'
            all_content += add_str
    return all_content

def code(task):
    coder = SaveableAssistantAgent(
        name="coder",
        system_message=coder_sys,
        is_termination_msg=lambda x: x.get("content", "") and x.get(
            "content", "").rstrip().endswith("TERMINATE"),
        llm_config=llm_config_code,
        work_dir=WORKDIR
    )

    code_admin = UserProxyAgent(
        name="code_admin",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config=False,
        is_termination_msg=lambda x: x.get("content", "") and x.get(
            "content", "").rstrip().endswith("TERMINATE"),
        llm_config=llm_config,
        system_message=admin_sys,
    )

    coder_ini = code_initiate_mess()
    #消息交换机制部分  重点
    code_admin.initiate_chat(
        coder, message=coder_ini+f"\n编写Java代码完成任务: {task},仅实现该任务,请勿发散修改任务内容.")

    code_admin.stop_reply_at_receive(coder)

    # 循环执行基于编译结果优化代码
    for _ in range(5):
        complie_message = compile_error()
        if complie_message:
            code_admin.send(f"请你根据以下错误信息\t{complie_message}\t修改优化代码,输出代码必须完整,包括所有导包",coder)
        else:
            break

    code_admin.send(
        "Evaluate task completion based on goals, reply whether it is completed or failed, and add TERMINATE to the end of the message", coder)

    subtask_code = code_admin.last_message()["content"]

    return subtask_code

llm_config_dispatcher = {
    "seed": SEED,
    "config_list": config_list,
    "request_timeout": 600,
    "temperature": 0,
    "functions": [
        {
            "name": "code",
            "description": "Distribute a task and complete the task using java code",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "要实现的任务需求完整描述，任务需求描述必须完整",
                        }
                    },
                "required": ["task"],
            },
        },
    ]
}


planner = AssistantAgent(
    name="planner",
    llm_config={"config_list": config_list,"seed": SEED,"temperature": 0.2,},
    system_message=plan_init_sys,
    # work_dir=WORKDIR
)

dispatcher = AssistantAgent(
    name="dispatcher",
    llm_config=llm_config_dispatcher,
    system_message=dispatcher_sys,    
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=30,
    code_execution_config=False,
    is_termination_msg=lambda x: x.get("content", "") and x.get(
            "content", "").rstrip().endswith("TERMINATE"),
    llm_config=llm_config,
    system_message=user_sys,
    function_map={
        "code": code
    } 
)

# 创建 组 groupchat
groupchat = GroupChat(
    agents=[user_proxy, planner, dispatcher], messages=[])
manager = GroupChatManager(groupchat=groupchat, name="main plan", llm_config=llm_config)


if __name__ == "__main__":
    spec_home = os.getenv("specHome")
    spec_list = os.listdir(spec_home)
    if not spec_list:
        error = f"规格文档目录下没存放规格文件,请检查规格目录{spec_home}"
        print(colored(error, 'red'))
        raise BaseException
    if len(spec_list) > 1:
        error = f"规格文档目录下超过了1份规格文件,目前不支持批量生成,请检查规格目录{spec_home}"
        print(colored(error, 'red'))
        raise BaseException
    
    excel_name = os.path.join(spec_home, spec_list[0])
    print(excel_name)
    task_content = read_excel_to_get_content(excel_name)
    # print(task_content)

    # 子组执行
    code(task=task_content)

    # 父子组运行
    # user_proxy.initiate_chat(
    #     manager,
    #     message=task
    # )