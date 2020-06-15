from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import os
import json
import base65536

# Have put in dodgy functions so that the base library can be changed.
def ByteToString(x):
    return base65536.encode(x)

def StrToByte(x):
    return base65536.decode(x)

# Encrypt message, and return AEs key and nocne
def EncryptText(msg,key=None):
    # Generate random key if none given
    if key is None:
        key = os.urandom(16)
    aesCipher = AES.new(key, AES.MODE_EAX)
    cipherText, authTag = aesCipher.encrypt_and_digest(msg.encode())
    return cipherText,key,aesCipher.nonce

def RetweetKeyAndNonce(publicKey_target,key,nonce):
    encryptor = PKCS1_OAEP.new(publicKey_target)
    key_encrypted = encryptor.encrypt(key)
    nonce_encrypted = encryptor.encrypt(nonce)
    return key_encrypted,nonce_encrypted

# Returns privateKey,publicKey from a PEM file
def LoadKeyPairPEM(path='./personalKey.pem'):
    f = open(path,'r')
    key = RSA.import_key(f.read())
    return key.exportKey(),key.publickey().exportKey()

def LoadTargetJSON(path='./targetKeys.json'):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def DecryptRetweet(rt,personalKey):
    key_encrypted = rt.split(' ')[1]
    nonce_encrypted = rt.split(' ')[-1]
    decryptor = PKCS1_OAEP.new(personalKey)
    key = decryptor.decrypt(bytes(StrToByte(key_encrypted)))
    nonce = decryptor.decrypt(bytes(StrToByte(nonce_encrypted)))
    return key,nonce

def DecryptTweet(twt,rtwt,personalKey):
    key,nonce = DecryptRetweet(rtwt,personalKey)
    aesCipher = AES.new(key,AES.MODE_EAX,nonce=nonce)
    text = aesCipher.decrypt(StrToByte(twt))
    return text
