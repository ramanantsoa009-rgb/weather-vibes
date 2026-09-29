from pydantic import BaseModel


class Vibe(BaseModel):
    """Humeur associée à une météo : ce que le front affiche et le thème visuel à appliquer."""

    emoji: str
    message: str
    theme: str
