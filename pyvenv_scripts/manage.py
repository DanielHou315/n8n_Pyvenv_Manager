import os, sys, json

# Put existing scripts dir in a list
def find_existing_scripts(root):
    script_list = []
    for dir in os.listdir(root):
        if dir != "manage" and os.path.isdir(dir) and os.path.isfile(os.path.join(dir, "script_config.json")):
            script_list.append(dir)
    return script_list

def find_existing_envs(root):
    env_list = []
    for dir in os.listdir(os.path.join(root, ".envs/")):
        if os.path.isdir(dir):
            env_list.append(dir)
    return env_list

def autoremove(root):
    scripts = find_existing_scripts(root)
    envs = find_existing_envs(root)
    for env in envs:
        if env not in scripts:
            ip = input("Found Obsolete Environment '{0}', confirm delete? [Y/n]".format(env))
            if ip == 'Y' or ip == 'y':
                os.system("/bin/bash ./resources/remove_venv.sh {0}".format(env))
            else:
                print("Skipped Deleting {0}".format(env))


def create_script_env(root, name, dependencies):
    # Module setup
    module_name = name
    module_dependencies = dependencies

    # Check for proprietary libraries
    if module_name == 'manage':
        raise Exception("Module name 'manage' is reserved for the manager")

    # Create virtualenv
    env_path = root + ".envs/" + module_name
    os.system("python3 -m venv --without-pip " + env_path)
    # Activate virtualenv and setup
    activation_path = root + ".envs/" + module_name + "/bin/activate"
    # Install pip and dependent packages
    os.system("/bin/bash ./resources/install_pip.sh " + root + " " + module_name)
    for item in module_dependencies:
        os.system("/bin/bash ./resources/install_package.sh " + root + " " + module_name + " " + item)


def main():
    # Configure Manager
    try:
        with open("./manager_config.json") as conf:
            data = conf.read(); content = json.loads(data)
        root_path = content["root_path"]
    except:
        raise Exception("ERROR: unable to configure manager with manager_config.json")

    if len(sys.argv) > 1:
        # If create venv
        if sys.argv[1] == "create":
            # if no argument provided, raise exception
            if len(sys.argv) != 3:
                raise Exception("Wrong number of arguments for command 'create'!")

            # Otherwise load config of the 
            with open(root_path + sys.argv[2] + "/script_config.json", 'r') as conf:
                data = conf.read(); config = json.loads(data)
                create_script_env(root_path, config["name"], config["dependencies"])

        # If run script
        elif sys.argv[1] == "run":
            # If no argument provided, raise Exception
            if len(sys.argv) != 3:
                raise Exception("Wrong number of arguments for command 'run'!")
            # Otherwise run script
            os.system("/bin/bash ./resources/run_script.sh {0} {1}".format(root_path, sys.argv[2]))

        # If remove venv
        elif sys.argv[1] == "remove":
            # If no argument provided, raise Exception
            if len(sys.argv) != 3:
                raise Exception("Wrong number of arguments for command 'remove'!")
            # Otherwise run remove_venv.sh
            os.system("/bin/bash ./resources/remove_venv.sh {0}".format(sys.argv[2]))

        # If autoremove
        elif sys.argv[1] == "autoremove": autoremove(root_path)

        # Otherwise, raise exception not valid command
        else: raise Exception("Invalid Command " + sys.argv[1] + "!\nValid commands are 'create', 'run', 'remove'.")

    else: print("Valid pyvenv-manager commands are 'create <script_name>', 'run <script_name>', 'remove <script_name>'.")
    return


if __name__ == "__main__":
    main()
