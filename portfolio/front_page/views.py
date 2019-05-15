from flask import url_for, flash, redirect, request, abort
from jinja2 import TemplateNotFound
from portfolio.views import GeneralView

class Home(GeneralView):
    def dispatch_request(self):
        return super().dispatch_request(title='Home')

class About(GeneralView):
        def dispatch_request(self):
            return super().dispatch_request(title='About Me')
