import json
import hashlib
from datetime import datetime
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from wallet import wallets
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from binascii import unhexlify


class Transaction(object):
    __slots__ = [
        "sender",
        "receiver",
        "amount",
        "signature",
        "__signatureBytes",
        "time",
        "hash",
        "__hashObj",
        "__dict__",
    ]

    def __init__(self, sender="", receiver="", amount=0) -> None:
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = ""
        self.__signatureBytes = ""
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash, self.__hashObj = self.calculateHash()
        self.completed = False

    def calculateHash(self):
        hashString = self.sender + self.receiver + str(self.amount) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        hashed = SHA256.new(hashEncoded)
        return hashed.hexdigest(), hashed

    def parseDict(self):
        transactionDict = {}
        for attr in filter(lambda a: a.startswith("_") == False, self.__slots__):
            transactionDict[attr] = str(self.__getattribute__(attr))

        return transactionDict

    def signTransaction(self, senderKey):
        calculatedHash, _ = self.calculateHash()

        if self.sender == self.receiver:
            print("Same wallet.")
            return False

        if self.hash != calculatedHash:
            print("Transaction tampered.")
            return

        self.__signatureBytes = pkcs1_15.new(senderKey).sign(self.__hashObj)
        self.signature = self.__signatureBytes.hex()
        print("Transaction Signed.")
        return

    def completeTranfer(self):
        receiverWallet = None
        senderWallet = None

        try:
            receiverWallet = wallets.getWallet(self.receiver)
        except:
            print("No receiver wallet found.")
            return

        if self.sender != "Mine Reward":
            try:
                senderWallet = wallets.getWallet(self.sender)
            except:
                print("No sender wallet found.")
                return

        self.completed = True

    @property
    def isValid(self):
        if self.sender == "Mine Reward":
            return True

        senderWallet = None
        senderKey = None

        try:
            senderWallet = wallets.getWallet(self.sender)
            senderKey = RSA.import_key(senderWallet.publicKey)
        except:
            print("No Wallet.")
            return False

        try:
            pkcs1_15.new(senderKey).verify(self.__hashObj, self.__signatureBytes)

            if senderWallet.balance < int(self.amount):
                return False

            return True
        except Exception as e:
            print("Invalid transaction.")
            return False

    @staticmethod
    def importFromDict(array):
        parsedArray = []
        for item in array:
            transaction = Transaction()
            for key in item.keys():
                transaction.__setattr__(key, item[key])
                transaction.hash, transaction.__hashObj = transaction.calculateHash()
                transaction.__signatureBytes = unhexlify(item["signature"])
            parsedArray.append(transaction)

        return parsedArray

    @staticmethod
    def importOneFromDict(obj):
        transaction = Transaction()
        for key in obj.keys():
            transaction.__setattr__(key, obj[key])
            transaction.hash, transaction.__hashObj = transaction.calculateHash()
            transaction.__signatureBytes = unhexlify(obj["signature"])

        return transaction
