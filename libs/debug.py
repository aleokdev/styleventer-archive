import inspect
import os


logFormat = "[{name}] {msg}"

__raw_print = print

def log(*args, **kwargs):
    callerfunc = inspect.stack()[1]
    __raw_print(logFormat.format(name=os.path.basename(callerfunc.filename), msg=" ".join([str(i) for i in args])))

print = log