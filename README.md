# n8n Python Virtualenv Manager

The n8n Python Virtual Environment Manager creates virtual environments and run your python scripts in virtual environment with one command. This allows your scripts to run in designated virtual environments in n8n that otherwise do not support persistent python site-package storage or virtual environment. Files saved from your script can also be read and edited by other n8n nodes or other scripts should you choose to do so. 

This packages comes with nano to help edit files and configure scripts from within the container, but you can always edit files in the maped directories from your host system. 

# Installation

Use the n8n-pyvenv-manager docker image . The configuration is as of now command-line based. This assumes you have some fundamental knowledge of unix operating systems and docker exec.

To Run with Docker Compose:

```
// Coming Soon
```

# Script Setup

1. Create a directory for each of your scripts in the /data/pyvenv_scripts directory like so:
   Each Script must be setup in a specific structure so that the manager can recognize the script and configure the virtual environments accordingly. The home directory of pyvenv_manager should look something like this: 

```
<root_path>/                        # root_directory for scripts in persistent n8n storage path
  - <script_1_name>/
    - <script_1_name>.py            # This is the main script that will be executed by manager
    - script_config.json            # See script_config.json
    - <other_required_files>
  - <script_2_name>/
    - <script_1_name>.py            # This is the main script that will be executed by manager
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

### manager_config.json

The json file configures the manager. As of now, it only configures the home path for the manager. The default is "/data/pyvenv_scripts". In this directory the scripts should be structured as specified above. This should be the exact same thing as the <root_path> mentioned above
CAUTION: make sure the "/" at the end of the path string is present! Otherwise, the script will not work. 
```
{
    "root_path":"/data/pyvenv_scripts/"     # OK
}
// vs
{
    "root_path":"/data/pyvenv_scripts"      # Script will FAIL
}
```
### script_config.json
This JSON file configures the script and its dependencies:
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
As of now, the name category is not being used. It is, however, good for debugging to configure a proper name in the json file. 
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
    - some_other_stuff/ # Whatever other scripts or modules print_hello script relies on
  - manage/ # This is where the manager program and is dependencies lives
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
     "BeautifulSoup4", # Script will Fail
     "bs4" # Script will work
  ]
}
```

## Create Virtual Environment for Script

To create a virtual environment for this module, run
```
python3
```

The manager will automatically create a virtual environment for this script, add pip to the venv, and install the dependencies listed in script_config.json. 

## Delete Virtual Environment

To delete a virtual environment, run
```
python3 /data/pyvenv_scripts/manage.py remove print_hello
```

The manager only deletes the virtual environment, and your scripts path will be left intact in the original paths. 

## Run Script
Make sure you have created a virtual environment for this script using the method mentioned above. 
To run a script, run
```
python3 /data/pyvenv_scripts/manage.py run print_hello
```

This activates the virtual environment for that script, runs the script, and deactivates virtual environment. 

## Auto Remove unused environments
Coming Soon

# Debugging
To manually activate a virtual environment and debug script, run
```
source /<root_directory>/.env/<script_name>/bin/activate
```
Now you can debug your script in the virtual environment.  

To deactivate the virtual environment, run
```
deactivate
```
NOTE: some shell does not have the "source" or "deactivate" command. All commands in manage.py and in the examples here are run with #!/bin/bash. Check documentaiton for your shell for how to activate python virtual environments. 

# More Documentation:
### manage.py
Coming Soon

# Future Plans
1. Enable adding arguments to the end of scripts. Right now, a workaround is to save the arguments in a json file and let another script read that json file to get the parameters. 
2. autoremove command to remove unused virtual environments