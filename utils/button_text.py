from dataclasses import dataclass


@dataclass
class ButtonSigns:
    cancel: str = "\U0000274C Cancel"
    setting_location: str = "\U0001F3E1 Set location"
    adding_location: str = "\U0001F3E1 Add location"
    set_favorite_location: str = "\U00002705 Set"
    add_wishlist_location: str = "\U00002705 Add"
    changing_location: str = "\U0001F3E1 Change location"
    change_favorite_location: str = "\U00002705 Change"
