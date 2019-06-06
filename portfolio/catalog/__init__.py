import os
from flask import current_app
from pathlib import Path
from portfolio import db, bcrypt
from portfolio.models import db, Post, Tag

class Catalog(object):

    def __init__(self, page=1, **kwargs):
        self.posts = Post.query.filter(Post.complete == kwargs['complete'])
        if kwargs['or']:
            self.posts = self.posts.filter(Post.tags.any(Tag.name == kwargs['tag'][0]))
            kwargs['tag'].pop(0)
            self.posts = self.posts.filter(db.or_(*[Post.tags.any(Tag.name == tag) for tag in kwargs['tag']]))
        else:
            for tag in kwargs['tag']:
                self.posts = self.posts.filter(Post.tags.any(Tag.name == tag))

        self.posts = self.posts.order_by(Post.id.desc()).\
                                paginate(page=page, per_page=kwargs['max_page'])
