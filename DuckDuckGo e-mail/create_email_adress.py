import random
import string
import os

def generate_random_alias(length=10):
    """Generate a random alias of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_duck_aliases(count, filename="duck_aliases.txt"):
    """Generate a specified number of DuckDuckGo email aliases and save them to a file."""
    
    # 8 characters is the default length of a randomly generated one-time DuckDuckGo address