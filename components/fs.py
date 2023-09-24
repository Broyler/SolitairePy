from json import loads


def load(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return loads(f.read())
