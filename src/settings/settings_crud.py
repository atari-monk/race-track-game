from pathlib import Path
import tomllib
import tomli_w
from src.settings.settings import Settings

class SettingsCRUD:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self.save(Settings(fullscreen=False))

    def load(self) -> Settings:
        with self._path.open('rb') as f:
            data = tomllib.load(f)
        return Settings(fullscreen=bool(data.get('fullscreen', False)))

    def save(self, settings: Settings) -> None:
        with self._path.open('wb') as f:
            tomli_w.dump({'fullscreen': settings.fullscreen}, f)

if __name__ == '__main__':
    path = Path('settings.toml')
    crud = SettingsCRUD(path)
    
    def print_and_toggle():
        settings = crud.load()
        print(f"Current settings: {settings}")
        updated = Settings(fullscreen=not settings.fullscreen)
        crud.save(updated)
        return updated
    
    for _ in range(2):
        print_and_toggle()