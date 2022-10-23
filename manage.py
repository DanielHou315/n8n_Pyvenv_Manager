import os
import sys
import json

def create_script_env(name, requirements, root):
    # Module setup
    module_name = name
    module_requirements = requirements
    # Check for proprietary libraries
    if module_name == 'lib' or module_name == 'manage':
        raise Exception("Module lib is propritary")

    # Create virtualenv
    env_path = root + ".envs/" + module_name
    os.system("python3 -m venv --without-pip " + env_path)
    # Activate virtualenv and setup
    activation_path = root + ".envs/" + module_name + "/bin/activate"
    # Install pip and dependent packages
    os.system("/bin/bash ./resources/install_pip.sh " + root + " " + module_name)
    for item in module_requirements:
        os.system("/bin/bash ./resources/install_package.sh " + root + " " + module_name + " " + item)



def main():
    with open("./manager_config.json") as conf:
        data = conf.read(); content = json.loads(data)
    root_path = content["root_path"]
    if len(sys.argv) > 1:

        # If create venv
        if sys.argv[1] == "create":
            if len(sys.argv) != 3:
                raise Exception("Wrong number of arguments for command 'create'!")
            with open(root_path + sys.argv[2] + "/script_config.json", 'r') as conf:
                data = conf.read()
                config = json.loads(data)
                create_script_env(config["name"], config["dependencies"], root_path)

        # If run script
        elif sys.argv[1] == "run":
            if len(sys.argv) != 3:
                raise Exception("Wrong number of arguments for command 'run'!")
            else:
                os.system("/bin/bash ./resources/run_script.sh {0}".format(sys.argv[2]))

        # If remove venv
        elif sys.argv[1] == "remove":
            if len(sys.argv) != 3:
                raise Exception("Wrong number of arguments for command 'remove'!")
            else:
                os.system("/bin/bash ./resources/remove_venv.sh {0}".format(sys.argv[2]))
        else:
            # print(sys.argv[1])
            print("Help Documents coming! Guess what to do now hahaha")
    else:
        print("2Help Documents coming! Guess what to do now hahaha")
    return


if __name__ == "__main__":
    main()
