import enum
from .execbase import ExecuteFlags


class ExecToken:
    def execute(self, ctx):
        pass


class LiteralExecToken(ExecToken):
    def __init__(self, content: str):
        self.content = content

    def execute(self, ctx):
        ctx.stack.append(self.content)

    def __str__(self):
        return "LiteralExecToken with '" + self.content + "'"


class NumberExecToken(ExecToken):
    def __init__(self, content: int):
        self.content = content

    def execute(self, ctx):
        ctx.stack.append(self.content)

    def __str__(self):
        return "NumberExecToken with '" + str(self.content) + "'"


class SpecificatorType(enum.Enum):
    Character = 1
    Word = 2
    Text = 3
    Start = 4
    End = 5


SpecificatorTypeBindings = {'c': SpecificatorType.Character, 'w': SpecificatorType.Word, 't': SpecificatorType.Text,
                            's': SpecificatorType.Start, 'e': SpecificatorType.End}


class CommandContainerExecToken(ExecToken):
    def __init__(self):
        self.contents = []

    def add_content(self, token):
        if token is None:
            return
        self.contents.append(token)
        token.parent = self

    def check_execution_flags(self, ctx):
        if ctx.flags & ExecuteFlags.ExitProgram:
            return True
        if ctx.flags & ExecuteFlags.ExitSpecifier:
            ctx.flags ^= ExecuteFlags.ExitSpecifier
            return True
        if ctx.flags & ExecuteFlags.ExitParent:
            ctx.flags ^= ExecuteFlags.ExitParent
            return True
        return False

    def execute(self, ctx):
        for t in self.contents:
            t.execute(ctx)
            if self.check_execution_flags(ctx):
                return

    def execute_from(self, pc, ctx):
        for t in self.contents[pc:]:
            t.execute(ctx)
            if self.check_execution_flags(ctx):
                return

    def get_next_pc(self) -> int:
        return len(self.contents)


class SpecificatorExecToken(CommandContainerExecToken):
    def __init__(self, _type: SpecificatorType):
        super().__init__()
        self.specificator_type = _type

    def __str__(self):
        return self.specificator_type.name + " specificator:\n\t" + " ... ".join(str(t) for t in self.contents)


class EqualConditionalExecToken(CommandContainerExecToken):
    def comparer(self, ctx) -> bool:
        return ctx.stack[-1] == 0

    def check_execution_flags(self, ctx):
        if ctx.flags & ExecuteFlags.ExitProgram:
            return True
        if ctx.flags & ExecuteFlags.ExitSpecifier:
            return True
        if ctx.flags & ExecuteFlags.ExitParent:
            ctx.flags ^= ExecuteFlags.ExitParent
            return True
        return False

    def execute(self, ctx):
        if self.comparer(ctx):
            super().execute(ctx)


class GreaterConditionalExecToken(EqualConditionalExecToken):
    def comparer(self, ctx) -> bool:
        return ctx.stack[-1] > 0


class VariableExecToken(ExecToken):
    def __init__(self, _name: str):
        self.name = _name

    def __str__(self):
        return "Variable named " + self.name

    def execute(self, ctx):
        if self.name == "STACK_LENGTH":
            ctx.stack.append(len(ctx.stack))
        else:
            ctx.stack.append(ctx.variables[self.name])


class CommandExecToken(ExecToken):
    pass


class GenericCommandExecToken(ExecToken):
    def __init__(self, exec_function):
        self.execute = exec_function


class LabelExecToken(ExecToken):
    def __init__(self, _name, _pc):
        self.name = _name
        self.pc = _pc


class JumpExecToken(ExecToken):
    def __init__(self, _name):
        self.name = _name

    def execute(self, ctx):
        ctx.flags |= ExecuteFlags.JumpToToken | ExecuteFlags.ExitSpecifier
        ctx.jump_to = ctx.labels[self.name]
