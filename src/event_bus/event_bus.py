from typing import Callable, Dict, List, TypeVar, Any

T = TypeVar('T')

class EventBus:
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[..., None]]] = {}
    
    def on(self, event_type: str) -> Callable[[Callable[..., None]], Callable[..., None]]:
        def decorator(listener: Callable[..., None]) -> Callable[..., None]:
            self.subscribe(event_type, listener)
            return listener
        return decorator
    
    def subscribe(self, event_type: str, listener: Callable[..., None]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
    
    def unsubscribe(self, event_type: str, listener: Callable[..., None]) -> None:
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)
            if not self._listeners[event_type]:
                del self._listeners[event_type]
    
    def publish(self, event_type: str, *args: Any, **kwargs: Any) -> None:
        listeners = self._listeners.get(event_type, [])
        for listener in listeners[:]:
            listener(*args, **kwargs)
    
    def once(self, event_type: str, listener: Callable[..., None]) -> None:
        def wrapper(*args: Any, **kwargs: Any) -> None:
            self.unsubscribe(event_type, wrapper)
            listener(*args, **kwargs)
        self.subscribe(event_type, wrapper)

if __name__ == "__main__":
    bus = EventBus()

    @bus.on("click")
    def handle_click(x: int, y: int):
        print(f"Clicked at ({x}, {y})")

    bus.publish("click", 100, 200)