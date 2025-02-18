class KeyTrainerData:
    def __init__(self):
        self.keys_en = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m"],
        ]
        self.easy_text = ["Farmer Jack realized that big yellow quilts were expensive.",
        "The quick brown fox jumps over the lazy dog"]
        self.mid_text = ["Five jumping wizards hex bolty quick. Jacky can now give six big tips from the old quiz ",
        "Is the milk cold, or still hot? Tom hasn't had anything to eat since breakfast."]
        self.hard_text = ["She's got eyes of the bluest skies As if they thought of rain I'd hate to look into those eyes and see an ounce of pain Her hair reminds me of a warm, safe place Where, as a child, I'd hide And pray for the thunder and the rain to quietly pass me by",
        "They decided to plant a tree in the backyard to celebrate the start of spring. Your name isn't you. That is also just a letter code that identifies you. If you're one of those people who hates staying home on the weekend, check out the local bowling alley. "]
        self.text_position = 0
