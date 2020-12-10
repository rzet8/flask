import string
import random
symbols = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + ['/','?', '{', '}', '[', ']']
def generate(l=32):
    token = ""
    for i in range(l+1):
        r = random.choice(symbols)
        token += r
    return token