from .types import (
    Mean,
    Median,
    Maximum,
    Minimum,
    Count,
    StandardDeviation,
    MedianAbsoluteDeviation,
    Variance,
    Quantile
)

class StreamField:

    def __init__(self, stream=None, config=None):
        self.stream = stream
        self.metadata = {}

        if config is None:
            config = {}

        if config.get('metadata'):
            for field in config.get('metadata'):
                self.metadata[field] = config.get('metadata').get(field)

        self.stats = {
            'mean': Mean(),
            'med': Median(),
            'max': Maximum(),
            'min': Minimum(),
            'std': StandardDeviation(),
            'mad': MedianAbsoluteDeviation(),
            'var': Variance()
        }

        self.counts = {
            'TOTAL': Count(bin_name='TOTAL')
        }

        self.quantiles = {}
        self.tags = {}

        if self.metadata.get('event_tags'):
            self.tags.update(self.metadata.get('event_tags'))

        quantiles = config.get("quantiles")
        if quantiles is None:
            quantiles = [10, 25, 50, 75, 90, 95, 99]

        for quantile in quantiles:
            self.quantiles[quantile] = Quantile(quantile=quantile)

    async def update(self, metadata=None, value=None, bin_name=None):
        if metadata:
            if metadata.get('event_tags'):
                self.tags.update(
                    {
                        tag.get('name'): tag.get('value') for tag in metadata.get('event_tags')
                    }
                )
            self.metadata.update(metadata)

        if value:
            for stat in self.stats:
                await self.stats[stat].update(value)

            for quantile in self.quantiles:
                await self.quantiles[quantile].update(value)

        if bin_name:

            if bin_name not in self.counts:
                self.counts[bin_name] = Count(bin_name=bin_name)

            await self.counts.get(bin_name).update()

        await self.counts.get('TOTAL').update()

    async def get_metadata(self):
        self.metadata['event_tags'] = [{tag_name: tag_value} for tag_name, tag_value in self.tags.items()]
        return self.metadata

    async def get_stats(self, stat=None):
        stat_data = {}
        if stat:
            stat_data[stat] = await self.stats[stat].get()
            
        else:
            for stat in self.stats:
                stat_data[stat] = await self.stats[stat].get()
        return stat_data

    async def get_counts(self, count=None):
        count_data = {}
        if count:
            count_data[count] = await self.counts[count].get()

        else:
            for count in self.counts:
                count_data[count] = await self.counts[count].get()
        return count_data

    async def get_quantiles(self, quantile=None):
        quantile_data = {}
        if quantile:
            quantile_key = '{quantile}th_quantile'.format(quantile=quantile)
            quantile_data[quantile_key] = await self.quantiles[quantile].get()

        else:
            for quantile in self.quantiles:
                quantile_key = '{quantile}th_quantile'.format(quantile=quantile)
                quantile_data[quantile_key] = await self.quantiles[quantile].get()

        return quantile_data

    async def get_all(self):
        summary = {
            'metadata': await self.get_metadata(),
            'stats': await self.get_stats(),
            'counts': await self.get_counts(),
            'quantiles': await self.get_quantiles()
        }

        return summary
