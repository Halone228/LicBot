import json
def get_info(file_path):
    with open(file_path,'r') as f:
        return dict(json.load(f))