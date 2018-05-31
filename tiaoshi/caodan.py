import re

A = 'grabcy'
regx = 'gr(abc|abd)y'
B = repr(A)


if __name__ == '__main__':
    # pattern = re.compile(pattern=regx)
    # pipei = re.findall(pattern=pattern, string=A)
    # print(pipei)
    print(re.search(regx, A).group())
