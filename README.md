# Hybrid-Cipher : Vigenère + Columnar Transposition

## 📜Overview
This project implements a hybrid encryption algorithm that combines:

1. Vigenère Cipher (Substitution) – A polyalphabetic cipher that shifts characters using a repeating key.
2. Columnar Transposition (Permutation) – A technique that rearranges the ciphertext into a matrix and swaps column positions.
   
This combination improves security by enhancing both confusion and diffusion, making cryptanalysis significantly harder.

## 📜Features
- ✅ 128-bit Key Strength – Uses a random 16-byte key for Vigenère encryption.
- ✅ PKCS#7 Padding – Ensures proper block alignment for transposition.
- ✅ Confusion & Diffusion – Protects against frequency analysis and known plaintext attacks.
- ✅ Secure Random Key Generation – Uses os.urandom() for cryptographic security.
- ✅ Fast Performance – Optimized with O(n log n) complexity.

## 📜Usage
### 🔑 Generate Random Encryption Keys
```python
from hybrid_cipher import generate_vigenere_key, generate_transposition_key

vigenere_key = generate_vigenere_key()  
transposition_key = generate_transposition_key(12)  
print(f"Vigenère Key: {vigenere_key.hex()}")
print(f"Transposition Key: {transposition_key}")
```
### 🔐 Encrypt a Message
```python
from hybrid_cipher import hybrid_encrypt

plaintext = "This is a secure hybrid cipher."
encrypted = hybrid_encrypt(plaintext, vigenere_key, transposition_key)
print(f"Encrypted Text (Hex): {encrypted.hex()}")
```
### 🔓 Decrypt a Message
```python
from hybrid_cipher import hybrid_decrypt

decrypted = hybrid_decrypt(encrypted, vigenere_key, transposition_key)
print(f"Decrypted Text: {decrypted}")
```

## 📝 Example Output
```python
Original Text: This is a secure hybrid cipher.
Vigenère Key: 5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d
Transposition Key: [3, 0, 4, 1, 2]
Encrypted (Hex): 7a6f9d8e3f4a5c7e6b2c...
Decrypted: This is a secure hybrid cipher.
```
## Why is this Hybrid Cipher More Secure?
🔹 Increased Key Space:
- The 128-bit Vigenère extension ensures a large key space, preventing brute-force attacks.
- The columnar transposition step introduces additional permutation complexity.  
🔹 Confusion & Diffusion Principles (Shannon’s Security Model):
- Vigenère (Substitution) adds confusion: Each character is substituted unpredictably.
- Transposition adds diffusion: The entire structure of the message changes, making pattern analysis difficult.  
🔹 Resilience Against Known Attacks:
- Prevents Frequency Analysis: Since the transposition step scrambles letter positions, letter frequency distributions are obscured.
- Prevents Key Length Detection: Traditional Kasiski examination fails because transposition disrupts repeated patterns.
