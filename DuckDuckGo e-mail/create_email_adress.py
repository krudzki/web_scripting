import random
import string
import os

def generate_random_alias(length=10):
    """Generate a random alias of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))