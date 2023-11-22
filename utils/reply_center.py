class Reply:
    def __init__(self, message):
        self.__hellos: list = [
            "Hi",
            "How are things",
            "G'day",
            "Howdy",
            "What's up",
            "How is it going",
            "What's happening",
            "Yo",
            "Hello",
            "It’s nice to see you again",
        ]
        self.__addressees: list = [
            "pal",
            "my friend",
            "amigo",
            "buddy",
            "comrade",
            "chum",
            "crony",
            message.from_user.first_name,
        ]
        self.__not_defined: list = [
            "Could you, please, repeat that?",
            "Could you say that again?",
            "I'm sorry, I didn't catch that!",
            "Would you mind repeating that?",
            "Do you mind repeating that?",
            "Excuse me?!",
            "Sorry?!",
            "Come again, please!",
            "Say that again, pls!",
            "Pardon?!",
            "I beg your a pardon?!",
            "This is wrong command! \N{loudly crying face}",
            "You're wrong! \N{unamused face}",
        ]
        self.__tired: list = [
            "you have to be more accurate with your typing! \U0001F928",
            "you are still wrong! \U0001F625",
            "if you're behind the wheel, just stop and type your command, pls!",
            "something's wrong with your keyboard, probably! \U0001F928",
            "stop for a second, relax and type again! \U0001F60D",
            "thing's are not that simple, but I believe in you! Type again, pls!",
        ]
        self.__help: dict = {
            # "/start": "Start weathering, start seeing the future!",
            "/my": "I'll send you the weather forecast of your favorite city (if there's one)",
            "/del": "Just remove your favorite city out of our minds for good!",
            "/change": "Yes, we can just switch to another favorite place!",
            "/wishlist": "Check it out!",
            "/add": "Add a new place to a wishlist and joy forecasting!",
            "/empty": "Just move everything out of wishlist!",
            "/remove": "Remove favorite city from your wishlist, but not out of your memory!",
            "/help": "I'll start helping you over!",
        }

    @property
    def hellos(self):
        return self.__hellos

    @property
    def addressees(self):
        return self.__addressees

    @property
    def not_defined(self):
        return self.__not_defined

    @property
    def tired(self):
        return self.__tired

    @property
    def help(self):
        return self.__help
