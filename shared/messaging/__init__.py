"""Messaging package for inter-service communication."""

from shared.messaging.interfaces import MessageConsumer, MessagePublisher

__all__ = [
    "MessagePublisher",
    "MessageConsumer",
]
