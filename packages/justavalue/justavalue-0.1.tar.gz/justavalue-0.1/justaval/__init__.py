import os
import json
import asyncio
config = {
    'base_file': 'justaval.json',
}
loop = None

def file_exists(file_name):
    if file_name in os.listdir():
        return bool(os.path.getsize(file_name))
    return False

def setup():
    if not file_exists(config['base_file']):
        fl = open(config['base_file'], '+wb')
        fl.write(b'{}')
        fl.close()
    op = open(config['base_file'], 'rb')
    return json.load(op)    
data = setup()

def commit():
    with open(config['base_file'], '+w') as file:
        json.dump(data, file)
        file.close()


class JustAval():
    def __init__(self, value_name:str, base_data = {}):
        self.vals = data
        if value_name not in self.vals:
            self.vals[value_name] = base_data
            self.vals = self.vals[value_name]
        else:
            self.vals = self.vals[value_name]
        self.value_name = value_name

    def keys(self):
        return [i for i in self.vals]
    
    def values(self):
        return [self.vals[i] for i in self.vals]

    def __setitem__(self, key,value) -> None:
        self.vals[key] = value
        commit()
    
    def __delitem__(self, __key) -> None:
        self.vals.pop(__key)
        commit()
    
    def __getitem__(self, __key):
        return self.vals[__key]

        


        