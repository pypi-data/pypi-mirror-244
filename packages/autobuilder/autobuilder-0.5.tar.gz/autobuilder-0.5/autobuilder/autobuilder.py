import os
thisFile = os.path.realpath(__file__)
packageFolder = os.path.dirname(thisFile)
package = os.path.basename(packageFolder)
if os.getcwd() != packageFolder:
    os.chdir(packageFolder)
configFile = os.path.join(packageFolder, "config.py")
if not os.path.isfile(configFile):
    open(configFile, "a", encoding="utf-8").close()
from autobuilder import config

from autobuilder.health_check import HealthCheck
if not hasattr(config, "openaiApiKey") or not config.openaiApiKey:
    HealthCheck.setBasicConfig()
    HealthCheck.changeAPIkey()
    HealthCheck.saveConfig()
    print("Updated!")
HealthCheck.checkCompletion()

#from autogen.agentchat.contrib.agent_builder import AgentBuilder
from autobuilder.agent_builder import AgentBuilder
import autogen, os, json, traceback, re, datetime
from pathlib import Path
from urllib.parse import quote
#from autobuilder.utils.prompts import Prompts
#from prompt_toolkit.styles import Style
#from prompt_toolkit import PromptSession
#from prompt_toolkit.history import FileHistory
if not hasattr(config, "group_chat_max_round"):
    config.group_chat_max_round = 12

# Reference: https://microsoft.github.io/autogen/docs/reference/agentchat/contrib/agent_builder
class AutoGenBuilder:

    def __init__(self):
        #config_list = autogen.get_config_list(
        #    [config.openaiApiKey], # assume openaiApiKey is in place in config.py
        #    api_type="openai",
        #    api_version=None,
        #)
        oai_config_list = []
        for model in ("gpt-4-1106-preview", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"):
            oai_config_list.append({"model": model, "api_key": config.openaiApiKey})
        os.environ["OAI_CONFIG_LIST"] = json.dumps(oai_config_list)

    def getSavePath(self, title=""):
        package = os.path.basename(packageFolder)
        preferredDir = os.path.join(os.path.expanduser('~'), package)
        if os.path.isdir(preferredDir):
            folder = preferredDir
        elif config.startupdirectory:
            folder = config.startupdirectory
        else:
            folder = os.path.join(packageFolder, "files")
        folder = os.path.join(folder, "autogen", "builder")
        Path(folder).mkdir(parents=True, exist_ok=True)
        if title:
            title = "_" + quote(title, safe="")
        currentTime = re.sub("[\. :]", "_", str(datetime.datetime.now()))
        return os.path.join(folder, f"{currentTime}{title}.json")

    def getResponse(self, task, title=""):

        config_list = autogen.config_list_from_json(
            env_or_file="OAI_CONFIG_LIST",  # or OAI_CONFIG_LIST.json if file extension is added
            filter_dict={
                "model": {
                    'gpt-4-1106-preview',
                }
            }
        )
        llm_config={
            #"cache_seed": 42,  # seed for caching and reproducibility
            "config_list": config_list,  # a list of OpenAI API configurations
            "temperature": config.chatGPTApiTemperature,  # temperature for sampling
            "timeout": 300,
        }  # configuration for autogen's enhanced inference API which is compatible with OpenAI API

        builder = AgentBuilder(
            #config_path=config_path,
            builder_model='gpt-4-1106-preview',
            agent_model='gpt-4-1106-preview'
        )

        #building_task = "Find a paper on arxiv by programming, and analysis its application in some domain. For example, find a latest paper about gpt-4 on arxiv and find its potential applications in software."
        #execution_task="Find a recent paper about gpt-4 on arxiv and find its potential applications in software."
        #agent_list, agent_configs = builder.build(building_task, llm_config, coding=True)
        
        building_task = execution_task = task
        agent_list, _ = builder.build(building_task, llm_config, coding=True)

        group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=config.group_chat_max_round)
        manager = autogen.GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": config_list, **llm_config},
        )
        agent_list[0].initiate_chat(manager, message=execution_task)

        # save building config
        builder.save(self.getSavePath(title))
        #clear all agents
        builder.clear_all_agents(recycle_endpoint=True)

    def run(self):
        self.print(f"AutoGen Builder launched!")
        self.print("[press 'ctrl+q' to exit]")
        while True:
            self.print(f"Hi! I am ready for a new task.")
            self.print(f"Please specify a task below:")
            task = input(">>> ")
            if task == config.exit_entry:
                break
            try:
                self.getResponse(task)
            except:
                self.print(traceback.format_exc())
                break
        self.print(f"\n\nAutoGen Builder closed!")


    def print(self, message):
        print(message)
        #print_formatted_text(HTML(message))

def main():
    AutoGenBuilder().run()

if __name__ == '__main__':
    main()