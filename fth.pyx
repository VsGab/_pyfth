def tok(str tib, int crnt):
    while crnt < len(tib) and ord(tib[crnt]) < 33:
        crnt += 1
    cdef int tok_start = crnt
    while crnt < len(tib) and ord(tib[crnt]) > 32:
        crnt += 1
    return tok_start, crnt

def skip(str tib, int crnt, str c):
    while crnt < len(tib) and tib[crnt] != c[0]:
        crnt += 1
    return crnt
