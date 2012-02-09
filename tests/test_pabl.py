from __future__ import unicode_literals
import os
import mock
import unittest

from pabl import PABL
from pabl.view import View
from pabl.parser import PABLParser
from pabl.template import Template


TEST_DATA = """\
@item account:
    # default values for everyone
    first,
    second,

    third,
    fourth;
@item account1:
    # default values for everyone
    first, second, third,
    fourth;
    @permissions marketplaces:
        restricted;
@item account2:
    # default values for everyone
    first, second;
    @permissions admin,pimp:
        adminOnly, secret, field;
    @permissions joe:
        joeonly;
    """


class TestPABL(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.path_to_templates = os.path.realpath('tests/fixtures/templates/')
        self.module_directory = '/tmp/pabl'

    def test_parse_and_restrict(self):
        parser = PABLParser()
        parsed = parser.parse_pabl(TEST_DATA).asList()

        class LikeAUser(object):
            def has_permission(self, role_name):
                return role_name == 'joe'

        user = LikeAUser()

        anonymous_results = [
            ['first', 'second', 'third', 'fourth'],
            ['first', 'second', 'third', 'fourth'],
            ['first', 'second', ]
        ]

        user_results = [
            ['first', 'second', 'third', 'fourth'],
            ['first', 'second', 'third', 'fourth'],
            ['first', 'second', 'joeonly'],
        ]

        for counter, item in enumerate(parsed[0]):
            view = View(item)
            self.assertEqual(list(view.visible_fields()),
                anonymous_results[counter])
            self.assertEqual(list(view.visible_fields(user)),
                user_results[counter])

    def test_load_template(self):
        template = Template(self.path_to_templates, self.module_directory)
        template_data = template.load_template('test.pabl')
        self.assertEqual(template_data.split('\n')[0], '@item account:')

    def test_PABL(self):
        mock_account = mock.Mock()
        mock_account.__pabl__ = 'test.pabl'
        pabl = PABL(self.path_to_templates, self.module_directory)
        json = pabl.render_to('json', mock_account, None)
        self.assertDictEqual(json, {'id': mock_account.id.return_value,
                                    'title': mock_account.title.return_value})
