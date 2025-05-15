import string

def mod_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def affine_encrypt(text, a, b):
    alphabet = string.ascii_lowercase.replace(" ", "")  # Loại bỏ khoảng trắng
    m = len(alphabet)
    encrypted_text = ""
    for char in text:
        if char in alphabet:
            x = alphabet.index(char)
            encrypted_text += alphabet[(a * x + b) % m]
        else:
            encrypted_text += char  # Giữ nguyên khoảng trắng
    return encrypted_text

def affine_decrypt(text, a, b):
    alphabet = string.ascii_lowercase.replace(" ", "")
    m = len(alphabet)
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        raise ValueError("Không tìm được nghịch đảo modular của a")
    decrypted_text = ""
    for char in text:
        if char in alphabet:
            y = alphabet.index(char)
            decrypted_text += alphabet[(a_inv * (y - b)) % m]
        else:
            decrypted_text += char  # Giữ nguyên khoảng trắng
    return decrypted_text

# Dữ liệu đầu vào
plaintext = "hoc vien ktqs".replace(" ", "")  # Loại bỏ khoảng trắng

# Khóa mã hóa
a, b = 17, 21

# Mã hóa
ciphertext = affine_encrypt(plaintext, a, b)
print(f"Bản mã: {ciphertext}")

# Giải mã
decrypted_text = affine_decrypt(ciphertext, a, b)
print(f"Giải mã: {decrypted_text}")
