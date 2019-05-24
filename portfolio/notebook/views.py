from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView
from portfolio.catalog import Catalog

class Notebook(GeneralView):

    def dispatch_request(self):
        post_catalog = Catalog(source='notes')
        return super().dispatch_request(title='Notebook', catalog=post_catalog)
