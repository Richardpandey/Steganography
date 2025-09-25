# Steganography Tool - Hide Messages in Images

A secure Python tool for hiding messages and files inside images using steganography with military grade encryption. Protect your confidential data by embedding it invisibly within ordinary images.

<img width="586" height="369" alt="Screenshot 2025-09-26 at 01 55 18" src="https://github.com/user-attachments/assets/862f1090-05e4-419c-8166-5cacb4cfbba5" />

A powerful Python tool that allows you to hide secret messages and files inside images using steganography with AES encryption.

##  Features

- **Hide Text Messages**: Encode secret text into images
- **Hide Files**: Embed any type of file (documents, images, etc.) into carrier images
- **Military-Grade Encryption**: AES-256 encryption with password protection
- **Automatic Image Creation**: Generates optimal carrier images if needed
- **Extract Hidden Data**: Decode messages and files from steganographic images
- **Multiple Data Types**: Can hide both text and files simultaneously

##  Installation

### 1. Download the git file
```bash
git clone https://github.com/Richardpandey/Steganography.git
```

### 2. Move to the Directory
```bash
cd Steganography
```

### 3. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 4. Run the tool.
```bash
python3 main.py
```
## Encoding (Hiding Data)

### Encode a text message:

- Choose option 1

- Select text message (option 1)

- Provide input image or let the tool create one

- Enter your secret message

- Set a strong password

### Encode a file:

- Choose option 1

- Select file (option 2)

- Provide the file path to hide

- Set encryption password

### Encode both text and file:

- Choose option 1

- Select both options (1,2)

- Follow the prompts for both data types

### Decoding (Extracting Data)
- Decode hidden content:

- Choose option 2

- Provide the steganographic image path

- Enter the correct password

- The tool will automatically detect and extract text/files

## Disclaimer (Educational Purpose Only) 

Use responsibly and only on files you own or have permission to test. The author is not responsible for misuse.



