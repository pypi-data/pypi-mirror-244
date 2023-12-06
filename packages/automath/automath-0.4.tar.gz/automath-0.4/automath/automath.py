import os
thisFile = os.path.realpath(__file__)
packageFolder = os.path.dirname(thisFile)
package = os.path.basename(packageFolder)
if os.getcwd() != packageFolder:
    os.chdir(packageFolder)
configFile = os.path.join(packageFolder, "config.py")
if not os.path.isfile(configFile):
    open(configFile, "a", encoding="utf-8").close()
from automath import config

from automath.health_check import HealthCheck
if not config.openaiApiKey:
    HealthCheck.changeAPIkey()
    HealthCheck.saveConfig()
    print("Updated!")
HealthCheck.checkCompletion()

import autogen, os, json, traceback
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
from autogen import config_list_from_json
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent


class AutoGenMath:

    def __init__(self):
        oai_config_list = []
        for model in ("gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"):
            oai_config_list.append({"model": model, "api_key": config.openaiApiKey})
        os.environ["OAI_CONFIG_LIST"] = json.dumps(oai_config_list)

    def getResponse(self, math_problem):
        config_list = autogen.config_list_from_json(
            env_or_file="OAI_CONFIG_LIST",  # or OAI_CONFIG_LIST.json if file extension is added
            filter_dict={
                "model": {
                    config.chatGPTApiModel,
                }
            }
        )

        # reference https://microsoft.github.io/autogen/docs/reference/agentchat/contrib/math_user_proxy_agent
        # 1. create an AssistantAgent instance named "assistant"
        assistant = autogen.AssistantAgent(
            name="assistant", 
            system_message="You are a helpful assistant.",
            llm_config={
                #"cache_seed": 42,  # seed for caching and reproducibility
                "config_list": config_list,  # a list of OpenAI API configurations
                "temperature": config.chatGPTApiTemperature,  # temperature for sampling
                "timeout": 600,
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )

        # 2. create the MathUserProxyAgent instance named "mathproxyagent"
        # By default, the human_input_mode is "NEVER", which means the agent will not ask for human input.
        mathproxyagent = MathUserProxyAgent(
            name="mathproxyagent",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
        )

        mathproxyagent.initiate_chat(assistant, problem=math_problem)

    def print(self, message):
        #print(message)
        print_formatted_text(HTML(message))

    def run(self):
        print("AutoGen Math launched!")
        print("[press 'ctrl+q' to exit]")
        while True:
            print("New session started!")
            print("Enter a math problem below:")
            math_problem = prompt()
            if math_problem == config.exit_entry:
                break
            try:
                self.getResponse(math_problem)
            except:
                print(traceback.format_exc())
                break
        print("\n\nAutoGen Math closed!")

def main():
    AutoGenMath().run()

if __name__ == '__main__':
    main()