from flask import url_for, flash, redirect, request, abort, current_app
from portfolio.views import GeneralView
import os.path as path
import os
from pathlib import Path

class Hub(GeneralView):

    def count_proj(self):
        try:
            from portfolio.project_catalog import proj_num, module_list
        except:
            proj_num = 0

        return proj_num, module_list

    def dispatch_request(self):
        proj_num, modules = self.count_proj()
        return super().dispatch_request(title='Project Hub',
                                        proj_num=proj_num,
                                        modules=modules)
