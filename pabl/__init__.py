from view import View
from parser import PABLParser
from template import Template


__all__ = ['PABL']


class PABL(object):
    def __init__(self, root_template_directory=None, module_directory=None):
        self.template_loader = Template(root_template_directory,
            module_directory)
        self.formatters = {'json': self.to_json}
        self.parser = PABLParser()

    def render_to(self, format, obj, user=None, wrap=True):
        if isinstance(obj, tuple):
            template_name = obj[1]
        else:
            template_name = obj.__pabl__

        view = self._load_view(template_name)
        return self.formatters[format](obj, view.resource_name,
            view.visible_fields(user), user, wrap)

    def _load_view(self, template_name):

        unparsed_pabl = self.template_loader.load_template(template_name)
        parsed_pabl = self.parser.parse_pabl(unparsed_pabl).asList()[0]
        view = View(parsed_pabl[0])

        return view

    def to_json(self, obj, resource_name, visible_fields, user, wrap):
        json_dict = self._to_json(obj, visible_fields, user)
        if wrap:
            return {resource_name: json_dict}
        return json_dict

    def _to_json(self, obj, visible_fields, user):
        json_dict = {}
        for field in visible_fields:
            if isinstance(field, tuple):  # we are aliasing this field
                field_value = PABL.find_obj(obj, field[0])
                field_name = field[1]
            else:
                field_value = PABL.find_obj(obj, field)
                field_name = field

            try:
                field_value = field_value()
            except TypeError:  # object is not callable
                pass

            if hasattr(field_value, '__pabl__'):
                field_value = self.render_to('json', field_value, user, False)

            json_dict[field_name] = field_value

        return json_dict

    @classmethod
    def find_obj(cls, obj, dotted):
        value = obj
        while dotted.find('.') >= 0:
            root, _, dotted = dotted.partition('.')
            value = getattr(value, root)
        return getattr(value, dotted)
