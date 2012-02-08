from __future__ import unicode_literals


class View(object):
    def __init__(self, item):
        self._item = item

    @property
    def resource_name(self):
        return self._item[0]

    @property
    def _fields_and_roles(self):
        return self._item[1]

    def _yield_visible_fields(self, user, field_or_role):
        spec, roles, fields = field_or_role[0]
        if spec != '@role':
            return
        if not any([user.in_role(role) for role in roles]):
            return
        for field in fields:
            yield field

    def visible_fields(self, user=None):
        for field_or_role in self._fields_and_roles:
            if isinstance(field_or_role, basestring):
                yield field_or_role
                continue
            if (user and isinstance(field_or_role, list)
                and len(field_or_role[0]) == 3):
                for field in self._yield_visible_fields(user, field_or_role):
                    yield field
