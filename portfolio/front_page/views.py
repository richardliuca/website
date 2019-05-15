from flask import url_for, flash, redirect, request, abort
from jinja2 import TemplateNotFound
from portfolio.views import GeneralView

class Home(GeneralView):
    pass
