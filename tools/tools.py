"""module to create hash"""

from hashlib import blake2b


def create_hash(text: str) -> str:
    """return a has for a provided text"""
    return blake2b(key=bytes(text, 'utf-8'), digest_size=5).hexdigest()
