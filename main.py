import getpass
from banner import show_banner
from tool import encode_text_file, decode

def main():
    show_banner()

    print("What do you want to do?")
    print("1. Encode a message or file into an image")
    print("2. Decode a message or file from an image")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        img_path = input("Enter input image path (or leave empty to auto-create a carrier image): ").strip() or None
        output_path = input("Enter output image path (including filename, e.g., qr(encoded).png): ").strip()
        hide_choice = input("What do you want to hide? (You can choose both by typing 1,2)\n1. Text message\n2. File\nEnter choice: ").strip()

        message = None
        file_path = None

        if "1" in hide_choice:
            message = input("Enter the text message to hide: ").strip()
        if "2" in hide_choice:
            file_path = input("Enter the file path to hide: ").strip()

        password = getpass.getpass("Enter a password for encryption: ").strip()

        encode_text_file(img_path=img_path, message=message, file_path=file_path, output_path=output_path, password=password)

    elif choice == "2":
        img_path = input("Enter image path to decode: ").strip()
        password = getpass.getpass("Enter the password for decryption: ").strip()
        result = decode(img_path, password=password)
        print(result)

    else:
        print("[-] Invalid choice!")

if __name__ == "__main__":
    main()
