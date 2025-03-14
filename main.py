from  dataclasses import dataclass
from io import StringIO
import fth

@dataclass
class Fstate:
    tib: str
    tibi: int
    words: dict
    ds: list
    out: StringIO

tib = '''

" hello"
"  world " + .
kv 99 ! num1 98 ! num2
@ num1
'''

def plus(s):
    s.ds[-2] += s.ds[-1]
    s.ds.pop()

def comment(s):
    s.tibi = fth.skip(s.tib, s.tibi, '\n')

def string(s):
    closing = fth.skip(s.tib, s.tibi, '"')
    s.ds.append(s.tib[s.tibi+1:closing])
    s.tibi = closing+1

class ShortRead(Exception):
    pass

def dict_set(s):
    name_start, name_end = fth.tok(s.tib, s.tibi)
    if name_start == name_end:
        raise ShortRead()
    s.tibi = name_end
    s.ds[-2] |= {s.tib[name_start:name_end]: s.ds[-1]}
    s.ds.pop()

def dict_get(s):
    name_start, name_end = fth.tok(s.tib, s.tibi)
    if name_start == name_end:
        raise ShortRead()
    s.tibi = name_end
    s.ds.append(s.ds[-1].get(s.tib[name_start:name_end]))

words = {
    '+': plus,
    '#': comment,
    '"': string,
    "!": dict_set,
    "@": dict_get,
    "kv": lambda s: s.ds.append(dict()),
    'drop': lambda s: s.ds.pop(),
    '.': lambda s: s.out.write(str(s.ds.pop())),
}

state = Fstate(tib, 0, words, [], StringIO())

class UndefinedWord(Exception):
    pass

def process_tib(s):
    while s.tibi < len(s.tib):
        start, end = fth.tok(s.tib, s.tibi)
        if start == end:
            break
        tok = s.tib[start:end]
        print(f'<{tok}> {s.tibi}')
        if tok.isdigit():
            s.ds.append(int(tok))
            s.tibi = end
        else:
            fun = s.words.get(tok)
            if fun is None:
                raise UndefinedWord(tok)
            s.tibi = end
            fun(s)



process_tib(state)
print(state.out.getvalue())
print(state.ds)

