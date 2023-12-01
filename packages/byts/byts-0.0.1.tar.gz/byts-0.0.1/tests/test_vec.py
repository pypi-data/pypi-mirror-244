from byts import pack, unpack

def test_pack_unpack():
    for n in range(1, 1000):
        assert n == pack(unpack(n))

    for k in range(1, 63):
        n = 2**k
        assert n == pack(unpack(n))


def test_unpack():
    for n in range(1, 1000):
        s = bin(n)[2:]
        assert s == "".join([str(i) for i in unpack(n)])[: len(s)]
