import sys

class Config:
    port: int

    def __init__(self):
        self._config()

    def _config(self):
        if len(sys.argv) > 1:
            for a in sys.argv:
                if a.startswith('-port'):
                    self.port = a.split("=")[1]

    def __str__(self) -> str:
        return f"port={self.port}"