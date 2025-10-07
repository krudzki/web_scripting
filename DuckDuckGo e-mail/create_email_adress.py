import random
import string
import os

def generate_random_alias(length=10):
    """Generate a random alias of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_duck_aliases(count, filename="duck_aliases.txt"):
    """Generate a specified number of DuckDuckGo email aliases and save them to a file."""
    
    # characters is the default length of a randomly generated one-time DuckDuckGo address
    ALIAS_LENGTH = 40
    DOMAIN = "@duck.com"

    unique_aliases = set()
    print(f"Generating {count} unique DuckDuckGo email aliases...")

    # Generate unique aliases
    while len(unique_aliases) < count:
        alias = generate_random_alias(ALIAS_LENGTH)
        # unique_aliases.add(alias + DOMAIN)
        unique_aliases.add(alias)

    # Write aliases to the specified file
    try:
        with open(filename, 'w') as file:
            for alias in unique_aliases:
                file.write(f"{alias}\n")
        print(f"Successfully saved {count} aliases to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

# --- Script usage example ---
# How many aliases to generate
NUM_ALIASES = 100
# Output file name
OUTPUT_FILE = "duck_aliases.txt"

generate_duck_aliases(NUM_ALIASES, OUTPUT_FILE)