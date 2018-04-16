import json

settings = open(r"C:\Users\pruszyns\Desktop\settings.txt", "r")
settings_content = json.load(settings)
settings.close()


def read_settings(settings_content, option):
    print settings_content[option]


read_settings(settings_content, "log_dir")