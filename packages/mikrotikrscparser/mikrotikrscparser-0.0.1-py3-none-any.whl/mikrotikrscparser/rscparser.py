from enum import Enum

from mikrotikrscparser.statement import Statement, CommandType


class ParserState(Enum):
    NONE = 0
    COMMENT = 1
    PATH = 2
    STATEMENT = 3
    PROPERTY = 4
    PROPERTY_VALUE_START = 5
    PROPERTY_VALUE_START_NEWLINE = 6
    PROPERTY_VALUE_QUOTED = 7
    PROPERTY_VALUE_QUOTED_ESCAPE = 8
    PROPERTY_VALUE_QUOTED_ESCAPE_NEWLINE = 9
    PROPERTY_VALUE_UNQUOTED = 10
    STATEMENT_CONDITION = 11
    NOW_END_STATEMENT = 100

class RscParser:

    def __init__(self):
        pass

    def parse(self, infile: str):
        statements = []
        buffer = ""
        head = 0
        path = ""
        c = ParserState.NONE
        property_key = ""
        property_value = ""
        escape_start = -1
        command_type = ""
        nextline_included = False
        condition = ""
        properties = []
        while head < len(infile):
            if c == ParserState.NONE and infile[head] == '#':
                c = ParserState.COMMENT
            elif c == ParserState.NONE and infile[head] == '/':
                c = ParserState.PATH
            elif infile[head] == '\r':
                pass
            elif c == ParserState.COMMENT and infile[head] == '\n':
                # print(f"COMMENT: {buffer}")
                buffer = ""
                c = ParserState.NONE
            elif c == ParserState.PATH and infile[head] == '\n':
                # print(f"PATH: {buffer}")
                path = buffer
                buffer = ""
                c = ParserState.NONE
            elif c == ParserState.NONE \
                    and (buffer == "add"\
                    or buffer == "set") :
                c = ParserState.STATEMENT
                command_type = buffer.strip()
                buffer = ""
            elif c == ParserState.STATEMENT and infile[head] == '[':
                c = ParserState.STATEMENT_CONDITION
                buffer = ""
            elif c == ParserState.STATEMENT_CONDITION and infile[head] == ']':
                c = ParserState.STATEMENT
                condition = buffer.strip()
                # print(f"Condition: {condition}")
                buffer = ""
            elif c == ParserState.STATEMENT and infile[head] != " " and infile[head] != "\n" and infile[head] != '\\':
                c = ParserState.PROPERTY
                buffer += "" + infile[head]
            elif c == ParserState.PROPERTY and infile[head] == " " and buffer.strip() != '':
                c = ParserState.STATEMENT
                property_key = buffer.strip()
                properties.append({property_key: None})
                buffer = ""
            elif c == ParserState.PROPERTY and infile[head] == "=":
                c = ParserState.PROPERTY_VALUE_START
                property_key = buffer.strip()
                buffer = ""
            elif c == ParserState.PROPERTY_VALUE_START and infile[head] != '\\':
                if infile[head] == '"':
                    c = ParserState.PROPERTY_VALUE_QUOTED
                else:
                    c = ParserState.PROPERTY_VALUE_UNQUOTED
                    buffer += "" + infile[head]
            elif c == ParserState.PROPERTY_VALUE_START and infile[head] == '\\':
                c = ParserState.PROPERTY_VALUE_START_NEWLINE
            elif c == ParserState.PROPERTY_VALUE_START_NEWLINE:
                if infile[head] != '\n' and infile[head] != ' ':
                    c = ParserState.PROPERTY_VALUE_START
                    if infile[head] == '"':
                        head -= 1
                    else:
                        buffer += "" + infile[head]
                else:
                    pass
            elif c == ParserState.PROPERTY_VALUE_QUOTED and infile[head] == '\\':
                c = ParserState.PROPERTY_VALUE_QUOTED_ESCAPE
            elif c == ParserState.PROPERTY_VALUE_QUOTED_ESCAPE:
                if infile[head] != '\n':
                    buffer += "\\" + infile[head]
                    c = ParserState.PROPERTY_VALUE_QUOTED
                else:
                    c = ParserState.PROPERTY_VALUE_QUOTED_ESCAPE_NEWLINE
            elif c == ParserState.PROPERTY_VALUE_QUOTED_ESCAPE_NEWLINE:
                if infile[head] != ' ':
                    c = ParserState.PROPERTY_VALUE_QUOTED
                    head -= 1
            elif (c == ParserState.PROPERTY_VALUE_UNQUOTED and infile[head] == ' ') \
                    or (c == ParserState.PROPERTY_VALUE_UNQUOTED and infile[head] == '\n') \
                    or (c == ParserState.PROPERTY_VALUE_QUOTED and infile[head] == '"'):
                property_value = buffer.strip()
                buffer = ""
                # print(f"PROPERTY: {path} => {property_key} = {property_value}")
                properties.append({property_key: property_value})
                if c == ParserState.PROPERTY_VALUE_UNQUOTED and infile[head] == '\n':
                    c = ParserState.NOW_END_STATEMENT
                else:
                    c = ParserState.STATEMENT
            elif c == ParserState.STATEMENT and infile[head] == '\\':
                nextline_included = True
            elif nextline_included and infile[head] == '\n':
                nextline_included = False
                buffer = ""
            elif c == ParserState.STATEMENT and infile[head] == '\n' and not nextline_included:
                c = ParserState.NOW_END_STATEMENT
            else:
                buffer += "" + infile[head]
            # print(f"* STATE: {c}: {infile[head]}")

            # Don't wait for these states to execute until moving head
            if c == ParserState.NOW_END_STATEMENT:
                statement = Statement(CommandType[command_type.upper()], path)
                statement.properties = properties
                properties = []
                if condition != "":
                    statement.condition = condition
                condition = ""
                statements.append(statement)
                c = ParserState.NONE

            head += 1
        return statements
