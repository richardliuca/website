from flask import current_app
from pathlib import Path
import os

proj_num = 0
module_list = []

proj_dir = Path(current_app.instance_path).joinpath('projects')

for folder in os.listdir(proj_dir):
    if folder.startswith('__'):
        pass
    elif proj_dir.joinpath(folder).is_dir():
        proj_num += 1
        module_list.append({
            'name': 'Flask Website',
            'description': "I built a personal website using Flask backend framework and using bootstrap for most of the front end.",
            'category': 'Software'
        })
    else:
        pass
