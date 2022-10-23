# n8n Python Virtualenv Manager

The n8n Python Virtual Environment Manager creates virtual environments and run your python scripts in virtual environment with one command. This allows your scripts to run in designated virtual environments in n8n that otherwise do not support persistent python site-package storage or virtual environment. Files saved from your script can also be read and edited by other n8n nodes or other scripts should you choose to do so. 

This packages comes with nano to help edit files and configure scripts from within the container, but you can always edit files in the maped directories from your host system. 

## Table of Contents
- [Installation](#installation)
  - [Build from Source](#build-from-dockerfile)
  - [Start Docker Container](#start-docker-container)
- [Script Setup](#script-setup)
  - [Directory Setup](#directory-setup)
  - [Manager Config](#manager-configuration)
  - [Script Config](#script-configuration)
- [Example Usage](#example-usage)
  - [Configure Script Directory](#configure-script-directory)
  - [Create Virtual Environment for Script](#create-virtual-environment-for-script)
  - [Delete Virtual Environment](#delete-virtual-environment)
  - [Run Script](#run-script)
- [Debugging](#debugging)
  - [Activate Virtual Environment](#activate-virtual-environment)
  - [Dectivate Virtual Environment](#dectivate-virtual-environment)
- [Acknowledgements](#acknowledgements)
- [Future Plans](#future-plans)

# Installation
Install n8n-pyvenv-manager using the n8n-pyvenv-manager [docker](https://www.docker.com/) image. The configuration is as of now command-line based. This assumes you have some fundamental knowledge of unix commands and docker exec.
## Build from Dockerfile
To build docker image from Dockerfile, run
```
docker build . -t n8n-pyvenv-manager
```
## Start Docker Container
To start the n8n docker container with Docker Compose, run
```
docker compose up -d
```
You may need to use ```sudo``` depending on your docker configuration. 
NOTE: this is a modified version of the official docker-compose file with MariaDB 10.9. To run with other databases, see [official documentation](https://github.com/n8n-io/n8n)

# Script Setup
To setup directory structures for your scripts, you may need to access the container console. A docker dashboard, such as [Portainer](https://www.portainer.io/), is recommended. 

## Directory Setup
1. Create a directory for each of your scripts in the /data/pyvenv_scripts directory like so:
   Each Script must be setup in a specific structure so that the manager can recognize the script and configure the virtual environments accordingly. The home directory of pyvenv_manager should look something like this: 
```
<root_path>/                        # root_directory for scripts in persistent n8n storage path
  - <script_1_name>/
    - <script_1_name>.py            # This is the main script that will be executed by manager
    - script_config.json            # See script_config.json
    - <other_required_files>

  - <script_2_name>/
    - <script_2_name>.py            # This is the main script that will be executed by manager
    - script_config.json            # See script_config.json
    - <other_required_files>

  - manage/                         # This is where the manager program and is dependencies lives
    - manage.py                     # This is the main manager program
    - manager_config.json           # 
    - resources/                    # This is where the manager helper modules and scripts live

  - .envs/                          # This is a directory automatically created by manage.py to host all virtual environments
    - <script_1_name>/              # Venv for script_1
    - <script_2_name>/              # Venv for script_2
```
NOTE: the script directory name and the script name MUST be the same in order for the manager to create virtual environments and execute scripts successfully. 

## Manager Configuration

The manager_config.json file configures the manager. As of now, it only configures the home path for the manager. The default is "/data/pyvenv_scripts". In this directory the scripts should be structured as specified above. This should be the exact same thing as the <root_path> mentioned above
CAUTION: make sure the "/" at the end of the path string is present! Otherwise, the script will not work. 
```
{
    "root_path":"/data/pyvenv_scripts/"     # Script will run
}
```
VS.
```
{
    "root_path":"/data/pyvenv_scripts"      # Script will FAIL
}
```
## Script Configuration
These script_config.json files in each script directory configure the script and its dependencies:
```
{
    "name":<script_name>,
    "dependencies":[
        <dependency_1>,
        <dependency_2>,
        <dependency_3>,
        ...
    ]
}
```
As of now, the name category is not being used. It is, however, good for debugging to configure a proper name in the json file. An example script_config.json is provided in the manage/resources directory

NOTE: Right now, the manager does not have the capabilit to check for duplicated environments. It is your responsibility to make sure no two scripts have the same name. Otherwise, the venv could fail to create or the existing venv could be destroyed. Duplicate check will come in a future update. 

The manager installs python dependencies with pip, so for each dependency, please name it EXACTLY as the name used by pip. This means
```
{
    "name":<script_name>,
    "dependencies":[
        "BeautifulSoup4",               # Script will Fail
        "bs4"                           # Script will work
    ]
}
```

# Example Usage
## Configure Script Directory
Let's say I wrote a print_hello script that imports JSON, bs4, dropbox as my dependencies and prints out "Hello Venv!". Configure your script directories as mentioned above. For this case, I will have a script directory like this: 
```
/data/pyvenv_scripts/
  - print_hello/
    - print_hello.py
    - script_config.json
    - some_other_stuff/
  - manage/
    - manage.py
    - manager_config.json
    - resources/
  - .envs/
    - print_hello/
```
Where the script_config.json looks like
```
{
  "name":"print_hello",
  "dependencies":[
     "bs4",
     "dropbox"
  ]                         # Notice json module is part of Python, so no need to specify dependency
}
```

## Create Virtual Environment for Script

To create a virtual environment for this module, go to the manage directory and run
```
python3 manage.py create print_hello
```
The manager will automatically create a virtual environment for this script, add pip to the venv, and install the dependencies listed in script_config.json. 
NOTE: Right now, the manager does not have the capabilit to check for duplicated environments. It is your responsibility to make sure no two scripts have the same name. Otherwise, the venv could fail to create or the existing venv could be destroyed. Duplicate check will come in a future update. 

## Delete Virtual Environment

To delete a virtual environment, go to the manage directory and run
```
python3 manage.py remove print_hello
```
The manager only deletes the virtual environment, and your scripts path will be left intact in the original paths. 

## Run Script

Make sure you have created a virtual environment for this script using the method mentioned above. 
To run a script, go to the manage directory and run
```
python3 manage.py run print_hello
```
This activates the virtual environment for that script, runs the script, and deactivates virtual environment. 

This run command is intended for the n8n Execute node, where you run this line in the node and the manager takes care of the virtual environments for you. 

# Debugging
## Activate Virtual Environment
To manually activate a virtual environment and debug script, run
```
source /<root_directory>/.env/<script_name>/bin/activate
```
Now you can debug your script in the virtual environment.  

## Dectivate Virtual Environment
To deactivate the virtual environment, run
```
deactivate
```
NOTE: some shell does not have the "source" or "deactivate" command. All commands in manage.py and in the examples here are run with #!/bin/bash. Check documentaiton for your shell for how to activate python virtual environments. 

# Acknowledgements:
The manager installs pip in each virtual environment with [get-pip](https://github.com/pypa/get-pip)
The n8n-pyvenv-manager Docker image is based on [n8nio/n8n-debian](https://github.com/n8n-io/n8n/tree/master/docker/images/n8n-debian) and [nodejs-bullseye](https://hub.docker.com/layers/library/node/bullseye/images/sha256-57087574a8147a31efb0d21ef3b43ae8340ec7bf66679bb1a39b0f40b9f9f25b?context=explore)

# Future Plans
1. Enable duplicate checks. Right now, it is up to you to make sure no two scripts have the same directory name. 
2. Enable adding arguments to the end of scripts. Right now, a workaround is to save the arguments in a json file and let another script read that json file to get the parameters. 
3. autoremove command to remove unused virtual environments