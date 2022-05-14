#!/usr/bin/env python3

import os
import sys


def env_password():
    """Reads the password from the environment variable 'VAULT_PASSWORD'"""
    return os.environ.get("VAULT_PASSWORD", None)


def file_password(path):
    """Reads the password from the file .ansible_vault_credentials in the path passed as parameter""" 
    file = os.path.join(os.path.expanduser(path), ".ansible_vault_credentials")
    if os.path.isfile(file):
        with open(file) as f:
            return f.read().rstrip()
    else:
        return None


if __name__ == "__main__":
    env_pwd = env_password()
    file_pwd = file_password('~')
    if env_pwd:
        print(env_pwd, end="")
    elif file_pwd:
        print(file_pwd, end="")
    else:
        print("Unable to find the Vault Password!", file=sys.stderr)
        sys.exit(1)
