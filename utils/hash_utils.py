import hashlib

def hash_id(input_string):
    return hashlib.sha256(input_string.encode("utf-8")).hexdigest()
