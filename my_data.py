class KeyTrainerData:
    def __init__(self):
        self.keys_en = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m"],
        ]
        self.easy_text = "Farmer Jack realized that big yellow quilts were expensive."
        self.mid_text = "Five jumping wizards hex bolty quick. Jacky can now give six big tips from the old quiz "
        self.hard_text = "She's got eyes of the bluest skies As if they thought of rain I'd hate to look into those eyes and see an ounce of pain Her hair reminds me of a warm, safe place Where, as a child, I'd hide And pray for the thunder and the rain to quietly pass me by"
        self.text_position = 0
