import random


def hex_to_bin(a): #16转12
    m = ''
    for i in a:
        m = m + hex(i)[2:]
    return m


def tianchong(message):  # padding
    m = bin(int(message, 16))[2:]
    while len(m) != len(message) * 4:
        m = '0' + m
    a = '0' * (64 - len(bin(len(m))[2:])) + bin(len(m))[2:]
    m = m + '1'
    m = m + '0' * (448 - len(m) % 512) + a
    m = hex(int(m, 2))[2:]
    return m


def leftshift(s, l):
    l = l % 32
    return (((s << l) & 0xFFFFFFFF) | ((s & 0xFFFFFFFF) >> (32 - l)))


def FF(s1, s2, s3, i):
    if i >= 0 and i <= 15:
        return s1 ^ s2 ^ s3
    else:
        return ((s1 & s2) | (s1 & s3) | (s2 & s3))


def GG(s1, s2, s3, i):
    if i >= 0 and i <= 15:
        return s1 ^ s2 ^ s3
    else:
        return ((s1 & s2) | (~s1 & s3))


def P0(s):
    return s ^ leftshift(s, 9) ^ leftshift(s, 17)


def P1(s):
    return s ^ leftshift(s, 15) ^ leftshift(s, 23)


def T(i):
    if i >= 0 and i <= 15:
        return 0x79cc4519
    else:
        return 0x7a879d8a


def ls_(m):
    M = []
    for a in range(int(len(m) / 128)):
        M.append(m[128 * a:128 * (a + 1)])
    return M


def message_extension(M, n):
    W = []
    W1 = []
    for j in range(16):
        W.append(int(M[n][0 + 8 * j:8 + 8 * j], 16))
    for j in range(16, 68):
        W.append(P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ leftshift(W[j - 13], 7) ^ W[j - 6])
    for j in range(64):
        W1.append(W[j] ^ W[j + 4])
    s1 = ''
    s2 = ''
    for x in W:
        s1 += (hex(x)[2:] + ' ')
    for x in W1:
        s2 += (hex(x)[2:] + ' ')
    return W, W1


def message_compress(V, M, i):
    A, B, C, D, E, F, G, H = V[i]
    W, W1 = message_extension(M, i)
    for j in range(64):
        SS1 = leftshift((leftshift(A, 12) + E + leftshift(T(j), j % 32)) % (2 ** 32), 7)
        SS2 = SS1 ^ leftshift(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W1[j]) % (2 ** 32)
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) % (2 ** 32)
        D = C
        C = leftshift(B, 9)
        B = A
        A = TT1
        H = G
        G = leftshift(F, 19)
        F = E
        E = P0(TT2)

    a, b, c, d, e, f, g, h = V[i]
    V1 = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]
    return V1


def randomnum(n):
    rn = []
    while len(rn) < n:
        i = random.randint(0, pow(2, 64))
        if i not in rn:
            rn.append(i)
    return rn


def lengthextension_attack(m, IV, n):
    for i in range(n):
        m = '0' + m
    M = tianchong(m)
    M1 = ls_(M)
    h = SM3(M1, IV)
    return h


def SM3(M, IV):
    n = len(M)
    V = []
    V.append(IV)
    for i in range(n):
        V.append(message_compress(V, M, i))
    return V[n]


IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
ls = []
r1 = '987654321987654321'
r2 = '123456789123456789'
ls.append(hex_to_bin(SM3(ls_(tianchong(r1)), IV)))  # SM3(r1||padding,IV)
M1 = ls_(tianchong(tianchong(r1) + r2))
ls.append(hex_to_bin(SM3(ls_(tianchong(tianchong(r1) + r2)), IV)))  # SM3(r1||padding||r2,IV)
ls.append(hex_to_bin(lengthextension_attack(r2, SM3(ls_(tianchong(r1)), IV), 128)))  # SM3(r2,SM3(r1||padding))
if ls[1] == ls[2]:
    print("succeeded!")
