# coding: utf-8
import re

def nchars(n, s):
    assert n > 0
    reg = re.compile("(.)\\1{1,}")
    while True:
        m = reg.search(s)
        if not m: break
        print(m.group(0))
        s = s[m.end():]

def main():
    s = "あああいうええええおaabcdefdef"
    nchars(1, s)

main()
