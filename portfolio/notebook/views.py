from flask import url_for, flash, redirect, request, abort
from portfolio.views import GeneralView

class Notebook(GeneralView):

    def count_notes(self):
        try:
            from portfolio.notes_catalog import notes_num, module_list
        except:
            notes_num = 0

        return notes_num, module_list

    def dispatch_request(self):
        notes_num, modules = self.count_notes()
        return super().dispatch_request(title='Notebook',
                                        notes_num=notes_num,
                                        modules=modules)
