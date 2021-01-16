from .tokenbase import *
from .execbase import *


class OrdCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) == 0:
            raise ExecutionError(self, "Tried to get value from empty stack")
        ctx.stack.append(ord(ctx.stack.pop()))

    def __str__(self):
        return "Command ord stack"


class CharCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) == 0:
            raise ExecutionError(self, "Ran character stack command with empty stack")
        ctx.stack.append(chr(ctx.stack.pop()))

    def __str__(self):
        return "Command chr stack"


class OutputStackCmdToken(CommandExecToken):
    def execute(self, ctx):
        ctx.output += "".join(str(i) for i in ctx.stack)
        ctx.stack = []

    def __str__(self):
        return "Command output stack"


class OutputLastStackCharCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) == 0:
            return
        ctx.output += str(ctx.stack.pop())

    def __str__(self):
        return "Command output last char of stack"


class AddLastTwoNumbersCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) < 2:
            raise ExecutionError(self, "Ran stack add command with less than two stack elements")
        ctx.stack.append(ctx.stack.pop() + ctx.stack.pop())

    def __str__(self):
        return "Command add last two stack numbers"


class SubstractLastTwoNumbersCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) < 2:
            raise ExecutionError(self, "Ran stack substract command with less than two stack elements")
        b = ctx.stack.pop()
        ctx.stack.append(ctx.stack.pop() - b)

    def __str__(self):
        return "Command substract last two stack numbers"
		
class MultiplyLastTwoNumbersCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) < 2:
            raise ExecutionError(self, "Ran stack multiply command with less than two stack elements")
        ctx.stack.append(ctx.stack.pop() * ctx.stack.pop())

    def __str__(self):
        return "Command multiply last two stack numbers"
		
class PowerLastTwoNumbersCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) < 2:
            raise ExecutionError(self, "Ran stack power command with less than two stack elements")
        b = ctx.stack.pop()
        ctx.stack.append(pow(float(ctx.stack.pop()), float(b)))

    def __str__(self):
        return "Command power last two stack numbers"


class RemoveLastValueFromStackCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) == 0:
            return
        ctx.stack.pop()


class RemoveAllValuesFromStackCmdToken(CommandExecToken):
    def execute(self, ctx):
        ctx.stack = []


class DuplicateLastValueFromStackCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) == 0:
            raise ExecutionError(self, "Ran stack duplication command with empty stack")
        ctx.stack.append(ctx.stack[-1])


class ExitSpecifierCmdToken(CommandExecToken):
    def execute(self, ctx):
        ctx.flags |= ExecuteFlags.ExitSpecifier


class ExitParentCmdToken(CommandExecToken):
    def execute(self, ctx):
        ctx.flags |= ExecuteFlags.ExitParent


class ExitProgramCmdToken(CommandExecToken):
    def execute(self, ctx):
        ctx.flags |= ExecuteFlags.ExitProgram


class SwitchStackCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) == 0:
            raise ExecutionError(self, "Ran switch stack command with empty stack")
        if ctx.stack[-1] not in ctx.all_stacks.keys():
            ctx.create_stack(ctx.stack[-1])
        ctx.stack_index = ctx.stack.pop()


class MoveStackValCmdToken(CommandExecToken):
    def execute(self, ctx):
        if len(ctx.stack) == 0:
            raise ExecutionError(self, "Ran move stack command with empty stack")
        if ctx.stack[-1] not in ctx.all_stacks.keys():
            ctx.create_stack(ctx.stack[-1])
        ctx.all_stacks[ctx.stack.pop()].append(ctx.stack.pop())
