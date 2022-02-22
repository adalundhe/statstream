import tdigest

class Quantile:

    def __init__(self, quantile=None):
        self.digest = tdigest.TDigest()
        self.quantile = quantile

    async def update(self, new_value):
        self.digest.update(new_value)

    async def get(self):
        if len(self.digest) > 0:
            return self.digest.percentile(self.quantile)
        else:
            return 0