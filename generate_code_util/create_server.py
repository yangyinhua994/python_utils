import base

controller_fime_name = "TexturesServer.java"
intercept = "Server.java"

def start():
    before_file_name = controller_fime_name.split(intercept.split(".")[0])[0]
    with open(controller_fime_name, "r") as controllerFile:
        data = controllerFile.read().replace(before_file_name[0].upper() + before_file_name[1:],
                                             base.get_file_name_last_upper()).replace(
            before_file_name[0].lower() + before_file_name[1:], base.get_file_name_last_lower())
        base.write_file(data, base.service_path + "/" + base.get_file_name_last_upper() + intercept)
