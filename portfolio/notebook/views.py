from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView
from portfolio.catalog import Catalog

class Notebook(GeneralView):

    def dispatch_request(self):
        book_keeping = Catalog(source='notes')
        return super().dispatch_request(title='Notebook',
                                        num=book_keeping.num,
                                        modules=book_keeping.property_list)
