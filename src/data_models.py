import dataclasses
import copy # Still needed for shallow copy of the Manifest object

@dataclasses.dataclass
class Manifest:
    """
    The manifest data model, containing only the window title.
    """
    window_title: str = "Default AI Jig" # Default value if not found or file is missing

    @classmethod
    def from_dict(cls, data: dict) -> 'Manifest':
        """
        Instantiates a Manifest object from a dictionary.
        Provides a default for 'window_title' if missing in the data.
        """
        return cls(
            window_title=data.get("window_title", "Default AI Jig")
        )

    def to_dict(self) -> dict:
        """
        Converts the Manifest object to a dictionary.
        """
        return dataclasses.asdict(self)
