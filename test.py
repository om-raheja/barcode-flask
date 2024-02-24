from os import urandom
from base64 import b64encode

rnd=urandom(16)
rnd_bytes=b64encode(rnd).decode('utf-8')

print(rnd_bytes)
