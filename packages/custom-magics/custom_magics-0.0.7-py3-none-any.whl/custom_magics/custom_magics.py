import base64
import keyword
import os
import re
import sys
import warnings
from typing import Optional
import requests
import json
import click
from IPython import get_ipython
from IPython.core.magic import Magics, line_cell_magic, magics_class, register_cell_magic
from IPython.display import HTML, JSON, Markdown, Math
from IPython.terminal.interactiveshell import TerminalInteractiveShell
# from IPython.config.configurable import Configurable


MODEL_ID_ALIASES = {
    "gpt2": "huggingface_hub:gpt2",
    "gpt3": "openai:text-davinci-003",
    "chatgpt": "openai-chat:gpt-3.5-turbo",
    "gpt4": "openai-chat:gpt-4",
    "titan": "bedrock:amazon.titan-tg1-large",
}

@magics_class
class MyMagics(Magics):

    def __init__(self, shell):
        super().__init__(shell)
        # Configurable.__init__(self, config=shell.config)
        Magics.__init__(self, shell=shell)

        # Add ourselves to the list of module configurable via %config
        self.shell.configurables.append(self)
        self.transcript_openai = []

        # suppress warning when using old OpenAIChat provider
        warnings.filterwarnings(
            "ignore",
            message="You are trying to use a chat model. This way of initializing it is "
            "no longer supported. Instead, please use: "
            "`from langchain.chat_models import ChatOpenAI`",
        )
        # suppress warning when using old Anthropic provider
        warnings.filterwarnings(
            "ignore",
            message="This Anthropic LLM is deprecated. Please use "
            "`from langchain.chat_models import ChatAnthropic` instead",
        )

        # self.providers = get_lm_providers()

        # initialize a registry of custom model/chain names
        self.custom_model_registry = MODEL_ID_ALIASES
    @line_cell_magic
    def data_explore(self, line, cell=None):
        raw_args = line;
        user_ns = self.shell.user_ns
        
        url = 'http://localhost:5000/'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "messages": 
                {
                    "role": "user",
                    "content": "What is the security id for MSFT US? Could you please provide the query to get that?"
                }

        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        data = response.json()
        #print(data)
        return data
    
    """
        This method supports multiline features and its supports all type
        of special character.
    """
    @line_cell_magic
    def cell_explore(self, line, cell):
        raw_args = cell;
        user_ns = self.shell.user_ns

        url = 'http://localhost:5000/'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "messages": 
                {
                    "role": "user",
                    "content": "What is the security id for MSFT US? Could you please provide the query to get that?"
                }

        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        data = response.json()
        return data
    
ip = get_ipython()
ip.register_magics(MyMagics)
