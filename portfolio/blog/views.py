from flask import url_for, flash, redirect, request, abort
from portfolio.views import PostSearch

class Hub(PostSearch):
    title = 'Project Hub'
    target = ['project',]
    max_page = 8
    complete = True

class Notebook(PostSearch):
    title = 'Notebook'
    target = ['note',]
    max_page = 8
    complete = True
