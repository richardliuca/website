from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView
from portfolio.catalog import Catalog

class Hub(GeneralView):

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', None)
        kwargs = {'source': 'project', 'page': page}
        if category:
            kwargs.update({'category': category})
        try:
            post_catalog = Catalog(**kwargs)
        except:
            abort(404)
        return super().dispatch_request(title='Project Hub',
                                        catalog=post_catalog.posts,
                                        source='projects')

class Notebook(GeneralView):

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', None)
        kwargs = {'source': 'note', 'page': page}
        if category:
            kwargs.update({'category': category})
        try:
            post_catalog = Catalog(**kwargs)
        except:
            abort(404)
        return super().dispatch_request(title='Notebook',
                                        catalog=post_catalog.posts,
                                        source='notes')
