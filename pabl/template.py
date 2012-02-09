from __future__ import unicode_literals

#from mako.template import Template as MakoTemplate
from mako.lookup import TemplateLookup


class Template(object):
    def __init__(self, root_template_location, module_directory):
        self.lookup = TemplateLookup(directories=[root_template_location],
            module_directory=module_directory if module_directory else None)

    def load_template(self, template_location, **kwargs):
        template = self.lookup.get_template(template_location)
        return template.render(**kwargs)
