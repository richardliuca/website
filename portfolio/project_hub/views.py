from flask import url_for, flash, redirect, request, abort, current_app
from portfolio.views import GeneralView

class Hub(GeneralView):

    def count_projs(self):
        try:
            from portfolio.project_catalog import proj_num, module_list
        except:
            proj_num = 0
            module_list = None

        return proj_num, module_list

    def dispatch_request(self):
        proj_num, modules = self.count_projs()
        return super().dispatch_request(title='Project Hub',
                                        num=proj_num,
                                        modules=modules)
