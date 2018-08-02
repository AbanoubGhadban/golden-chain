import hashlib
import jsonpickle


def sha256(data):
    hash_object = hashlib.sha256(data)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def parseFromJson(strData):
    return jsonpickle.decode(strData)
