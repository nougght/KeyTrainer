from dataclasses import dataclass, field
import json
import random

@dataclass
class Text:
    id: int
    language: str
    length: str
    difficulty: str
    content: str


# Модель для списка текстов
@dataclass
class TextList:
    texts: list[Text] = field(default_factory=list)

    def add_text(self, text: Text):
        self.texts.append(text)

    def remove_text(self, text_id: int):
        self.texts = [text for text in self.texts if text.id != text_id]

    def filter_by_lang_diff(self, language: str, difficulty: str):
        return [text for text in self.texts if text.language == language and text.difficulty == difficulty]

    def get_random_text(self, language: str, difficulty: str):
        texts = self.filter_by_lang_diff(language, difficulty)
        return texts[random.randint(0, len(texts) - 1)].content
    
    # def find_by_id(self, text_id: int) -> Text:
    #     return next((text for text in self.en_texts if text.id == text_id), None)

    def save_to_json(self, file_path: str):
        data = {
            "texts": [
                {
                    "id": text.id,
                    "language": text.language,
                    "content": text.content,
                    "difficulty": text.difficulty,
                    "length": text.length
                }
                for text in self.texts
            ]
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_from_json(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.texts = [
            Text(
                id=text["id"],
                language=text["language"],
                content=text["content"],
                difficulty=text["difficulty"],
                length=text["length"]
            )
            for text in data["texts"]
        ]
