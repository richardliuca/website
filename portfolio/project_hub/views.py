from flask import url_for, flash, redirect, request, abort
from jinja2 import TemplateNotFound
from portfolio.views import GeneralView

class Hub(GeneralView):
    def dispatch_request(self):
        return super().dispatch_request(title='Projects Hub')
