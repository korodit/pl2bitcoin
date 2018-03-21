import hashlib

# st = input()
# st="421731f"
st = int("796fae438ebdc83ac3a4e8a071d71b1f0f0eace40d8a5b92bb64b1e9ed746066",16).to_bytes(32,"big")
res = hashlib.sha256(st).digest()
# res = hashlib.sha256(res.encode("utf-8")).digest()
res = hashlib.sha256(res).hexdigest()
# res = hex(int(hashlib.sha256(res).digest(),16))
# res = hashlib.sha256(res.encode("utf-8")).hexdigest()
print(res)
# print(st)