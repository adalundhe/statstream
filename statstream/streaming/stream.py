from .stats.stream_field import StreamField
from statstream.models import (
    Event,
    Query
)


class StatStream:

    def __init__(self, fields=None):
        self.stream_fields = {}
        self.field_keys = set()

        if fields:
            for field_config in fields:
                field = StreamField(
                    stream=field_config,
                    config=fields.get(field_config)
                )
                
                self.stream_fields[field_config] = field

    def __iter__(self):
        for stream_field in self.stream_fields.values():
            yield stream_field.get_all()

    async def fields(self):
        for field in self.stream_fields:
            yield field

    async def update(self, event):
        if event.key not in self.field_keys:
            self.field_keys.add(event.key)
            self.stream_fields[event.key] = StreamField(stream=event.key)

        await self.stream_fields[event.key].update(
            metadata=event.metadata,
            value=event.value,
            bin_name=event.bin
        )
        return {
            'field': event.key,
            'message': 'OK'
        }

    async def get_stream_stats(self):
        stream_summary = {}
        for field_name, stats_field in self.stream_fields.items():
            stream_summary[field_name] = await stats_field.get_all()
        
        return stream_summary

    async def get_field_stats(self, query):
        return await self.stream_fields[query.key].get_all()

    async def get_field_stat(self, query):

        parital_summary = {
            'metadata': await self.stream_fields[query.key].get_metadata()
        }

        if query.type == 'stat':
            parital_summary['stats'] = await self.stream_fields[query.key].get_stats(
                stat=query.stat
            )
            

        elif query.type == 'count':
            parital_summary['counts'] = await self.stream_fields[query.key].get_counts(
                count=query.stat
            )

        elif query.type == 'quantile':
            parital_summary['quantiles'] = await self.stream_fields[query.key].get_quantiles(
                quantile=query.stat
            )

        else:
            raise Exception('Error: Query type not supported.')

        return parital_summary

    async def merge_stream(self, stream):
        for field in stream.fields():
            if self.stream_fields.get(field) is None:
                self.stream_fields[field] = stream.stream_fields.get(field)
            else:
                stream_field = stream.stream_fields.get(field)
                self.stream_fields[field].metadata.update(stream_field.metadata)

                for stat in stream_field.stats:
                    stat_value = stream_field.stats[stat].get()
                    self.stream_fields[field].stats[stat].update(stat_value)

                for quantile in stream_field.quantiles:
                    quantile_value = stream_field.quantiles[quantile].get()
                    self.stream_fields[field].quantiles[quantile].update(quantile_value)

                for count in stream_field.counts:
                    if self.stream_fields[field].counts.get(count) is None:
                        self.stream_fields[field].counts[count] = stream_field.counts.get(count)
                    else:
                        count_value = stream_field.counts[count].get()
                        self.stream_fields[field].counts[count].update(amount=count_value)


                

                    
            


