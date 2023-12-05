import gzip
import shutil
from hashlib import sha256
from pathlib import Path

import dill

# NOTE:
# 1. pickleだと並列で動かした時にエラーが出るのでdill
# 2. dataは複数形、datumが単数形らしい。


class Kvs:
    def __init__(self, db_path="kvs"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)

    def get_digest(self, key):
        return sha256(bytes(key, "utf8")).hexdigest()[:24]

    def flash(self, key, datum):
        hash = self.get_digest(key)
        value = gzip.compress(dill.dumps(datum))
        with Path(self.db_path, hash).open(mode="wb") as f:
            f.write(value)

    def is_exists(self, key):
        hash = self.get_digest(key)
        if Path(self.db_path, hash).exists():
            return True
        else:
            return False

    def get(self, key):
        if self.is_exists(key) is False:
            return None
        hash = self.get_digest(key)
        with Path(self.db_path, hash).open(mode="rb") as f:
            value = f.read()
        datum = dill.loads(gzip.decompress(value))
        return datum

    def cleanup(self):
        shutil.rmtree(self.db_path, ignore_errors=True)
