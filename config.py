from log import log
import json


def read_config():
    # * Read config and return json
    with open("config.json", "r") as file:
        json_data = json.load(file)
        return json_data
    log("INFO", "Reading from config")


def parse_config(conf_json, variable):
    if variable == "Token":
        return conf_json["Token"]
    else:
        return conf_json[variable]


def get_variable_from_config(name):
    variables_json = read_config()
    variable = None
    try:
        variable = variables_json[str(name)]
    except:
        variable = None
    return variable


def write_variable_to_config(name, value):
    dic = read_config()
    dic[str(name)].update(value)
    with open("config.json", "w") as f:
        json.dump(dic, f)
    log("INFO", "Writing to Config: {}".format(str(name) + ";" + str(value)))


def delete_variable_to_config(name, value):
    dic = read_config()
    dic[str(name)].pop(value)
    with open("config.json", "w") as f:
        json.dump(dic, f)
    log("INFO", "Deleting from Config: {}".format(str(name) + ";" + str(value)))
