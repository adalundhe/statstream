from zebra_statstream.streaming import StatStream
from zebra_statstream.models import (
    Event,
    Query
)

stream = StatStream()

for i in range(1, 1001):
  event = Event({
    'metadata': {
      'event_tags': [
        {
          'name': 'test_tag',
          'value': 'hello from tag number {idx}'.format(idx=i)
        }
      ],
      'additional_metadata_field': 'here is some additional metadata'
    },
    'key': 'field_one',
    'value': i
  })

  stream.update(event)

query = Query({
  'key': 'field_one'
})

stream_results = stream.get_field_stats(query)
print(stream_results)