import  optparse
import binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import string
import subprocess
parser = optparse.OptionParser()
parser.add_option("-e","--embeded_text",dest = "embeded_text",help="Embeded text")
parser.add_option("-f","--file",dest="file_path",help="Enter encrypted.bin file path [Example :- ../../encrypted.bin]")
(options,arguments)=parser.parse_args()

embeded_text = options.embeded_text
file_path = options.file_path


subprocess.call(["clear"])

print(""" 
  _____              _              _      _____  _                              _   __        
 |  __ \            (_)            | |    / ____|| |                            (_) / _|       
 | |__) |_ __  ___   _   ___   ___ | |_  | (___  | |_  ___   __ _   __ _  _ __   _ | |_  _   _ 
 |  ___/| '__|/ _ \ | | / _ \ / __|| __|  \___ \ | __|/ _ \ / _` | / _` || '_ \ | ||  _|| | | |
 | |    | |  | (_) || ||  __/| (__ | |_   ____) || |_|  __/| (_| || (_| || | | || || |  | |_| |
 |_|    |_|   \___/ | | \___| \___| \__| |_____/  \__|\___| \__, | \__,_||_| |_||_||_|   \__, |
                   _/ |                                      __/ |                        __/ |
                  |__/                                      |___/                        |___/ 
""")
print("""\n\n
\t\t\t\t\t---- Extraction Mode ----\n\n

""")

if(embeded_text == None or file_path == None):
    print("[-]  Arguments Not Provided")
    exit(0)

print("[+]  Extracting Cipher Message")


def extract(emdebed_text):
    embededtext=embeded_text
    # print("-->"+embededtext)
    embededtext = embededtext.replace("\u200b", "1")
    embededtext = embededtext.replace("\u200d", "0")
    embededtext = embededtext.replace("\u200c", " ")
    # print("binary-->",embededtext)
    cipher_message = str(embededtext[1:])
    # print(cipher_message)
    # print(type(cipher_message))
    cipher_message1="b"
    for i in cipher_message:
        if i!='0' and i!='1' and i!=' ':
            break;
        else :
            cipher_message1=cipher_message1+i
    # print(cipher_message1)
    cipher_message1=cipher_message1[1:]
    # print(cipher_message1)
    ciph_list=cipher_message1.split(" ")
    # print(ciph_list)

    sample = "s"

    for i in ciph_list:
        binary = '0b'+i
        n=int(binary,2)
        out= n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        sample= sample+out

    sample=sample[1:]
    # sample = sample.strip()
    a= sample
    # print(a)
    return a


cipher=extract(embeded_text)
print("[+]  Extraction Successful ")
print("[+]  Cipher Text is:  "+cipher)
#print(file_path)
print("[+]  Decrypting Cipher using AES")

def decrypt(ciphertext,file_path):
    ciphertext = bytearray.fromhex(ciphertext)
    file_in = open(file_path, "rb")
    nonce, tag, key = [file_in.read(x) for x in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data

data = str(decrypt(cipher,file_path))
print("[+]  Decryption Successful!")
data=data[2:]
data=data[:-1]
print("[+]  Your secret Message is :"+data)
