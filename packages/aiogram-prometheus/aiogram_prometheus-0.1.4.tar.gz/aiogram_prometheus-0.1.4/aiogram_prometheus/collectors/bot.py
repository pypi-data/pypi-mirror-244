import logging
from typing import Any, Iterable, Optional

from aiogram import Bot
from aiogram.methods import Response, SendMessage, TelegramMethod
from prometheus_client import Counter, Histogram
from prometheus_client.metrics_core import InfoMetricFamily, Metric
from aiogram_prometheus.collectors.base import BaseAiogramCollector

logger = logging.getLogger('app')


class BotAiogramCollector(BaseAiogramCollector):
    bot: Bot

    def __init__(self, bot: Bot, prefix: str = 'aiogram_') -> None:
        super().__init__(prefix)
        self.bot = bot

    def collect(self) -> Iterable[Metric]:
        bot_user = self.bot._me

        if bot_user is None:
            return

        yield InfoMetricFamily(
            f'{self.prefix}_bot',
            'Info about bot',
            {
                'id': str(self.bot.id),
                'username': str(bot_user.username),
                'is_bot': str(bot_user.is_bot),
                'first_name': str(bot_user.first_name),
                'last_name': str(bot_user.last_name),
                'language_code': str(bot_user.language_code),
                'is_premium': str(bot_user.is_premium),
                'added_to_attachment_menu': str(bot_user.added_to_attachment_menu),
                'can_join_groups': str(bot_user.can_join_groups),
                'can_read_all_group_messages': str(bot_user.can_read_all_group_messages),
                'supports_inline_queries': str(bot_user.supports_inline_queries),
                'parse_mode': str(self.bot.parse_mode),
                'disable_web_page_preview': str(self.bot.disable_web_page_preview),
                'protect_content': str(self.bot.protect_content),
            },
        )


class SendedMessagesAiogramCollector(BaseAiogramCollector):
    prefix: str
    messages_counter: Counter

    def __init__(self, prefix: str = 'aiogram_', collect_ids: bool = False) -> None:
        super().__init__(prefix, collect_ids)

        self.messages_counter = Counter(
            f'{self.prefix}_sended_messages',
            'Aiogram`s sended messages',
            self.labels,
            registry=None,
        )

    @property
    def labels(self):
        if self.collect_ids:
            return ['bot_id', 'bot_username', 'chat_id']

        return ['bot_id', 'bot_username']

    def add_messages(self, bot: Bot, message: SendMessage):
        labels = [
            bot.id,
            getattr(bot._me, 'username', 'None'),
        ]

        if self.collect_ids:
            labels += [
                message.chat_id,
            ]

        self.messages_counter.labels(*labels).inc()

    def collect(self) -> Iterable[Metric]:
        yield from self.messages_counter.collect()


class SessionMiddlewareAiogramCollector(BaseAiogramCollector):
    prefix: str
    requests_histogram: Histogram
    LABELS = ['method_type', 'bot_username', 'error']

    def __init__(self, prefix: str = 'aiogram_') -> None:
        super().__init__(prefix)

        self.sended_messages_collector = SendedMessagesAiogramCollector()

        self.requests_histogram = Histogram(
            f'{self.prefix}_requests',
            'Aiogram`s requests',
            self.LABELS,
            registry=None,
        )

    def add_request(
        self,
        bot: Bot,
        method: Optional[TelegramMethod[Any]],
        response: Optional[Response[Any]],
        executing_time: float,
        error: Optional[BaseException] = None,
    ):
        labels = [
            method.__class__.__name__,
            getattr(bot._me, 'username', 'None'),
            error.__class__.__name__,
            'None',
            'None',
        ]

        if response is not None:
            labels = [
                method.__class__.__name__,
                getattr(bot._me, 'username', 'None'),
                error.__class__.__name__,
                # response.ok,
                # response.error_code,
            ]

        self.requests_histogram.labels(*labels).observe(executing_time)

        if isinstance(method, SendMessage):
            self.sended_messages_collector.add_messages(bot, method)

    def collect(self) -> Iterable[Metric]:
        yield from self.requests_histogram.collect()
        yield from self.sended_messages_collector.collect()
