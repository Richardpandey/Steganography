from PIL import Image
import os
import math
import base64
import hashlib
from cryptography.fernet import Fernet

# ---------------------------
# Encryption / Decryption
# ---------------------------
def generate_key(password: str) -> bytes:
    """Generate a Fernet key from a password (SHA256)."""
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_data(data: bytes, password: str) -> bytes:
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(data: bytes, password: str) -> bytes:
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(data)

# ---------------------------
# Encoding
# ---------------------------
def encode_text_file(img_path=None, message=None, file_path=None, output_path="output.png", password="secret"):
    combined_bits = ""

    # Encode text with encryption
    if message:
        encrypted_text = encrypt_data(message.encode(), password)
        text_header = f"TEXT:{len(encrypted_text)}###"
        combined_bits += ''.join([format(ord(c), '08b') for c in text_header])
        combined_bits += ''.join([format(b, '08b') for b in encrypted_text])

    # Encode file with encryption
    if file_path:
        if not os.path.isfile(file_path):
            print("[-] File does not exist!")
            return
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_data = f.read()
        encrypted_file = encrypt_data(file_data, password)
        file_header = f"FILE:{file_name}:{len(encrypted_file)}###"
        file_header_bits = ''.join([format(ord(c), '08b') for c in file_header])
        file_data_bits = ''.join([format(b, '08b') for b in encrypted_file])
        combined_bits += file_header_bits + file_data_bits

    total_bits = len(combined_bits)

    # Load image or auto-create
    if img_path:
        img = Image.open(img_path)
        capacity = img.width * img.height * 3
        if total_bits > capacity:
            print("[*] Original image too small. Creating a larger blank carrier image...")
            img = create_image_for_data(total_bits)
    else:
        img = create_image_for_data(total_bits)

    _encode_bits(img, combined_bits, output_path)

def create_image_for_data(total_bits):
    required_pixels = math.ceil(total_bits / 3)
    side = math.ceil(math.sqrt(required_pixels))
    print(f"[*] Creating new blank image {side}x{side} to fit all data...")
    return Image.new("RGB", (side, side), color=(255, 255, 255))

def _encode_bits(img, binary_data, output_path):
    encoded = img.copy()
    data_index = 0
    for y in range(encoded.height):
        for x in range(encoded.width):
            pixel = list(encoded.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_data):
                    pixel[i] = pixel[i] & ~1 | int(binary_data[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
    encoded.save(output_path)
    print(f"[+] Data encoded and saved to {output_path}")

# ---------------------------
# Decoding
# ---------------------------
def decode(img_path, password="secret"):
    if not os.path.isfile(img_path):
        return "[-] Image file does not exist!"

    img_dir = os.path.dirname(img_path)
    img = Image.open(img_path)
    binary_data = ""

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    results = []
    i = 0

    # Decode text
    decoded_text = ""
    while i + 8 <= len(binary_data):
        char = chr(int(binary_data[i:i+8], 2))
        decoded_text += char
        i += 8
        if decoded_text.endswith("###"):
            break

    if decoded_text.startswith("TEXT:"):
        try:
            text_length = int(decoded_text.replace("TEXT:", "").replace("###", ""))
            encrypted_text_bits = binary_data[i:i+text_length*8]
            encrypted_text_bytes = bytearray()
            for j in range(0, len(encrypted_text_bits), 8):
                encrypted_text_bytes.append(int(encrypted_text_bits[j:j+8], 2))
            decrypted_text = decrypt_data(bytes(encrypted_text_bytes), password).decode()
            results.append(f"[+] Hidden text message: {decrypted_text}")
            i += text_length*8
        except Exception as e:
            results.append("[-] Failed to decrypt text (wrong password?)")

    # Decode file
    remaining_bits = binary_data[i:]
    file_marker = ''.join([format(ord(c), '08b') for c in "FILE:"])
    start_index = remaining_bits.find(file_marker)
    if start_index != -1:
        all_bytes = [remaining_bits[i:i+8] for i in range(start_index, len(remaining_bits), 8)]
        header_text = ""
        for byte in all_bytes:
            header_text += chr(int(byte, 2))
            if "###" in header_text:
                break
        header_clean = header_text.split("###")[0]
        parts = header_clean.split(":")
        if len(parts) == 3 and parts[0] == "FILE":
            file_name = parts[1]
            file_length = int(parts[2])
            start_file_bits = start_index + len(header_text)*8
            file_bits = remaining_bits[start_file_bits:start_file_bits+file_length*8]
            file_bytes = bytearray()
            for j in range(0, len(file_bits), 8):
                file_bytes.append(int(file_bits[j:j+8], 2))
            try:
                decrypted_file = decrypt_data(bytes(file_bytes), password)
                output_file_path = os.path.join(img_dir, file_name)
                with open(output_file_path, "wb") as f:
                    f.write(decrypted_file)
                results.append(f"[+] File automatically extracted: {output_file_path}")
            except Exception:
                results.append("[-] Failed to decrypt file (wrong password?)")

    if not results:
        return "[-] No hidden data found in this image."
    return "\n".join(results)
