from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView
from portfolio.catalog import Catalog

class Hub(GeneralView):

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        tag = request.args.getlist('tag')
        tag = tag if not('project' in tag) else tag.remove('project')
        or_search = request.args.get('or', 0, type=int)
        kwargs = {'tag': ['project',], 'page': page, 'or': False,
                'complete': True, 'max_page': 8}
        if tag:
            kwargs['tag'].extend(tag)
            kwargs['or'] = or_search
        try:
            post_catalog = Catalog(**kwargs)
        except:
            abort(404)
        if 'project' in kwargs['tag']:
            tags = kwargs['tag'].remove('project')
        else:
            tags = kwargs['tag']
        return super().dispatch_request(title='Project Hub',
                                        catalog=post_catalog.posts,
                                        source='project',
                                        tags=tags,
                                        or_search=or_search)

class Notebook(GeneralView):

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        tag = request.args.getlist('tag')
        tag = tag if not('note' in tag) else tag.remove('note')
        or_search = request.args.get('or', 0, type=int)
        kwargs = {'tag': ['note',], 'page': page, 'or': False,
                'complete': True, 'max_page': 8}
        if tag:
            kwargs['tag'].extend(tag)
            kwargs['or'] = or_search
        try:
            post_catalog = Catalog(**kwargs)
        except:
            abort(404)
        if 'note' in kwargs['tag']:
            tags = kwargs['tag'].remove('note')
        else:
            tags = kwargs['tag']
        return super().dispatch_request(title='Notebook',
                                        catalog=post_catalog.posts,
                                        source='note',
                                        tags=tags,
                                        or_search=or_search)
