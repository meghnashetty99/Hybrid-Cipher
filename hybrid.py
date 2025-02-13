import os
from typing import List
import random

def generate_vigenere_key() -> bytes:
    return os.urandom(16)

def generate_transposition_key(num_columns: int) -> List[int]:
    permutation = list(range(num_columns))
    os.urandom(num_columns)  # Seed PRNG
    random.shuffle(permutation)
    return permutation

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_length = block_size - (len(data) % block_size)
    if pad_length == 0:
        pad_length = block_size
    return data + bytes([pad_length] * pad_length)

def pkcs7_unpad(data: bytes) -> bytes:
    pad_length = data[-1]
    if pad_length < 1 or pad_length > len(data) or not all(b == pad_length for b in data[-pad_length:]):
        raise ValueError("Invalid padding")
    return data[:-pad_length]

def vigenere_encrypt(plaintext: bytes, key: bytes) -> bytes:
    key_bytes = key * (len(plaintext) // len(key) + 1)
    encrypted = bytes((p + k) % 256 for p, k in zip(plaintext, key_bytes))
    return encrypted

def vigenere_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    key_bytes = key * (len(ciphertext) // len(key) + 1)
    decrypted = bytes((c - k) % 256 for c, k in zip(ciphertext, key_bytes))
    return decrypted

def transposition_encrypt(data: bytes, permutation: List[int]) -> bytes:
    num_columns = len(permutation)
    padded_data = pkcs7_pad(data, num_columns)
    num_rows = len(padded_data) // num_columns
    matrix = [padded_data[i*num_columns : (i+1)*num_columns] for i in range(num_rows)]
    ciphertext = bytes(matrix[row][col] for col in permutation for row in range(num_rows))
    return ciphertext

def transposition_decrypt(ciphertext: bytes, permutation: List[int]) -> bytes:
    num_columns = len(permutation)
    if len(ciphertext) % num_columns != 0:
        raise ValueError("Ciphertext length must be a multiple of column count")
    num_rows = len(ciphertext) // num_columns
    inverse_perm = [0] * num_columns
    for idx, col in enumerate(permutation):
        inverse_perm[col] = idx
    matrix = [ciphertext[i*num_rows : (i+1)*num_rows] for i in range(num_columns)]
    decrypted = bytes(matrix[inverse_perm[col]][row] for row in range(num_rows) for col in range(num_columns))
    return pkcs7_unpad(decrypted)

def hybrid_encrypt(plaintext: str, vigenere_key: bytes, transposition_key: List[int]) -> bytes:
    plaintext_bytes = plaintext.encode("utf-8")
    vigenere_result = vigenere_encrypt(plaintext_bytes, vigenere_key)
    transposed_result = transposition_encrypt(vigenere_result, transposition_key)
    return transposed_result

def hybrid_decrypt(ciphertext: bytes, vigenere_key: bytes, transposition_key: List[int]) -> str:
    transposed_result = transposition_decrypt(ciphertext, transposition_key)
    vigenere_result = vigenere_decrypt(transposed_result, vigenere_key)
    return vigenere_result.decode("utf-8")

if __name__ == "__main__":
    plaintext = "This is Hybrid"
    vigenere_key = generate_vigenere_key()
    transposition_key = generate_transposition_key(12)  # 12 columns → 12! ≈ 2^29 permutations

    print(f"Original Text: {plaintext}")
    print(f"Vigenère Key (hex): {vigenere_key.hex()}")
    print(f"Transposition Key: {transposition_key}")

    encrypted = hybrid_encrypt(plaintext, vigenere_key, transposition_key)
    print(f"Encrypted (hex): {encrypted.hex()}")

    decrypted = hybrid_decrypt(encrypted, vigenere_key, transposition_key)
    print(f"Decrypted: {decrypted}")
