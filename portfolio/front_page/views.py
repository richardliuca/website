from flask import url_for, flash, redirect, request, abort, current_app
from portfolio.views import GeneralView
import os, pathlib
import os.path as path

class Home(GeneralView):
    def dispatch_request(self):
        return super().dispatch_request(title='Home')
