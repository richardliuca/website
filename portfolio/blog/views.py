from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView
from portfolio.models import db, Post, Tag

class Hub(GeneralView):
    title = 'Project Hub'
    target = ['project',]
    max_page = 8
    complete = True

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        tags = [name.lower() for name in request.args.getlist('tag')
                                if not(name.lower() in self.target)]
        or_search = request.args.get('or', 0, type=int)

        if self.complete == True or self.complete == False:
            self.posts = Post.query.filter(Post.complete == self.complete)
        else:
            self.posts = Post.query

        self.posts = self.posts.filter(db.or_(
                    *[Post.tags.any(Tag.name == tag) for tag in self.target]))

        if or_search:
            self.posts = self.posts.filter(db.or_(
                    *[Post.tags.any(Tag.name == tag) for tag in tags]))
        else:
            for tag in tags:
                self.posts = self.posts.filter(Post.tags.any(Tag.name == tag))
            or_search = None

        self.posts = self.posts.order_by(Post.id.desc())

        if self.max_page:
            self.posts = self.posts.paginate(page=page, per_page=self.max_page)
        else:
            self.posts = self.posts.all()

        return super().dispatch_request(title=self.title,
                                        catalog=self.posts,
                                        source=self.target,
                                        tags=tags,
                                        or_search=or_search)

class Notebook(GeneralView):

    title = 'Notebook'

    def dispatch_request(self):
        posts = Post.query.filter_by(complete=True).\
                            filter(Post.tags.any(Tag.name == 'note')).\
                            filter(Post.tags.any(Tag.name == 'note')).all()
        tags = []
        condtion = lambda tag : tag not in tags and \
                                not(tag.name == 'note') and \
                                '-' not in tag.name
        [ tags.extend(filter(condtion, post.tags)) for post in posts]
        catalog = {}
        for tag in tags:
            match_post = tuple(filter(lambda post: tag in post.tags, posts))
            catalog.update({tag.name: match_post})

        return super().dispatch_request(title=self.title, catalog=catalog)
