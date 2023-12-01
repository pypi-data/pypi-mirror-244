from autogen import ConversableAgent
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from autogen import oai
from autogen.agentchat.agent import Agent
from collections import defaultdict

try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x

all_token_take = 0

class CustomConversableAgent(ConversableAgent):
    def __init__(
        self, 
        name: str,
        system_message: Optional[str] = "You are a helpful AI Assistant.",
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "TERMINATE",
        function_map: Optional[Dict[str, Callable]] = None,
        code_execution_config: Optional[Union[Dict, bool]] = None,
        llm_config: Optional[Union[Dict, bool]] = None,
        default_auto_reply: Optional[Union[str, Dict, None]] = "",
    ):
        self._name = name
        self._oai_messages = defaultdict(list)
        self._oai_system_message = [{"content": system_message, "role": "system"}]
        self._is_termination_msg = (
            is_termination_msg if is_termination_msg is not None else (lambda x: x.get("content") == "TERMINATE")
        )
        if llm_config is False:
            self.llm_config = False
        else:
            self.llm_config = self.DEFAULT_CONFIG.copy()
            if isinstance(llm_config, dict):
                self.llm_config.update(llm_config)

        self._code_execution_config = {} if code_execution_config is None else code_execution_config
        self.human_input_mode = human_input_mode
        self._max_consecutive_auto_reply = (
            max_consecutive_auto_reply if max_consecutive_auto_reply is not None else self.MAX_CONSECUTIVE_AUTO_REPLY
        )
        self._consecutive_auto_reply_counter = defaultdict(int)
        self._max_consecutive_auto_reply_dict = defaultdict(self.max_consecutive_auto_reply)
        self._function_map = {} if function_map is None else function_map
        self._default_auto_reply = default_auto_reply
        self._reply_func_list = []
        self.reply_at_receive = defaultdict(bool)
        self.register_reply([Agent, None], CustomConversableAgent.generate_oai_reply)
        self.register_reply([Agent, None], CustomConversableAgent.generate_code_execution_reply)
        self.register_reply([Agent, None], CustomConversableAgent.generate_function_call_reply)
        self.register_reply([Agent, None], CustomConversableAgent.check_termination_and_human_reply)

    def generate_oai_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[Any] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """Generate a reply using autogen.oai."""
        llm_config = self.llm_config if config is None else config
        if llm_config is False:
            return False, None
        if messages is None:
            messages = self._oai_messages[sender]

        # TODO: #1143 handle token limit exceeded error
        response = oai.ChatCompletion.create(
            context=messages[-1].pop("context", None), messages=self._oai_system_message + messages, **llm_config
        )

        # TODO: 计算总token数和费用
        global all_token_take
        tokens = response.get("usage", {})
        takes = response.get("cost", 0)
        print(colored(f"{self.name}本次token: {tokens}", "green"))
        print(colored(f"{self.name}本次费用: {takes}", "green"))
        all_token_take += response.get("cost", 0)
        print(colored(f"总费用: {all_token_take}", "red"))

        return True, oai.ChatCompletion.extract_text_or_function_call(response)[0]
     