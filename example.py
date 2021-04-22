import sqlite3
from scipy.spatial.distance import cdist
import numpy as np


class Vector:
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return 'Vector({!r})'.format(self.arg)


def adapter_func(obj: np.ndarray):
    return obj.tobytes()


def converter_func(data: bytes):
    return np.frombuffer(data)


sqlite3.register_adapter(Vector, adapter_func)
sqlite3.register_converter(f"{Vector.__name__}", converter_func)

if __name__ == '__main__':
    with sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES) as con:
        cur = con.cursor()
        cur.execute("create table test(v vector)")
        cur.execute("insert into test(v) values (?)", (np.random.random(1280),))
        cur.execute("insert into test(v) values (?)", (np.random.random(1280),))

        cur.execute('select v from test')
        vectors = []
        for v, in cur.fetchall():
            print(v.shape, v)
            assert isinstance(v, np.ndarray)
            vectors.append(v)

        assert len(vectors) == 2
        print(cdist(vectors[:1], vectors[1:], metric='cosine')[0])

        cur.close()

