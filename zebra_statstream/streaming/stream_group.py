from .stream import StatStream


class StatStreamGroup:

    def __init__(self, streams=None):
        if streams is None:
            streams = []

        stream_group = {}

        for stream in streams:
            stream_name = stream.get('stream_name')
            stream_group[stream_name] = StatStream(
                fields=stream.get('fields')
            )

        self.streams = stream_group

    def __iter__(self):
        for stream in self.streams:
            yield stream

    async def add_stream(self, stream_config):
        if self.streams.get(stream_config.name) is None:
            self.streams[stream_config.name] = StatStream(
                fields=stream_config.fields
            )

    async def update(self, event):
        return await self.streams[event.stream_name].update(event)

    async def get_stream_stats(self, query):
        return await self.streams[query.stream_name].get_stream_stats()

    async def get_field_stats(self, query):
        return await self.streams[query.stream_name].get_field_stats(query)

    async def get_field_stat(self, query):
        return await self.streams[query.stream_name].get_field_stat(query)

    async def merge(self, stream_group, stream_name=None):
        stream = stream_group.streams.get(stream_name)
        await self.streams[stream_name].merge_stream(stream)
        return self.streams
        

