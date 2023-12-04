import getpass
import os
from pathlib import Path

import yaml

from glow.colors import cprint, mask_print
from glow.constants import ASCII_ART, GLOW_SECRETS_FILE
from glow.utils.yaml import open_yaml_conf


GLOW_SECRETS = dict()


def load_secrets(glow_secrets_file: str = GLOW_SECRETS_FILE):
    """
    Load all the secrets
    """
    if not Path(glow_secrets_file).exists():
        Path(glow_secrets_file).parent.mkdir(parents=True, exist_ok=True)
        return {}
    yaml_conf = open_yaml_conf(str(glow_secrets_file))
    for name, item in yaml_conf["secrets"].items():
        item_value = item["value"]
        os.environ[name] = f"{item_value}"
        GLOW_SECRETS[name] = f"{item_value}"
    return GLOW_SECRETS


def update_env(name: str, value: str, glow_secrets_file: str = GLOW_SECRETS_FILE):
    if not Path(glow_secrets_file).exists():
        Path(glow_secrets_file).parent.mkdir(parents=True, exist_ok=True)
        yaml_conf = {"secrets": {}}
    else:
        yaml_conf = open_yaml_conf(str(glow_secrets_file))
        if yaml_conf is None:
            yaml_conf = {"secrets": {}}

    if name in yaml_conf["secrets"]:
        yaml_conf["secrets"][name] = value
    else:
        yaml_conf["secrets"][name] = {
            "name": name,
            "value": value,
        }
    GLOW_SECRETS[name] = value

    # writing it back to the file
    with open(glow_secrets_file, "w") as f:
        f.write(yaml.dump(yaml_conf))


def remove_key(name: str, glow_secrets_file: str = GLOW_SECRETS_FILE):
    if not Path(glow_secrets_file).exists():
        Path(glow_secrets_file).parent.mkdir(parents=True, exist_ok=True)
        return {}
    yaml_conf = open_yaml_conf(str(glow_secrets_file))
    if name in yaml_conf["secrets"]:
        del yaml_conf["secrets"][name]
    with open(glow_secrets_file, "w") as f:
        f.write(yaml.dump(yaml_conf))


def secrets_help():
    cprint("✨ GLOW SECRETS", ["green", "bold"])
    cprint(ASCII_ART, ["green"])

    cprint(
        """
    Please use `g secrets add SOME_API_TOKEN` to add a secret

    You can use `g secrets list` to list all the secrets on your local machine

    `g remove SOME_API_TOKEN` to remove a secret
    """,
        ["green"],
    )


def secrets_manage(*args, **data):
    if len(args) == 0 and len(data) == 0:
        secrets_help()
        return

    if args[0].lower() == "get":
        if len(args) == 1:
            cprint("Please input the name of the secret", ["yellow"])
            name = input("🤫 Name: ")
        else:
            name = args[1]
        load_secrets()
        if name in GLOW_SECRETS:
            print(GLOW_SECRETS[name], end="")
            return
        else:
            cprint(f"❌ secret {name} NOT FOUND ✅", ["red"])
            return
    if (args[0].lower() == "list") or "list" in data:
        load_secrets()
        print("🤫 Available secrets:")
        for key, value in GLOW_SECRETS.items():
            cprint(f"  - {key} = {mask_print(value)}", ["cyan"])

    elif (args[0].lower() == "add") or "add" in data:
        # in cases where name wasn't assigned
        if len(args) == 1:
            cprint("Please input the name of the secret", ["yellow"])
            name = input("🤫 Name: ")
        else:
            name = args[1]

        if len(args) <= 2:
            cprint("Please input the value of the secret", ["yellow"])
            value = getpass.getpass("🤫🔑 Value: ")
        else:
            value = args[2]

        update_env(name, value)

        cprint(f"🔑✨ {name} ADDED ✅", ["green"])

    elif (args[0].lower() == "remove") or "remove" in data:
        name = args[1] if len(args) > 1 else data["remove"]
        if name in GLOW_SECRETS:
            del GLOW_SECRETS[name]
        remove_key(name)
        cprint(f"❌ secret {name} REMOVED ✅", ["green"])
        return
    else:
        cprint("🔑 Please specify the action", ["yellow"])

        secrets_help()
        return
