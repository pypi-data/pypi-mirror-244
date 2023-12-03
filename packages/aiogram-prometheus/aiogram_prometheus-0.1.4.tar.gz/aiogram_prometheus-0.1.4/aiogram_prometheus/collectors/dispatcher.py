import logging
from typing import Iterable, Optional

import aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message, TelegramObject
from prometheus_client import Counter, Histogram
from prometheus_client.metrics_core import GaugeMetricFamily, InfoMetricFamily, Metric
from aiogram_prometheus.collectors.base import BaseAiogramCollector

logger = logging.getLogger('app')


class DispatcherAiogramCollector(BaseAiogramCollector):
    dp: Dispatcher

    def __init__(self, dp: Dispatcher, prefix: str = 'aiogram_') -> None:
        self.dp = dp
        self.prefix = prefix

        self.aiogram_info_metric = InfoMetricFamily(
            'aiogram',
            'Info about aiogram',
            value={
                'version': aiogram.__version__,
                'api_version': aiogram.__api_version__,
            },
        )

        self.dispatcher_info_metric = InfoMetricFamily(
            f'{self.prefix}_dispatcher',
            'Info about aiogram dispatcher',
            value={
                # 'version': self.dp.errors,
                # 'api_version': aiogram.__api_version__,
            },
        )

    def collect(self) -> Iterable[Metric]:
        yield self.aiogram_info_metric

        c = GaugeMetricFamily(
            f'{self.prefix}_observers',
            'Aiogram`s Dispatcher`s observers',
            labels=['name'],
        )

        c.add_metric(['shutdown'], len(self.dp.shutdown.handlers))
        c.add_metric(['startup'], len(self.dp.startup.handlers))

        for observer_name, observer in self.dp.observers.items():
            c.add_metric([observer_name], len(observer.handlers))

        yield c

        yield InfoMetricFamily(
            f'{self.prefix}_fsm',
            'Info about aiogram`s dispatcher`s fsm',
            {
                'storage': self.dp.fsm.storage.__class__.__name__,
                'strategy': self.dp.fsm.strategy.__class__.__name__,
                'events_isolation': str(self.dp.fsm.events_isolation),
            },
        )


class ReceivedMessagesAiogramCollector(BaseAiogramCollector):
    prefix: str
    messages_counter: Counter

    def __init__(self, prefix: str = 'aiogram_', collect_ids: bool = False) -> None:
        super().__init__(prefix, collect_ids)

        self.messages_counter = Counter(
            f'{self.prefix}_received_messages',
            'Aiogram`s received messages',
            self.labels,
            registry=None,
        )

    @property
    def labels(self):
        if self.collect_ids:
            return ['bot_id', 'bot_username', 'is_audio', 'is_file', 'is_reply', 'chat_id', 'sender_id']

        return ['bot_id', 'bot_username', 'is_audio', 'is_file', 'is_reply']

    def add_messages(self, bot: Bot, message: Message):
        labels = [
            bot.id,
            getattr(bot._me, 'username', 'None'),
            'is_audio' if message.audio is not None else 'no_audio',
            'is_file' if message.media_group_id is not None else 'no_file',
            'is_reply' if message.reply_to_message is not None else 'no_reply',
        ]

        if self.collect_ids:
            labels += [
                message.chat.id,
                message.from_user.id,
            ]

        self.messages_counter.labels(*labels).inc()

    def collect(self) -> Iterable[Metric]:
        yield from self.messages_counter.collect()


class MessageMiddlewareAiogramCollector(BaseAiogramCollector):
    prefix: str
    events_histogram: Histogram

    def __init__(self, prefix: str = 'aiogram_', collect_ids: bool = False) -> None:
        super().__init__(prefix, collect_ids)

        self.received_messages_collector = ReceivedMessagesAiogramCollector(self.prefix, self.collect_ids)

        self.events_histogram = Histogram(
            f'{self.prefix}_events',
            'Aiogram`s events',
            self.labels,
            registry=None,
        )

    @property
    def labels(self):
        if self.collect_ids:
            return ['bot_id', 'bot_username', 'event_type', 'status', 'chat_id', 'sender_id']

        return ['bot_id', 'bot_username', 'event_type', 'status']

    def add_event(self, event: TelegramObject, executing_time: float, error: Optional[BaseException]):
        labels = [
            event.bot.id,
            getattr(event.bot._me, 'username', 'None'),
            event.__class__.__name__,
            error.__class__.__name__,
        ]

        if self.collect_ids:
            labels += [event.chat.id, event.from_user.id]

        if isinstance(event, Message):
            self.received_messages_collector.add_messages(event.bot, event)

        self.events_histogram.labels(*labels).observe(executing_time)

    def collect(self) -> Iterable[Metric]:
        yield from self.events_histogram.collect()
        yield from self.received_messages_collector.collect()
