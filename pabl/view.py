from __future__ import unicode_literals


class View(object):
    def __init__(self, item):
        self._item = item

    @property
    def resource_name(self):
        return self._item[0]

    @property
    def _fields_and_permissions(self):
        return self._item[1]

    def _yield_visible_fields(self, user, field_or_permission):
        spec, permissions, fields = field_or_permission[0]
        if spec != '@permissions':
            return
        if not any([user.has_permission(permission)
                    for permission in permissions]):
            return
        for field in fields:
            yield field

    def visible_fields(self, user=None):
        for field_or_permission in self._fields_and_permissions:
            if isinstance(field_or_permission, basestring):
                yield field_or_permission
                continue
            if isinstance(field_or_permission, list):
                item = field_or_permission
                if not len(item):
                    continue
                if len(item) == 3:
                    if item[1] == 'as':
                        yield (item[0], item[2])
                        continue
                if user and isinstance(item[0], list) and len(item[0]) == 3:
                    for field in self._yield_visible_fields(user, item):
                        yield field
