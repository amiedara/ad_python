import re, string
from django.conf import settings

if not settings.configured:
    settings.configure(
    )


def encode(val):
    if type(val) == int:
        return b'i' + str(val).encode() + b'e'
    elif type(val) == str:
        val = val.encode()
        return str(len(val)).encode() + b':' + val
    elif type(val) == list:
        return list_encode(val, b'l')
    elif type(val) == dict:
        return dict_encode(val)
    elif type(val) == bytes:
        return str(len(val)).encode() + b':' + val
    else:
        raise TypeError


def list_encode(val, ch):
    res = ch
    for i in val:
        res += encode(i)
    return res + b'e'


def dict_encode(val):
    result = []
    for k, v in val.items():
        result.append(k)
        result.append(v)
    return list_encode(result, b'd')


def decode(val):
    def decode_rec(val):
        if val.startswith(b'i'):
            find_str = re.match(b'i(-?\d+)e', val)
            return int(find_str.group(1)), val[find_str.span()[1]:]
        elif val.startswith(b'l') or val.startswith(b'd'):
            result = []
            rest = val[1:]
            while not rest.startswith(b'e'):
                elem, rest = decode_rec(rest)
                result.append(elem)
            rest = rest[1:]
            if val.startswith(b'l'):
                return result, rest
            else:
                return {i: j for i, j in zip(result[::2], result[1::2])}, rest
        elif (val.startswith(i.encode()) for i in string.digits):
            m = re.match(b'(\d+):', val)
            leng = int(m.group(1))
            rest_i = m.span()[1]
            start = rest_i
            end = rest_i + leng
            return val[start:end], val[end:]

        else:
            raise TypeError

    if isinstance(val, str):
        val = val.encode()

    a, b = decode_rec(val)
    if b:
        raise TypeError
    return a
