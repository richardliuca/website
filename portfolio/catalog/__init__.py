import os
from flask import current_app
from pathlib import Path
from portfolio import db, bcrypt
from portfolio.models import Post

class Catalog(object):

    def __init__(self, source=None, page=1, **kwargs):
        if source is not None:
            self.posts = Post.query.\
                filter_by(complete=True, post_type=source, **kwargs).\
                order_by(Post.date_posted.desc()).\
                paginate(page=page, per_page=9)
        else:
            raise Exception('Souce not specified')
