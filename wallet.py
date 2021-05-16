from Crypto.PublicKey import RSA
from Crypto.Signature import *
from Crypto.Cipher import PKCS1_OAEP


class Wallet(object):
    __slots__ = [
        "address",
        "privateKey",
        "publicKey",
    ]

    def __init__(self, username="", passphrase="nonw") -> None:
        self.privateKey, self.publicKey = self.generateKeys(passphrase)
        self.address = self.generateAddress(passphrase, username)

    @property
    def balance(self):
        from chain import chain

        balance = 50
        for i in range(1, len(chain.chain)):
            if i + chain.blockValidity < len(chain.chain):
                block = chain.chain[i]
                try:
                    for j in range(0, len(block.transactions)):
                        transaction = block.transactions[j]
                        if transaction.completed == True:
                            if transaction.sender == self.address:
                                balance -= transaction.amount
                            if transaction.receiver == self.address:
                                balance += transaction.amount
                except AttributeError:
                    print("No transaction.")
        return balance

    def generateKeys(self, passphrase):
        key = RSA.generate(1024)

        return key.export_key(passphrase=passphrase).decode(
            "UTF-8"
        ), key.publickey().export_key().decode("UTF-8")

    def generateAddress(self, passphrase, username):
        key = RSA.import_key(self.privateKey, passphrase=passphrase)
        cipher_rsa = PKCS1_OAEP.new(key)

        return cipher_rsa.encrypt(username.encode()).hex().upper()

    @staticmethod
    def importFromDict(obj):
        wallet = Wallet()

        for key in obj.keys():
            print(key)
            wallet.__setattr__(key, obj[key])

        return wallet

    def parseDict(self):
        wallerDict = {}
        for attr in filter(lambda a: a.startswith("_") == False, self.__slots__):
            wallerDict[attr] = str(self.__getattribute__(attr))

        return wallerDict


class Wallets(object):
    __slots__ = [
        "wallets",
    ]

    def __init__(self) -> None:
        self.wallets = {}

    def addWallet(self, wallet):
        self.wallets[wallet.address] = wallet

    def createWallet(self, username, passphrase) -> Wallet:
        newWallet = Wallet(username, passphrase)
        self.addWallet(newWallet)
        return newWallet

    def getWallet(self, address) -> Wallet:
        return self.wallets[address]

    def importFromDict(self, obj):

        for key in obj.keys():
            temp = Wallet.importFromDict(obj[key])
            self.addWallet(temp)

    def parseDict(self):
        walletsDict = {}

        for key in self.wallets.keys():
            walletsDict[key] = self.wallets[key].parseDict()

        return walletsDict


wallets = Wallets()
