import os.path as path
import os
from importlib import import_module

dir, _ = path.split(path.abspath(__file__))

proj_num = 0
module_list = []

for folder in os.listdir(dir):
    if folder.startswith('__'):
        pass
    elif path.isdir(path.join(dir, folder)):
        proj_num += 1
        module_list.append(import_module('portfolio.project_catalog.'+folder))
    else:
        pass
