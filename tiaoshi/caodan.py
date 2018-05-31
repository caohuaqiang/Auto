import re

A = 'From: 342473195@qq.com\nSubject: i am chq'
regx = '^(From|Subject|Date): .*'
B = repr(A)


if __name__ == '__main__':
    # pattern = re.compile(pattern=regx)
    # pipei = re.findall(pattern=pattern, string=A)
    # print(pipei)
    ccc = re.search(regx, A).string.split('\n')
    # for word in ccc:
    #     print(word)
    print(ccc)

