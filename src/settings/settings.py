from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Settings:
    fullscreen: bool

