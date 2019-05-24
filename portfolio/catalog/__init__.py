import os
from flask import current_app
from pathlib import Path
from portfolio import db, bcrypt
from portfolio.models import Project, Note

class Catalog(object):

    num = 0
    property_list = []

    def __init__(self, source=None, page=1, **kwargs):
        if source is not None:
            proj_dir = Path(current_app.instance_path).joinpath(source)

        if source == 'projects':
            self.posts = Project.query.\
            filter_by(complete=True, **kwargs).order_by(Project.date_posted.desc()).\
            paginate(page=page, per_page=9)
        elif source == 'notes':
            self.posts = Note.query.\
            filter_by(complete=True, **kwargs).order_by(Note.date_posted.desc()).\
            paginate(page=page, per_page=9)
        else:
            raise Exception('Wrong post type')
