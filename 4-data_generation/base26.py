from string import ascii_uppercase as alphabet

base = 26

def toCode(num):
    if 17575 < num or 0 > num:
        print 'Bad number'
        return ''
    digits = []
    while 3 > len(digits):
        if 0 == num:
            digits.append(0)
        else:
            digits.append(num % base)
            num //= base

    code = ''
    for c in reversed(digits):
        code += alphabet[c]
    return code

def fromCode(strRep):
    pos = 0
    num = 0
    for c in reversed(strRep):
        num += 26**pos * alphabet.index(c)
        pos += 1
    return num

