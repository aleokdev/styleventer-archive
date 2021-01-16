import enum


class ExecuteFlags(enum.IntFlag):
    Continue = 0
    ExitSpecifier = 1
    ExitParent = 2
    ExitProgram = 4
    JumpToToken = 8


class ExecContext:
    def __init__(self, tokens):
        self.pc = 0
        self.tokens = tokens
        self.all_stacks = {0:[]}
        self.stack_index = 0
        self.variables = {"CHAR":"", "WORD":"", "TEXT":""}
        self.output = ""
        self.flags = ExecuteFlags.Continue
        self.jump_to = None
        self.labels = {}

    @property
    def stack(self):
        return self.all_stacks[self.stack_index]

    @stack.setter
    def stack(self, val):
        self.all_stacks[self.stack_index] = val

    def create_stack(self, n):
        self.all_stacks[n] = []


class ExecutionError(Exception):
    def __init__(self, token, message):
        self.message = message
        self.token = token
