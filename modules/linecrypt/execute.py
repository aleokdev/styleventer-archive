from .tokenbase import *
from .tokencmds import *
from . import tokenizer
from .execbase import *


def execute_specificatortype(execCtx: ExecContext, specificator_type: SpecificatorType):
    if execCtx.flags & ExecuteFlags.ExitProgram:
        return
    for token in execCtx.tokens:
        if type(token) is SpecificatorExecToken:
            if token.specificator_type == specificator_type:
                if not (execCtx.flags & ExecuteFlags.JumpToToken):
                    token.execute(execCtx)
                if execCtx.flags & ExecuteFlags.ExitProgram:
                    return
                while execCtx.flags & ExecuteFlags.JumpToToken:
                    execCtx.flags ^= ExecuteFlags.JumpToToken
                    absolute_parent = execCtx.jump_to.parent
                    while hasattr(absolute_parent, "parent"):
                        absolute_parent = absolute_parent.parent
                    if absolute_parent != token:
                        raise ExecutionError(execCtx.jump_to, "Tried to jump to token that is out of scope")
                    execCtx.jump_to.parent.execute_from(execCtx.jump_to.pc, execCtx)
                    if execCtx.flags & ExecuteFlags.ExitProgram:
                        return


def execute(program: str, prg_input: str):
    programScript = tokenizer.ProgramScript(program)
    tokens = tokenizer.parse_tokens(programScript)
    execCtx = ExecContext(tokens)
    execCtx.labels = programScript.labels

    execCtx.variables["INPUT_LENGTH"] = len(prg_input)
    execCtx.variables["VERSION"] = "1.1"
    execute_specificatortype(execCtx, SpecificatorType.Start)

    current_word = ""
    for i_char, input_char in enumerate(prg_input):
        execCtx.variables["CHAR"] = input_char
        execCtx.variables["WORD"] = current_word
        execCtx.variables["TEXT"] += input_char
        if input_char == " " or i_char == len(prg_input)-1:
            if i_char == len(prg_input)-1:
                current_word += input_char
                execCtx.variables["WORD"] = current_word
            execute_specificatortype(execCtx, SpecificatorType.Word)
            current_word = ""
        else:
            current_word += input_char

        execute_specificatortype(execCtx, SpecificatorType.Character)

    execute_specificatortype(execCtx, SpecificatorType.End)
    return execCtx
