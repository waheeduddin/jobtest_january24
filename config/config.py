import os

class Config(object):
    def __init__(self):
        self._config = {"OPENAI_API_KEY":os.getenv("OPENAI_API_KEY",default=None),
                        "MAIL_SERVER":os.getenv("MAIL_SERVER",default=None),
                        "MAIL_PORT":os.getenv("MAIL_PORT",default=None),
                        "MAIL_USERNAME":os.getenv("MAIL_USERNAME",default=None),
                        "MAIL_PASSWORD":os.getenv("MAIL_PASSWORD",default=None),
                        "MAIL_USE_TLS":True,
                        "MAIL_USE_SSL":False
                        }

    def check_config(self):
        for key in self._config.keys():
            if self._config[key] is None:
                print(f"ERROR: Environmnet variables not set\nPlease set the value of the variable {key} in the system environment variables.\nTo check how to set environment varaibles, please vist the following link:\nhttps://www3.ntu.edu.sg/home/ehchua/programming/howto/Environment_Variables.html")
                return False
        return True
    
    def get_property(self, property_name):
        if property_name not in self._config.keys(): # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]