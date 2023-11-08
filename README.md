# Telegramm bot - WeatherBot

### Shortcut:

Weather forecast Telegramm bot with API and database.

## Functionality.

WeatherBot is a weather forecasting bot, which implements two main functionalities:

- store user's favorite city and output weather forecast by user's request;
- create and manage user's wishlist, which is a list of user's favorite places with weather forecast output followed by user's request.

Weather forecast is a data from openweathermap.org API.  
User's city and wishlist are stored in database SQLite3.

User's city forecast is shown by the user's command `/my`.  
User's wishlist is a reply-menu shown by user's command `/wishlist`. Forecast will be shown by pressing corresponding reply-button.  
If wishlist is empty or user city is not specified corresponding message will be shown.

## Main menu.

- /start - start weather forecasting
- /my - your city weather forecast
- /del - delete your city
- /change - change your city
- /wishlist - wishlist output
- /add - add place to a wish list
- /empty - clear your wishlist
- /remove - remove city from your wishlist
- /help - start helping me

## Command description and execution.

> #### 1. /start -  - start weather forecasting

***New user:***

- welcome message; 
- short description of bot functionality;
- help message;
- suggestion to add favorite city or start weather forecasting by typing a place name.

***Returned user:***

- welcome back message;
- short description of bot functionality;
- reminder of "your favorite city" and "your wishlist";
- help message.

***Current user:***

- reminder of "your favorite city" and "your wishlist";

> #### 2.  /my - your city weather forecast

Output user's city forecast. Reply menu with a forecast durations followed by forecast output based on user's choice.

> #### 3. /del - delete your city

Delete user's favorite city from database. Pre-deleting prompt message required - `Add`, `Cancel`.

> #### 4. /change - change your favorite city

Changing user's favorite city by asking user to type a new place followed by confirmation to make changes - `Change`, `Cancel`.

> #### 5. /wishlist - wishlist output

Show user's wishlist of favorite places as reply menu. Following forecast is shown after corresponding reply button press by user.

> #### 6. /add - add place to a wishlist
        
Adding new place to a user's wishlist by typing the name followed by confirmation - `Add`, `Cancel`.

> #### 7. /empty - clear your wishlist

Clear user's wishlist.  Pre-deleting prompt message required - `Clear`, `Cancel`.

> #### 8. /remove - remove city from your wishlist

Show user's wishlist as a reply menu. Pre-deleting message as reply to a message with an inline menu - `Delete`, `Cancel`.

> #### 9. /help - start helping me

Help output.

## Possible features.

- Celsius / Fahrenheit output;
- forecast output settings - varius detail and visualisation options (sets of options);
- auto messaging of current day weather at scheduled time.