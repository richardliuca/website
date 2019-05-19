from flask import current_app
from pathlib import Path
import os

notes_num = 0
module_list = []

proj_dir = Path(current_app.instance_path).joinpath('notes')

for folder in os.listdir(proj_dir):
    if folder.startswith('__'):
        pass
    elif proj_dir.joinpath(folder).is_dir():
        notes_num += 1
        module_list.append({
            'name': 'Python',
            'description': 'I learnt python from Learn Python The Hard Way',
            'category': 'Programming Languange'
        })
    else:
        pass
