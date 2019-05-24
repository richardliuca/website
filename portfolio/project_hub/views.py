from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView
from portfolio.catalog import Catalog

class Hub(GeneralView):

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        post_catalog = Catalog(source='projects', page=page)
        return super().dispatch_request(title='Project Hub',
                                        catalog=post_catalog.posts,
                                        source='projects')
