import os
import sys
import json

def create_script_env(name, requirements):
    # Module setup
    module_name = name
    module_requirements = requirements
    # Check for proprietary libraries
    if module_name == 'lib' or module_name == 'manage':
        raise Exception("Module lib is propritary")

    # Create virtualenv
    env_path = "/data/scripts/.envs/" + module_name
    os.system("python3 -m venv --without-pip " + env_path)
    # Activate virtualenv and setup
    activation_path = "/data/scripts/.envs/" + module_name + "/bin/activate"
    # Install pip and dependent packages
    os.system("/bin/bash ./resources/install_pip.sh " + module_name)
    for item in module_requirements:
        os.system("/bin/bash ./resources/install_package.sh " + module_name + " " + item)



def main():
    root_path = "/data/scripts/"
    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            if len(sys.argv) != 3:
                print("Wrong number of arguments")
                return
            with open(root_path + sys.argv[2] + "/script_config.json", 'r') as conf:
#             config = load_json(root_path + sys.argv[2] + "/script_config.json")
                data = conf.read()
                config = json.loads(data)
                create_script_env(config["name"], config["dependencies"])
        elif sys.argv[1] == "run":
            if len(sys.argv) != 3:
                print("Wrong number of arguments")
                return
            else:
                os.system("/bin/bash ./resources/run_script.sh {0}".format(sys.argv[2]))
        else:
            # print(sys.argv[1])
            print("Help Documents coming! Guess what to do now hahaha")
    else:
        print("2Help Documents coming! Guess what to do now hahaha")
    return


if __name__ == "__main__":
    main()
