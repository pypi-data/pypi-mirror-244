# glow
The glow command line interface.

[![PyPI version](https://img.shields.io/pypi/v/glow-cli)](https://pypi.org/project/glow-cli/)
[![📦 pypi](https://github.com/loopsocial/glow/actions/workflows/publish.yml/badge.svg)](https://github.com/loopsocial/glow/actions/workflows/publish.yml) 

```
   ________    ____ _       __
  / ____/ /   / __ \ |     / /
 / / __/ /   / / / / | /| / /
/ /_/ / /___/ /_/ /| |/ |/ /
\____/_____/\____/ |__/|__/
____________________________
__________________________________
________________________________________
```

## 📦 Installation
```shell
pip install glow-cli
```

If you want to use one of the lmm sdk
```shell
pip install "glow-cli[openai]"
```

You can set up configuration in `~/.glow/commands/<task>.yml`

## 🚀 Usage

```shell
g list
```

## 🦋 Templating
Say you set up a config at "./commands/pod-shell.yml"
```yaml
description: |
  Entering the shell of the 1st pod that matches the keyword
command: |
  kubectl exec -it $(kubectl get pods | grep { kw } | head -n 1 | awk '{print $1}') -- /bin/bash
inputs:
  kw:
    description: keyword to match
    type: str
```

you can run the command with:
```shell
g ./commands/pod-shell.yml --kw "app1"
```

Or you can store the configuration by
```shell
g install ./commands/pod-shell.yml
```

Then you can run the command with:
```shell
g pod-shell --kw "app1"
```

## 🦙 LLM in CLI 💻
> Why memorize commands when you can just ask?

You can setup the environment variables in the following file: eg, with `OPENAI_API_KEY`:

```
~/.glow/.env
```

Then you can try:
```shell
g code "redub a.mp4 file with b.mp3, save to c.mp4 with fps 12"
```

Or you can ask things in general:
```shell
g llm "explain btree to me"
```

Or with certain flavor to the robot role
```shell
g llm "explain btree to me" "you are a poet return everything in homer style"
```

### ✨ combine with other commands
Here's some good use cases to combine with other commands
```shell
g code "shell into one of the pods: $(kubectl get pods) with keyword app1"
```

```shell
g llm "please summarize the commit message for $(git diff)"
```

```shell
g llm "can you explain the structure of this folder: $(ls -l)"
```