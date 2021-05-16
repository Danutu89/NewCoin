from rpc import get_clients, BroadCast, start_server
from transaction import *
from block import *
import sys
import multiprocessing
import rpc
from node import *
import inspect

MODULES = ["account", "tx", "blockchain", "miner", "node"]


def upper_first(string):
    return string[0].upper() + string[1:]


class Node:
    def add(self, args):
        add_node(args[0])
        rpc.BroadCast().add_node(args[0])
        print("Allnode", get_nodes())

    def run(self, args):
        if args[0] == "127.0.0.1:5001":
            from wallet import wallets

            wallets.importFromDict(
                {
                    "479FE4FB377A2C6BE6C1B7D2B7C926734D4996D12F69335127C98A5B7BDA7E75574C211CA4A9B2F83595C728CD0F24C4F670F93826A8A2D5D1EF69AC872D2AC4BF127B579704F27A14656B013C8D10A69A6913B5C957F061E3E0BA048FF6BA76565724D3AD2FF037D18202F611452AF1289E841B060BD5BCFA5CCBF2F9E2D12B": {
                        "address": "479FE4FB377A2C6BE6C1B7D2B7C926734D4996D12F69335127C98A5B7BDA7E75574C211CA4A9B2F83595C728CD0F24C4F670F93826A8A2D5D1EF69AC872D2AC4BF127B579704F27A14656B013C8D10A69A6913B5C957F061E3E0BA048FF6BA76565724D3AD2FF037D18202F611452AF1289E841B060BD5BCFA5CCBF2F9E2D12B",
                        "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: DES-EDE3-CBC,78746D89818B9649\n\ndmKvZSIa8VaxUSHtFay4LerGBqy7HdavkufQWvweNwUiTSp0hcne+TpTMFi17dwl\nqtMc+LzJjsYSsz6VX4b9rgS6YvW1ucv5bDwkvefCAxKLHsSstKJ2CYwW9W33fzj1\nVn0cIhRjDzB4ypnYOV15xiSX46uE+aWAOc+tk9DDJwX7iheEd6do+Qvo/LQyLgM0\nu4OdpmhkEGZUwkNVuui3m+AMTe9qTbZUCqIRxDtMRjHxRaMW6fxJjkjME4N4ivs5\n2SOC1qs+TeePaLNDbXB+h4HxiP0AYeZYPqx688uN7jTWVH9ijtN/KiplVMbk5X8l\nFEjRO3Iw+T0rZNy7qpblAW9lbNhyZzyHbh/EOcvB0KOKSCS5lW3r1Rgcpi1C0Rqj\ny6CnT/TjTB8ScWTeY5C8P9ffbxk6NEm9+5lJgI48mGn0WkCRxdbc9ppyX20d0Jer\nbiKxurtHdQR65hdD+satz5unoiSeaqHCbP2ZdrjUB6jyPTh5u6Kfd3qQQ9qRntnp\nCAYH82f4xUhk0ckCi+1gWyqTo4lLYZWiAN5K67uIjvZ6cGNk38FdCdOOGpEKWURP\nuhs846tNCUWAB7gwOI7O+vTIjzf+jRGUUceSbim6H9CZ4yzRXKYXH2N9iR6UhfIZ\n5EOdA+/l89xkN6uAincBb7VeGmyWHRX+sWHcDTShPbTBC577aZ5pO2VqCTKHz3C5\ndDbtcetP6tyaW2qoZJyboOWxcHEulqxsBgraIESTqzz4eRIzZoy6hf6wZ7CJE5xg\nIH1RYhQX2A0JyNBXfRozz+QdkFQfa95g5d0NVeJ8mft17u4PkmkBXA==\n-----END RSA PRIVATE KEY-----",
                        "publicKey": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxoyKb4u2TNr+8DxTzQQcSCnA3\nk1DkYO3UYIVcMuayf/gJIvYuPKkRVMAq/kAMLQr167A/KOI4RT3Y7g3w5aPfzSRd\nfT4kid2VWhhj4Jo+NMmCKLWnIWUxb0gIjrbJcPGzsTYp3RDzcjlMAaX/IA4hsURn\nxRqbqnhotqVZL5RSdwIDAQAB\n-----END PUBLIC KEY-----",
                    },
                    "2330F7E77DC99C7F1BC5167020203A7B4E5FD58362810AB5225EAC080155D4743693591F38F6260CD05987C5BDA83681585886968B20F8D26DE7DA4DFBF4851B7B57BF5E44CCA27C86AB7F8A4523C87B45E54C78A115DDB836B7C21CB75CEACE2D3D9805E0AD99B8D00B58D47F5D50F48D550812B7B673CA96F012921DA46B23": {
                        "address": "2330F7E77DC99C7F1BC5167020203A7B4E5FD58362810AB5225EAC080155D4743693591F38F6260CD05987C5BDA83681585886968B20F8D26DE7DA4DFBF4851B7B57BF5E44CCA27C86AB7F8A4523C87B45E54C78A115DDB836B7C21CB75CEACE2D3D9805E0AD99B8D00B58D47F5D50F48D550812B7B673CA96F012921DA46B23",
                        "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: DES-EDE3-CBC,CC12E9B5B7DD13D4\n\nGlm0YpFr89Map6X/sLxJaTV6Q0rv39PE9B669SbYSiC+EFZjzMKILkjUxX8NcUfi\n2HImEaCXVfJVFXu7MFgQ7ZOP7TkSY42+7Xt/jlutnnQ64N41qvoYUrE9YhCO5hSz\n6z5Y2Te1tg2sakZ5FrraBF7NcjYXy1tTD5PslDeJvckLfK0hURXfzb43zQi4tNd9\nLcool8aK10KeyUEgCxOzRxKj8WfIP8GMMTtW35jCnUOepXu+bIIjwRAhSysPfXep\no0yMUfvFNJKs222ggB825KiXUP/bxWQWKihr6QmiHJrv4peghm4YaIQaIgJdlioT\ni0pEAmKIKMO2SoqRd6mSmy+Eziw1haIv6nc3h/N7suiXr+9Lw7516RHCm5F7OPTj\nW0duMjXkS1aNuxVBXTiYG9NUpJhfQcqgBqd2WU21t9NN2pJRxWL2pgZRKFluJ7MM\nxtQzQXtyjQ28qZiKhdmsFBZLDxlSoA4PH6nRFSHBFc6t9u0B4Vp8V9tKnpwTmeee\nz9VXqrJ5fY+CHOO99Em2B4gzgDB+C6RXe59yx5VHZZ4lPTWC99xl0Vo00cQ7/C/v\npIlU+iDI3bibGP+5ZVSpJSlH2+r/wBbqHbUKrXTb6B8iVl76FgLUtVonPftflb4c\n3Y21fXWjKpTjR+LwPKIQT4kUQTgMyttPR0Ue34llWTDOQj0OPTzypfCKig3w/9Nt\nMLuntpvJRsOCnh7R384X7deGgSxxyGMusLmcYg+ExpL5IkhyHVm28vQahPw2xxpi\nyEMPeSAJvvwrkEAzZcDD/9HBJ4i/BxeJAsNEPvL8Q410bery4dvHlg==\n-----END RSA PRIVATE KEY-----",
                        "publicKey": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDetmU4Yv/kSPOcoWlb404ez9r+\nUle3BG5kCnLrCHY7YXsxPvyh1vlxXbNHxvHvNCJz8/oTASsfWdjhH/47RaRvu2Qd\nl9dh3nGNRM6mchokR6ENfgnEwu2puuTxl966KynlYsOBZkp3zBu+jVjH9aGmnrax\nvA+8hIKVYFVl5iqSfwIDAQAB\n-----END PUBLIC KEY-----",
                    },
                }
            )
        start_node(args[0])

    def list(self, args):
        return []


class Miner:
    def start(self, args):
        if args[1] == None:
            print("ERROR", "Please create account before start miner.")
            exit()
        start_node(args[0])
        # while True:/
        chain.mine(args[1])


class Account:
    def create(self, args):
        wallet = wallets.createWallet(args[0], args[1])
        print("Private Key", wallet.privateKey)
        print("Public Key", wallet.publicKey)
        print("Address", wallet.address)
        rpc.BroadCast().add_account(wallet.parseDict())

    # def get(self, args):
    #     cprint('All Account',AccountDB().read())

    # def current(self, args):
    #     cprint('Current Account', get_account())


class Blockchain:
    def list(self, args):
        pass


class Tx:
    def list(self, args):
        pass

    def transfer(self, args):
        start_node(args[4])
        transaction = chain.addTransaction(args[0], args[1], args[2], args[3])
        rpc.BroadCast().new_transaction(transaction.parseDict())


def usage(class_name):
    module = globals()[upper_first(class_name)]
    print("  " + class_name + "\r")
    print("    [action]\r")
    for k, v in module.__dict__.items():
        if callable(v):
            print("      %s" % (k,))
    print("\r")


def help():
    print("Usage: python console.py [module] [action]\r")
    print("[module]\n")
    for m in MODULES:
        usage(m)


if __name__ == "__main__":

    if len(sys.argv) == 1:
        help()
        exit()
    module = sys.argv[1]
    if module == "help":
        help()
        exit()
    if module not in MODULES:
        print(
            "Error",
            "First arg shoud in %s"
            % (
                str(
                    MODULES,
                )
            ),
        )
        exit()
    mob = globals()[upper_first(module)]()
    method = sys.argv[2]

    getattr(mob, method)(sys.argv[3:])
