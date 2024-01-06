from dataclasses import dataclass


@dataclass
class Users:
    table_name: str = 'users'
    user_id: str = 'user_id'
    user_city: str = 'user_city'


@dataclass
class Favorites:
    table_name: str = 'favorites'
    favorites_user_id: str = 'favorites_user_id'
    user_favorite_city_name: str = 'user_favorite_city_name'
