import json


def read_config():
    # * Read config and return json
    with open("config.json", "r") as file:
        json_data = json.load(file)
        return json_data


def parse_config(conf_json, variable):
    if variable == "Token":
        return conf_json["Token"]
    else:
        raise Exception("Can't find specified id in config")


def get_variable_from_config(name):
    variable = parse_config(read_config(), name)
    return variable


def write_variable_to_config(name, value):
    variable = {name: value}
    dic = read_config()
    dic.update(variable)
    with open("config.json", "w") as f:
        json.dump(dic, f)
    # TODO: Log the value to the config
