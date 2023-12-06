# autobuilder

A simple auto builder to build a group of AI assistants for task execution. It is built on [AutoGen framework](https://microsoft.github.io/autogen/docs/Getting-Started/), particularly https://github.com/microsoft/autogen/blob/main/autogen/agentchat/contrib/agent_builder.py

It is a simplified version of the "autobuilder" tool, integrated in our [LetMeDoIt AI project](https://github.com/eliranwong/letmedoit)

# Install

> pip install autobuilder

# Usage

Import as a module

```
from autobuilder import AutoGenBuilder
AutoGenBuilder().getResponse("write a dummpy PySide6 app")
```

CLI options:

> autobuilder

> autobuilder -h

> autobuilder "write a dummpy PySide6 app" # specify a task

> autobuilder -c "saved_building_config.json" # load saved building config file

> autobuilder -a 5 # specify the maximum number of agents

> autobuilder -r 12 # specify the maximum round of group chat

> autobuilder -o true # enable OpenAI Assistant API

> autobuilder -o false # disable OpenAI Assistant API
