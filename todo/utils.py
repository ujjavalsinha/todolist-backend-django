import uuid

def get_random_code():
    code = str(uuid.uuid())[:6].replace('-','').lower()
    return code