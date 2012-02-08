from pabl import View, PABLParser

import unittest


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
    @role marketplaces:
        restricted;
@item account2:
    # default values for everyone
    first, second;
    @role admin,pimp:
        adminOnly, secret, field;
    @role joe:
        joeonly;
    """


class TestPABL(unittest.TestCase):
    def test_integration(self):
        parser = PABLParser()
        parsed = parser.parse_pabl(TEST_DATA).asList()

        class LikeAUser(object):
            def in_role(self, role_name):
                return role_name == 'joe'

        user = LikeAUser()

        anonymous_results = [
            ['first', 'second', 'third', 'fourth'],
            ['first', 'second', 'third', 'fourth'],
            ['first', 'second', ]
        ]

        user_results =  [
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

