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
if not hasattr(config, "max_agents"):
    config.max_agents = 5
if not hasattr(config, "max_group_chat_round"):
    config.max_group_chat_round = 12
if not hasattr(config, "use_oai_assistant"):
    config.use_oai_assistant = False

from autobuilder.health_check import HealthCheck
if not hasattr(config, "openaiApiKey") or not config.openaiApiKey:
    HealthCheck.setBasicConfig()
    HealthCheck.changeAPIkey()
    HealthCheck.saveConfig()
    print("Updated!")
HealthCheck.checkCompletion()

from autobuilder.agent_builder import AgentBuilder
import autogen, os, json, traceback, re, datetime, argparse
from pathlib import Path
from urllib.parse import quote
#from autobuilder.utils.prompts import Prompts
#from autobuilder.utils.shared_utils import SharedUtil
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
#from prompt_toolkit import PromptSession
#from prompt_toolkit.history import FileHistory

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
        # assign ChatGPT4 to run the builder
        self.chatGPTmodel = "gpt-4-1106-preview"

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

    def getResponse(self, task, title="", load_path=""):
        building_task = execution_task = task

        config_list = autogen.config_list_from_json(
            env_or_file="OAI_CONFIG_LIST",  # or OAI_CONFIG_LIST.json if file extension is added
            filter_dict={
                "model": {
                    self.chatGPTmodel,
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
            #config_path=config_path, # use default
            builder_model=self.chatGPTmodel,
            agent_model=self.chatGPTmodel,
        )

        # e.g.
        #building_task = "Find a paper on arxiv by programming, and analysis its application in some domain. For example, find a latest paper about gpt-4 on arxiv and find its potential applications in software."
        #execution_task="Find a recent paper about gpt-4 on arxiv and find its potential applications in software."
        #agent_list, agent_configs = builder.build(building_task, llm_config, coding=True)
        
        if load_path:
            agent_list, _ = builder.load(load_path)
        else:
            agent_list, _ = builder.build(building_task, llm_config, coding=True, use_oai_assistant=config.use_oai_assistant)

        group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=config.max_group_chat_round)
        manager = autogen.GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": config_list, **llm_config},
        )
        agent_list[0].initiate_chat(manager, message=execution_task)

        # save building config
        if not load_path:
            builder.save(self.getSavePath(title))
        #clear all agents
        builder.clear_all_agents(recycle_endpoint=True)

    def promptTask(self):
        self.print(f"<{config.terminalCommandEntryColor1}>Please specify a task below:</{config.terminalCommandEntryColor1}>")
        return input(">>> ")

    def promptConfig(self):
        self.print("Enter maximum number of agents:")
        max_agents = input(">>> ")
        if max_agents and int(max_agents) > 1:
            config.max_agents = int(max_agents)
        
        self.print("Enter maximum round of group chat:")
        max_group_chat_round = input(">>> ")
        if max_group_chat_round and int(max_group_chat_round) > 1:
            config.max_group_chat_round = int(max_group_chat_round)

        self.print("Do you want to support OpenAI Assistant API (y/yes/N/NO)?")
        userInput = input(">>> ")
        if userInput:
            config.use_oai_assistant = True if userInput.strip().lower() in ("y", "yes") else False
        HealthCheck.saveConfig()

    def run(self):
        self.promptConfig()

        self.print("AutoGen Agent Builder launched!")
        self.print("[press 'ctrl+q' to exit]")
        while True:
            self.print("Hi! I am ready for a new task.")
            task = self.promptTask()
            if task == config.exit_entry:
                break
            try:
                self.getResponse(task)
            except:
                self.print(traceback.format_exc())
                break
        self.print("\n\nAutoGen Agent Builder closed!")


    def print(self, message):
        #print(message)
        print_formatted_text(HTML(message))

def main():
    parser = argparse.ArgumentParser(description="AutoGen Agent Builder cli options")
    # Add arguments
    parser.add_argument("default", nargs="?", default=None, help="execution task")
    parser.add_argument('-c', '--config', action='store', dest='config', help="load building config file")
    parser.add_argument('-a', '--agents', action='store', dest='agents', help="maximum number of agents")
    parser.add_argument('-r', '--round', action='store', dest='round', help="maximum round of group chat")
    parser.add_argument('-o', '--oaiassistant', action='store', dest='oaiassistant', help="support OpenAI Assistant API (true/false)")
    # Parse arguments
    args = parser.parse_args()

    builder = AutoGenBuilder()

    if args.agents:
        try:
            config.max_agents = int(args.agents)
        except:
            config.print2("Integer required for setting number of agents!")

    if args.round:
        try:
            config.max_group_chat_round = int(args.round)
        except:
            config.print2("Integer required for setting round of group chat!")

    if args.oaiassistant:
        config.use_oai_assistant = True if args.oaiassistant.lower() == "true" else False

    if args.config and not os.path.isfile(args.config):
        config.print2(f"'{args.config}' does not exist!")

    if args.config and os.path.isfile(args.config):
        task = args.default if args.default else ""
        if not task:
            task = self.promptTask()
        if task.strip():
            builder.getResponse(task=task.strip(), load_path=args.config)
        else:
            config.print2("Task not specified!")
    elif args.default.strip():
        builder.getResponse(task=args.default.strip())
    else:
        builder.run()

if __name__ == '__main__':
    main()