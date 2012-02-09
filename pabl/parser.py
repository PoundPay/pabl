from  __future__ import unicode_literals

from pyparsing import (Group, col, ParseFatalException, ParseException,
                       lineEnd, Group, Literal, Word, Forward, delimitedList,
                       empty, FollowedBy, restOfLine, alphas, alphanums,
                       OneOrMore)


class PABLParser(object):
    def __init__(self):
        self.indentStack = [1]

    def check_peer_indent(self, s, l, t):
        curCol = col(l, s)
        if curCol != self.indentStack[-1]:
            if (not self.indentStack) or curCol > self.indentStack[-1]:
                raise ParseFatalException(s, l, "illegal nesting")
            raise ParseException(s, l, "not a peer entry")

    def check_sub_indent(self, s, l, t):
        curCol = col(l, s)
        if curCol > self.indentStack[-1]:
            self.indentStack.append(curCol)
        else:
            raise ParseException(s, l, "not a subentry")

    def check_unindent(self, s, l, t):
        if l >= len(s):
            return
        curCol = col(l, s)
        if not(curCol < self.indentStack[-1]
               and curCol <= self.indentStack[-2]):
            raise ParseException(s, l, "not an unindent")

    def unindent(self):
        self.indentStack.pop()

    def parse_pabl(self, raw_pabl):
        INDENT = lineEnd.suppress() + empty + empty.copy().setParseAction(
            self.check_sub_indent)
        UNDENT = FollowedBy(empty).setParseAction(self.check_unindent)
        UNDENT.setParseAction(self.unindent)

        terminator = Literal(';').suppress()
        comment = Literal('#') + restOfLine
        item_name = Word(alphas, alphanums)
        variable = Word(alphas, alphanums + '_.')
        variable_as = (variable + 'as' + item_name)

        stmt = Forward()
        suite = Group(
            OneOrMore(empty + stmt.setParseAction(self.check_peer_indent)))
        suite.ignore(comment)

        item_start = Literal('@item').suppress()
        item_end = Literal(':').suppress()
        permission_start = Literal('@permissions')

        item_decl = (item_start + item_name.setResultsName('item') + item_end)
        item_defn = Group(item_decl + INDENT + suite + UNDENT)

        permission_decl = (permission_start + Group(
            delimitedList(item_name).setResultsName('permissions')) + item_end)
        permission_defn = Group(permission_decl + INDENT + suite + UNDENT)

        fieldList = delimitedList(
            Group(variable_as) | variable
        ).setResultsName('fields') + terminator

        stmt << (item_defn | fieldList | Group(permission_defn))

        parseTree = suite.parseString(raw_pabl)

        return parseTree
