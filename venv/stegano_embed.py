import optparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import string
import subprocess

parser = optparse.OptionParser()
parser.add_option("-c","--covertext",dest="cover_text",help="Visible text")
parser.add_option("-m","--message",dest="message",help="hidden message text")
parser.parse_args()
(options,arguments)=parser.parse_args()
covertext = options.cover_text
message = options.message

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
\t\t\t\t\t---- Embedding Mode ----\n\n

""")


if(covertext == None or message == None):
    print("[-] Arguments Not Provided")
    exit(0)
print("[WARNING !] In Every Iteration the information required for decoding changes make sure to use latest one !")
print("[+] Encrypting Message in AES ")

def encrypt(data):
    list=[]
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    text = bytes(data,'utf-8')
    ciphertext, tag = cipher.encrypt_and_digest(text)
    nonce = cipher.nonce
    file_out = open("encrypted.bin", "wb")


    [file_out.write(x) for x in (cipher.nonce, tag, key)]
    file_out.close()
    print("[+] Message Encrypted")
    #print("[+] Your secret key is : " + str(key))
    list.append(ciphertext)
    list.append(key)
    list.append(nonce)
    list.append(tag)
    return list
return_list = encrypt(message)
ciphertext = return_list[0].hex()
key = return_list[1].hex()
# def decrypt(ciphertext):
#     ciphertext = bytearray.fromhex(ciphertext)
#     file_in = open("encrypted.bin", "rb")
#     nonce, tag, key = [file_in.read(x) for x in (16, 16, -1)]
#     cipher = AES.new(key, AES.MODE_EAX, nonce)
#     data = cipher.decrypt_and_verify(ciphertext, tag)
#     return data

# data = decrypt(ciphertext)

print("[+]  Your cover text is :    "+covertext)
print("[+]  Your secret message is :    "+message)
print("[+]  Your encrypted message is   "+ciphertext)
print("[WARNING !] Don't loose the file \"encrypted.bin\" it contains all vital information for decoding")
print("[+] Embedding in Cover Text")
def embed(cipher_text,cover_text):
    bin_ciph = ' '.join(format(ord(x), 'b') for x in cipher_text)
    #print(bin_ciph)
    #print(covertext)

    bin_ciph = bin_ciph.replace("0", "\u200d")
    bin_ciph = bin_ciph.replace("1", "\u200b")
    bin_ciph = bin_ciph.replace(" ", "\u200c")
    part1 = covertext[:1]
    part2 = covertext[1:]

    embededtext = part1
    embededtext = embededtext + bin_ciph + part2
    # print(embededtext)
    f=open("embededtext.txt","w",encoding="utf-8")
    f.write(embededtext)
    f.close()
    print("[+] Embeded text stored in file embededtext.txt")
    return embededtext
embed(ciphertext,covertext)

# print(data)
