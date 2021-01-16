from .tokencmds import *
from .tokenbase import *


class ProgramScript:
    def __init__(self, prg):
        self.source = prg
        self.pc = 0
        self.labels = {}

    def next(self):
        if self.pc >= len(self.source):
            return None
        self.pc += 1
        return self.source[self.pc - 1]

    def peek(self):
        if self.pc >= len(self.source):
            return None
        return self.source[self.pc]


class TokenizationException(Exception):
    def __init__(self, pc, message):
        self.culprit_pc = pc
        self.message = message


def parse_variable(script: ProgramScript) -> VariableExecToken:
    # Check if string starts with hash
    if script.next() != '#':
        raise TokenizationException(script.pc, "Variables must start with a pound symbol (#)")

    var_name = ""
    while True:
        nextchar = script.next()
        if nextchar == '#':
            break
        elif nextchar is None:
            raise TokenizationException(script.pc, "Unfinished variable name; Use # to end your variable names")
        elif str.isspace(nextchar):
            raise TokenizationException(script.pc, "Variable names must not contain spaces")
        var_name += nextchar

    return VariableExecToken(var_name)


def parse_literal(script: ProgramScript) -> LiteralExecToken:
    if script.next() != '"':
        raise TokenizationException(script.pc, "Literals must start and end with quotes")

    content = ""
    while script.peek() != '"':
        if script.peek() is None:
            raise TokenizationException(script.pc, "Unexpected EOF while parsing literal")
        content += script.next()

    script.next()
    return LiteralExecToken(content)


def parse_number(script: ProgramScript) -> NumberExecToken:
    if not script.peek().isdigit():
        raise TokenizationException(script.pc, "Expected a number value")

    number = ""
    while script.peek().isdigit():
        number += script.next()

    return NumberExecToken(int(number))


def parse_conditional(script: ProgramScript) -> ExecToken:
    if script.next() != "?":
        raise TokenizationException(script.pc, "Expected '?' symbol before conditional contents")

    if script.peek() == ">":
        script.next()
        token = GreaterConditionalExecToken()
    else:
        token = EqualConditionalExecToken()
    if script.next() != "/":
        raise TokenizationException(script.pc, "Expected forward slash '/' before conditional contents")

    while True:
        if script.peek() == '/':
            script.next()
            return token
        else:
            tok, do_exit = parse_command(script, token)
            token.add_content(tok)
            if do_exit: return token

    script.next()
    return token


def parse_label(script: ProgramScript, parent) -> ExecToken:
    if script.next() != ":":
        raise TokenizationException(script.pc, "Labels must start with a colon (:)")

    name = ""
    while script.peek() != ":":
        if script.peek() is None:
            raise TokenizationException(script.pc, "Unexpected EOF while parsing label")
        name += script.next()

    script.next()
    script.labels[name] = LabelExecToken(name, parent.get_next_pc())
    return script.labels[name]


def parse_jump(script: ProgramScript) -> ExecToken:
    if script.next() != "=":
        raise TokenizationException(script.pc, "Jumps must start with an equals sign (=)")
    if script.next() != ">":
        raise TokenizationException(script.pc, "Expected jump command")

    name = ""
    while not (script.peek().isspace() or script.peek() == "/"):
        name += script.next()

    return JumpExecToken(name)


def parse_command(script: ProgramScript, parent) -> ExecToken:
    nextchar = script.peek()
    if nextchar is None:
        return None
    elif nextchar == '"':
        return parse_literal(script), False
    elif nextchar.isspace():
        script.next()
        return None, False
    elif nextchar == ":":
        return parse_label(script, parent), False
    elif nextchar == "=":
        return parse_jump(script), False
    elif nextchar == "o":
        script.next()
        return OrdCmdToken(), False
    elif nextchar == "c":
        script.next()
        return CharCmdToken(), False
    elif nextchar == ".":
        script.next()
        return OutputLastStackCharCmdToken(), False
    elif nextchar == "!":
        script.next()
        return OutputStackCmdToken(), False
    elif nextchar == "+":
        script.next()
        return AddLastTwoNumbersCmdToken(), False
    elif nextchar == "-":
        script.next()
        return SubstractLastTwoNumbersCmdToken(), False
    elif nextchar == "*":
        script.next()
        return MultiplyLastTwoNumbersCmdToken(), False
    elif nextchar == "?":
        return parse_conditional(script), False
    elif nextchar == "<":
        script.next()
        if script.peek() == "e":
            script.next()
            return RemoveAllValuesFromStackCmdToken(), False
        else:
            return RemoveLastValueFromStackCmdToken(), False
    elif nextchar == ">":
        script.next()
        return DuplicateLastValueFromStackCmdToken(), False
    elif nextchar == "[":
        script.next()
        if script.next() != "]":
            raise TokenizationException(script.pc, "Expected closing bracket")
        return SwitchStackCmdToken(), False
    elif nextchar == "@":
        script.next()
        if script.next() != "[":
            raise TokenizationException(script.pc, "Expected opening bracket")
        if script.next() != "]":
            raise TokenizationException(script.pc, "Expected closing bracket")
        return MoveStackValCmdToken(), False
    elif nextchar.isdigit():
        return parse_number(script), False
    elif nextchar == "^":
        script.next()
        if script.peek() == "/":
            script.next()
            return ExitParentCmdToken(), True
        if script.peek() == "^":
            script.next()
            if script.peek() == "/":
                script.next()
                return ExitSpecifierCmdToken(), True
            if script.peek() == "^":
                script.next()
                if script.peek() == "/":
                    script.next()
                    return ExitProgramCmdToken(), True
        else:
            return PowerLastTwoNumbersCmdToken(), False
    elif script.peek() == '#':
        return parse_variable(script), False
    else:
        raise TokenizationException(script.pc, f"Unexpected command starting with {nextchar}")


def parse_tokens_specificator(script: ProgramScript) -> SpecificatorExecToken:
    # First, check the specificator type.
    binding = script.next()
    if binding not in SpecificatorTypeBindings:
        raise TokenizationException(script.pc, f"Specificator {binding} is not allowed.")

    specificator_type = SpecificatorTypeBindings[binding]

    # Check if specificator type is followed by a forward slash.
    if script.next() != '/':
        raise TokenizationException(script.pc, "Specificators must be followed by a forward slash (/)")

    token = SpecificatorExecToken(specificator_type)
    while True:
        if script.peek() == '/':
            script.next()
            return token
        else:
            tok, do_exit = parse_command(script, token)
            token.add_content(tok)
            if do_exit: return token


def parse_tokens(script) -> list:
    tokens = []
    while script.peek() is not None:
        tokens.append(parse_tokens_specificator(script))
    return tokens
