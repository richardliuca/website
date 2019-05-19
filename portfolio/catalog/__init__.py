from flask import current_app
from pathlib import Path
import os

class Catalog(object):

    num = 0
    property_list = []

    def __init__(self, source=None):
        if source is not None:
            proj_dir = Path(current_app.instance_path).joinpath(source)

            try:
                for folder in os.listdir(proj_dir):
                    if folder.startswith('__'):
                        pass
                    elif proj_dir.joinpath(folder).is_dir():
                        self.num += 1
                        self.property_list.append({
                            'name': 'Python',
                            'description': 'I learnt python from Learn Python The Hard Way',
                            'category': 'Programming Languange'
                        })
                    else:
                        pass
            except:
                pass
