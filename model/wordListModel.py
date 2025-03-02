import json, random, typing
from dataclasses import dataclass, field

@dataclass
class WordList:
    # источники:
    # oxford 3000 - https://github.com/jnoodle/English-Vocabulary-Word-List/tree/master
    # нкря (первые 6000) - https://ru.wiktionary.org/wiki/%D0%9F%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5:%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%87%D0%B0%D1%81%D1%82%D0%BE%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8_%D0%BF%D0%BE_%D0%9D%D0%9A%D0%A0%D0%AF:_%D0%A3%D1%81%D1%82%D0%BD%D0%B0%D1%8F_%D1%80%D0%B5%D1%87%D1%8C_1%E2%80%941000
    languages: typing.Dict[str, typing.List[str]] = field(default_factory=dict)

    def add_word(self, lang: str, word: str):
        self.languages[lang].append(word)

    def save_to_json(self, file_path: str):
        data = {
            "languages": {
                lang : [word 
                    for word in lang_words
                ]
                for lang, lang_words in self.languages.items()
            }
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_from_json(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.languages = data['languages']

    def get_random_word(self, language):
        return self.languages[language][random.randint(0, len(self.languages[language]))]

    def gen_text(self, language, length):
        words = self.languages[language]
        return ' '.join(random.choices(words, k=length))


# # Пример загрузки
# word_collection = WordList()
# word_collection.load_from_json("./data/words.json")
# print(word_collection.get_random_word("russian"))
# for language, lst in word_collection.languages.items():
#     print(language)
#     for word in lst:
#         print('\t'+word)
#     print()

# c = 0
# with open("./data/ru.txt", "r", encoding="utf-8") as file:
#     word = file.readline()
#     while word:
#         c += 1
#         print(word)
#         word_collection.add_word("russian", word[:-1])
#         word = file.readline()
# print(c)
# word_collection.save_to_json("./data/words.json")
