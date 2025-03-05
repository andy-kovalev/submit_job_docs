import random
import string


def get_random_string(length: int) -> string:
    return ''.join(random.choice(string.printable) for i in range(length))
