class Count:

    def __init__(self, bin_name=None):
        self.bin_name = bin_name
        self.current_value = 0

    async def update(self, amount=None):
        if amount:
            self.current_value += amount
        else:
            self.current_value += 1
        return self

    async def get(self):
        return self.current_value