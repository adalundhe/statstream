import math
from .variance import (
    Variance
)

class StandardDeviation:

    def __init__(self):
        self.variance = Variance()

    async def update(self, new_value):
        await self.variance.update(new_value)
        return self

    async def get(self):
        return math.sqrt(await self.variance.get())

        