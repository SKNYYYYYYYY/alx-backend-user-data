#!/usr/bin/env python3

from flask import Flask, request, jsonify
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
from datetime import datetime

class Me:
    id = 1
    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert the object a JSON dictionary
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result


def p():
    me = Me()
    print(">>>>>>>",me)
    out = jsonify(me.to_json())
    print("<<<<<<<<<",out)
    out.set_cookie("ds", "sis")
    return out

if __name__ == "__main__":
   p()