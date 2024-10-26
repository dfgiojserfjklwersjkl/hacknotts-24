import json

class Config:
    config = json.load(open("config.json", "r"))

    @classmethod
    def get(cls, key):
        return cls.config[key]