"""Messaging interfaces for inter-service communication."""

from typing import Any, Awaitable, Callable, Protocol


class MessagePublisher(Protocol):
    """Protocol for publishing messages to a message queue or event bus."""
    
    async def publish(self, topic: str, message: dict[str, Any]) -> None:
        """
        Publish a message to a topic.
        
        Args:
            topic: Topic or queue name
            message: Message payload as dictionary
        """
        ...


class MessageConsumer(Protocol):
    """Protocol for consuming messages from a message queue or event bus."""
    
    async def subscribe(
        self,
        topic: str,
        handler: Callable[[dict[str, Any]], Awaitable[None]]
    ) -> None:
        """
        Subscribe to a topic and register a message handler.
        
        Args:
            topic: Topic or queue name
            handler: Callback function to handle received messages
        """
        ...
    
    async def start(self) -> None:
        """Start consuming messages."""
        ...
    
    async def stop(self) -> None:
        """Stop consuming messages."""
        ...
