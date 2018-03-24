import secrets
import hashlib

# magic = int("4217"+("0"*60),16)
# magic = "c988"
def find_bitcoin(magic_number):

    initial = ""
    value = 0
    found  = False
    while not found:
        n = secrets.randbits(256)
        ba = n.to_bytes(32,"big")
        res = hashlib.sha256(ba).digest()
        res = hashlib.sha256(res).hexdigest()
        if res[:4] == magic_number:
            initial = "{0:0{1}x}".format(n,64)
            # rs = res
            value = int(res[4:8],16)
            found = True
    return (initial,value)

if __name__ == "__main__":
    while True:
        magic = input("Give 4 digit hex magic number::> ")
        if (len(magic) != 4):
            continue
        try:
            temp = int(magic,16)
        except ValueError:
            break
        initial,value = find_bitcoin(magic)
        print(" This is the bitcoin:")
        print("  "+initial)
        print(" With value {} cents".format(value))