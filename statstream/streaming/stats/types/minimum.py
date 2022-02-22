import sys

class Minimum:

    def __init__(self):
        self.current_value = sys.float_info.max

    async def update(self, new_value):
        if new_value < self.current_value:
            self.current_value = new_value

        return self

    async def get(self):
        return self.current_value