"""OS env and shell utils"""

import json
import os
import subprocess

from pathlib import Path

from .colors import colored
from .logs import logger
from .dicts import CaseInsensitiveDict


class OSEnver:
    def __init__(self, secrets_json=None):
        if not secrets_json:
            self.secrets_json = Path(__file__).parent / "secrets.json"
        else:
            self.secrets_json = secrets_json
        self.load_secrets()

    def load_secrets(self):
        self.secrets = CaseInsensitiveDict()
        try:
            with open(self.secrets_json, mode="r", encoding="utf-8") as rf:
                secrets = json.load(rf)
                for key, value in secrets.items():
                    self.secrets[key] = value
        except Exception as e:
            logger.warn(f"Loading local secrets: {e}")

    def __getitem__(self, key=None):
        if key:
            return self.secrets.get(key, os.getenv(key, None))
        else:
            return dict(self.secrets.items())


def shell_cmd(cmd, getoutput=False, showcmd=True, env=None, sudo=False):
    """Run a shell command.

    Args:
        cmd: The command to run.
        getoutput: If True, return command output as string.
        showcmd: If True, log the command before running.
        env: Environment variables for the subprocess.
        sudo: If True, run with root privileges. Auto-detects mode:
            - Already root (euid==0): run as-is, no sudo needed.
            - SUDOPASS env set: pipe password to `sudo -S` each time.
            - Otherwise: prepend `sudo` (may prompt for password).
    """
    # Handle sudo privilege escalation
    use_sudo_s = False
    sudopass = ""
    if sudo and os.geteuid() != 0:
        sudopass = os.environ.get("SUDOPASS", "")
        if sudopass:
            cmd = f"sudo -S {cmd}"
            use_sudo_s = True
        else:
            cmd = f"sudo {cmd}"

    if showcmd:
        logger.info(colored(f"\n$ [{os.getcwd()}]", "light_blue"))
        logger.info(colored(f"  $ {cmd}\n", "light_cyan"))

    if use_sudo_s:
        # Pipe SUDOPASS to sudo -S via stdin
        if getoutput:
            result = subprocess.run(
                cmd,
                shell=True,
                text=True,
                input=sudopass + "\n",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            return result.stdout
        else:
            subprocess.run(
                cmd,
                shell=True,
                text=True,
                input=sudopass + "\n",
                env=env,
            )
    else:
        if getoutput:
            output = subprocess.getoutput(cmd)
            return output
        else:
            subprocess.run(cmd, shell=True, env=env)
