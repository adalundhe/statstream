class StreamConfig:

    def __init__(self, data):
        self.name = data.get('streamName')
        self.fields = data.get('fields')
