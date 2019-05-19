from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView
from portfolio.catalog import Catalog

class Hub(GeneralView):

    def dispatch_request(self):
        book_keeping = Catalog(source='projects')
        return super().dispatch_request(title='Project Hub',
                                        num=book_keeping.num,
                                        modules=book_keeping.property_list)
