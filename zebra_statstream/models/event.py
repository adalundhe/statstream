class Event:

    def __init__(self, data):
        self.metadata = data.get('metadata')
        self.key = data.get('key')
        self.value = data.get('value')
        self.bin = data.get('bin')
        self.stream_name = data.get('streamName')

    
        