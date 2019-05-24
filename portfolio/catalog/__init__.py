import os
from flask import current_app
from pathlib import Path
from portfolio import db, bcrypt
from portfolio.models import Project, Note

class Catalog(object):

    num = 0
    property_list = []

    def __init__(self, source=None):
        if source is not None:
            proj_dir = Path(current_app.instance_path).joinpath(source)

        if source == 'projects':
            self.post = db.session.query(Project).all()
        elif source == 'notes':
            self.post = db.session.query(Note).all()
        else:
            raise Exception('Wrong post type')
        self.count = len(self.post)
            # try:
            #     for folder in os.listdir(proj_dir):
            #         if folder.startswith('__'):
            #             pass
            #         elif proj_dir.joinpath(folder).is_dir():
            #             self.num += 1
            #             self.property_list.append({
            #                 'name': 'Python',
            #                 'description': 'I learnt python from Learn Python The Hard Way',
            #                 'category': 'Programming Languange'
            #             })
            #         else:
            #             pass
            # except:
            #     pass
