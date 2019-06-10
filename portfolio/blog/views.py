from flask import url_for, flash, redirect, request, abort
from portfolio.views import PostSearch

class Hub(PostSearch):
    title = 'Project Hub'
    target = ['project',]

class Notebook(PostSearch):
    title = 'NoteBook'
    target = ['note',]
