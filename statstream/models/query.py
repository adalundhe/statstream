class Query:

    def __init__(self, data):
        self.key = data.get('key')
        self.type = data.get('type')
        self.stat = data.get('stat')
        self.stream_name = data.get('streamName')