from statstream.streaming import StatStreamGroup
from statstream.models import (
    StreamConfig,
    Event,
    Query
)

stream = StreamConfig({
    'stream_name': 'stream_1'
})
stream_group = StatStreamGroup()

stream_group.add_stream(stream)

event = Event({
    'key': 'field_one',
    'value': 1,
    'stream_name': 'stream_1'
})

stream_group.update(event)

query = Query({
    'stream_name': 'stream_1'
})

results = stream_group.get_stream_stats(query)
print(results)

