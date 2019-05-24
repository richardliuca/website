import os
from flask import current_app
from pathlib import Path
from portfolio import db, bcrypt
from portfolio.models import Project, Note

class Catalog(object):

    num = 0
    property_list = []

    def __init__(self, source=None, page=1):
        if source is not None:
            proj_dir = Path(current_app.instance_path).joinpath(source)

        if source == 'projects':
            self.posts = Project.query.order_by(Project.date_posted.desc()).paginate(page=page, per_page=9)
        elif source == 'notes':
            self.posts = Note.query.order_by(Note.date_posted.desc()).paginate(page=page, per_page=9)
        else:
            raise Exception('Wrong post type')



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
