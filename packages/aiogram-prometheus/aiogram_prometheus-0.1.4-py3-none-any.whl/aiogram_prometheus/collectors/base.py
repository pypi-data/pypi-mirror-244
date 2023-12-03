import logging

from prometheus_client.registry import Collector

logger = logging.getLogger('app')


class BaseAiogramCollector(Collector):
    prefix: str
    collect_ids: bool

    def __init__(self, prefix: str = 'aiogram_', collect_ids: bool = False) -> None:
        self.prefix = prefix
        self.collect_ids = collect_ids
