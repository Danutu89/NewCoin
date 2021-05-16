from Crypto.Hash import SHA256


class MerkleHash(object):
    def __init__(self, items) -> None:
        self.items = items

    def calculate(self):
        blocks = []
        blocksLen = 0
        blocksSecondary = []
        blocksSecondaryLen = 0

        for item in sorted(self.items):
            blocks.append(item)

        blocksLen = len(blocks)
        while blocksLen % 2 != 0:
            blocks.extend(blocks[:1])
            blocksLen = len(blocks)

        for k in [blocks[x : x + 2] for x in range(0, blocksLen, 2)]:
            blocksSecondary.append(SHA256.new((k[0] + k[1]).encode()).hexdigest())

        blocksSecondaryLen = len(blocksSecondary)

        if blocksSecondaryLen <= 1:
            return blocksSecondary[0][0:64]

        else:
            self.items = blocksSecondary
            return self.calculate()
