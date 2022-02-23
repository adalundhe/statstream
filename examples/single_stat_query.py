from statstream.streaming import StatStream
from statstream.models import Event, Query

stream = StatStream(fields={
  'field_one': {
    'metadata': {
      'event_tags': [
        {
          'name': 'test_tag',
          'value': 'hello!'
        }
      ],
      'additional_metadata_field': 'here is some additional metadata'
    }
  }
})

for i in range(1, 1001):
  event = Event({
    'key': 'field_one',
    'value': i,
    'bin': 'success'
  })

  stream.update(event)

query = Query({
  'key': 'field_one',
  'type': 'stat',
  'stat': 'med'
})

stream_results = stream.get_field_stat(query)
print(stream_results)