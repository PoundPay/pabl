from view import View
from parser import PABLParser
from template import Template


__all__ = ['PABL']


class PABL(object):
    def __init__(self, root_template_directory=None, module_directory=None):
        self.template_loader = Template(root_template_directory,
            module_directory)
        self.formatters = {'json': self._to_json}
        self.parser = PABLParser()

    def render_to(self, format, obj, user=None, ):
        if isinstance(obj, tuple):
            template_name = obj[1]
        else:
            template_name = obj.__pabl__

        unparsed_pabl = self.template_loader.load_template(template_name)
        parsed_pabl = self.parser.parse_pabl(unparsed_pabl).asList()[0]
        view = View(parsed_pabl[0])

        return self.formatters[format](obj, view.visible_fields(user))

    def _to_json(self, obj, visible_fields):
        json_dict = {}
        for field in visible_fields:
            field_value = getattr(obj, field)
            try:
                field_value = field_value()
            except TypeError:  # object is not callable
                pass
            json_dict[field] = field_value
        return json_dict
