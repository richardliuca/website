from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView

class Notebook(GeneralView):
    def dispatch_request(self):
        return super().dispatch_request(title='Notebook')
