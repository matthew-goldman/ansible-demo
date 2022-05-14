#!/usr/bin/env python3


"""
The purpose of this script is to force the re-installation of roles
locally installed if its version differs from the one declared in 
requirements.yml. This was created because the 'ansible-galaxy'
command does not provide a way of doing this.
"""

import os
import sys
import subprocess
import argparse
import yaml
from packaging import version
from termcolor import cprint


COLOR_WARNING = "yellow"
COLOR_OK = "green"


def requirements_reader(requirements_file):
    """
    Reads the requirements file passed as parameter and
    returns the content of it.
    """
    content = []
    try:
        with open(requirements_file, "r") as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError:
        raise yaml.YAMLError("Invalid yaml syntax in requirements file")
    except FileNotFoundError:
        raise FileNotFoundError("Requirements file does not exists!")
    return content


def get_installed_version(path, name):
    """
    Given the path where content is being installed and the name,
    returns the version of it
    """
    version = None
    role_galaxy_info = os.path.join(path, name, 'meta', '.galaxy_install_info')
    try:
        with open(role_galaxy_info, "r") as f:
            meta_file = yaml.load(f, Loader=yaml.FullLoader)
            version = meta_file['version']
    except yaml.YAMLError:
        raise yaml.YAMLError("Invalid yaml syntax in role file")
    except FileNotFoundError:
        pass
    return version


def get_required_version(requirements, name):
    """
    Returns the version declared in the requirements file for a
    given name.
    """
    version = None
    for item in requirements:
        if item['name'] == name:
            try:
                version = item['version']
            except KeyError:
                pass
    return version


def is_installed(path, name):
    """
    Checks if a role is installed.
    """
    installed = False
    if os.path.isdir(os.path.join(path, name)):
        installed = True
    return installed


def install(path, resource):
    """
    Installs the required role by calling ansible-galaxy command
    with force flag.
    """
    success = False
    command = "ansible-galaxy install --force -p {} ".format(path)
    parameters = "{},{}".format(resource['name'], resource['version'])
    if resource.get('src'):
        parameters = "{},{},{}".format(resource['src'],
                                       resource['version'],
                                       resource['name'])
    try:
        execution = subprocess.check_output([command + parameters], shell=True)
        success = True
    except subprocess.CalledProcessError as e:
        raise Exception("Something went wrong when executing ansible-galaxy: stdout={}, rc={}"
                        .format(e.stdout, e.returncode))
    return success


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--requirements",
                    help="A file containing a list of roles requirements.",
                    type=str, default='roles/requirements.yml')
parser.add_argument("-p", "--path",
                    help="The path to the directory containing the roles.",
                    type=str, default='roles/')
parser.add_argument("-i", "--info",
                    help="If declared, the script will only inform about roles to be \
                    changed without performing any action.",
                    default=False, action="store_true")
args = parser.parse_args()


if __name__ == '__main__':
    action = False
    requirements = requirements_reader(args.requirements)
    if requirements:
        for item in requirements:
            required_version = get_required_version(requirements, item['name'])
            installed_version = get_installed_version(args.path, item['name'])
            if is_installed(args.path, item['name']):
                if required_version and installed_version:
                    if (version.parse(installed_version) !=
                            version.parse(required_version)):
                        if args.info:
                            cprint("Role {0} to be changed from '{1}' to '{2}'!"
                                   .format(item['name'],
                                           installed_version,
                                           required_version), COLOR_WARNING)
                        else:
                            if install(args.path, item):
                                cprint("Role {0} version changed successfuly!"
                                       .format(item['name']), COLOR_OK)
                        action = True
                else:
                    cprint("Role {0} has no version declared! Skipping..."
                           .format(item['name']), COLOR_WARNING)
            else:
                cprint("Role {0} not installed! Install it first. Skipping..."
                       .format(item['name']), COLOR_WARNING)
    else:
        cprint("Requirements file is empty! Exiting...", COLOR_WARNING)
        sys.exit(1)

if not action:
    cprint("No roles to update!", COLOR_OK) 
