# https://topaz.github.io/paste/#XQAAAQBhBAAAAAAAAAAzHIoib6qqOe07MhJ0XsXE6K08G4Ps1pPDNRTvQl6uZZoIftzHzLmOlfUUioR8ICEiLAtwA38K1najlvr0kQFi5dXeS97tonT1Qp6fgHAE4l61QGOkLkRQOxbqEDLzw02v2equaPS9qHfOBjS5CxbZ66foOGAp70tK2sDL0DrM0SaSQ7Pxm1jLvscyTzbu9obX7t7GVcKN5VXNEIoIdioDih2w0e6lBXJiyydTVwkVGj0Z93RkzEbGePDJCpweQTzn8OSakjZ4Lfd+hJrc1Lpx/qR6ybsHcsGbxC8t5sBxrTtJLvEeg75d8uBP7GdbhMOyVwhSpfm4EJBiUMNBjQWrmbC47odTrX7IO8tjQia9bvTPCsKXjl07M1Z1HJJzZQSvoVTJNukvbb35qD2KHLN0Ji8c5BhBYE9jaifBf14I56JWpi/MhrFhmwsypbXcuZKy6n6dcySVDvjVtUnYHMddnGtDarI1ud4GkmyLACW//UnHW8UyporMDhz4bhkr90whfCq27bbRcavfN4XVCHCKeq72Hi3FmpsUqY3La59B58MQyHBpU7hMEsYeR0a4T/KfvpcV1xWnyeRC6UqCsIIPlz7Hz3oiDtjXKfnRP6Jv2zrrOlosHQIuc0uTQ7yeVJ9i1kWQtrcgj1DPbfYoTt6a+S2J4u6VBmjWQP97e8oA
# https://old.reddit.com/r/adventofcode/comments/1hg38ah/2024_day_17_solutions/m2glx6y/

from re import findall
a, b, c, *prog = [int(n) for n in findall("(\d+)", open("input.txt").read())]

def run(prog, a):
    ip, b, c, out = 0, 0, 0, []
    while ip>=0 and ip<len(prog):
        lit, combo = prog[ip+1], [0,1,2,3,a,b,c,99999][prog[ip+1]]
        match prog[ip]:
            case 0: a = int(a / 2**combo)       # adv
            case 1: b = b ^ lit                 # bxl
            case 2: b = combo % 8               # bst
            case 3: ip = ip if a==0 else lit-2  # jnz
            case 4: b = b ^ c                   # bxc
            case 5: out.append(combo % 8)       # out
            case 6: b = int(a / 2**combo)       # bdv
            case 7: c = int(a / 2**combo)       # cdv
        ip+=2
    return out
print("Part 1:", ",".join(str(n) for n in run(prog, a)))

target = prog[::-1]
def find_a(a=0, depth=0):
    if depth == len(target):
        return a
    for i in range(8):
        output = run(prog, a*8 + i)
        if output and output[0] == target[depth]:
            if result := find_a((a*8 + i), depth+1):
                return result
    return 0
print("Part 2:", find_a())