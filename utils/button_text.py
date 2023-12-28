from dataclasses import dataclass


@dataclass
class ButtonSigns:
    cancel: str = "\U0000274C Cancel"
    setting_location: str = "\U0001F3E1 Set location"
    set_favorite_location: str = "\U00002705 Set"
    add_location: str = "\U00002705 Add"
