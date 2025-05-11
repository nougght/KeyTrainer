import datetime as dt
from dataclasses import dataclass, field
import json, typing


@dataclass
class Session:
    time: typing.List
    chars: typing.List
    cpm: typing.List
    wpm: typing.List
    errors: typing.List
    total_chars: int
    total_errors: int
    duration: int
    avg_cpm: int
    avg_wpm: int
    max_cpm: int
    max_wpm: int


class TypingSession:
    def __init__(self):
        self.reset_stats()

    def reset_stats(self):
        self.stats = {
            "time": [1],  # метки времени
            "chars": [0],
            "cpm": [0],  # моментальная скорость
            "wpm": [0],
            "errors": [0],  # ошибки в секунду
            "start_time": 0,
            "total_chars": 0,  # общее количество символов
            "total_errors": 0,
            "duration": 0,
            "accuracy": 0,
            "avg_cpm": 0,
            "avg_wpm": 0,
            "max_cpm": 0,
            "max_wpm": 0,
            "test_type": ''
        }

    def start_session(self, type):
        self.stats["start_time"] = dt.datetime.now()
        self.stats['test_type']= type

    def add_keystroke(self, char, is_correct):
        self.stats['chars'][-1] += is_correct
        self.stats['errors'][-1] += not is_correct
        self.stats["total_chars"] += is_correct
        self.stats["total_errors"] += not is_correct

    def on_time(self):
        self.stats["cpm"][-1] = self.stats["chars"][-1] * 60
        self.stats["wpm"][-1] = self.stats["cpm"][-1] / 5

        self.stats["time"].append(self.stats["time"][-1] + 1)
        self.stats["chars"].append(0)
        self.stats["errors"].append(0)
        self.stats["cpm"].append(0)
        self.stats["wpm"].append(0)

    def finish_session(self):
        self.stats["duration"] = (dt.datetime.now() - self.stats["start_time"]).total_seconds()
        self.stats["cpm"][-1] = self.stats["chars"][-1] * 60
        self.stats["wpm"][-1] = self.stats["cpm"][-1] / 5
        self.stats["avg_cpm"] = self.stats["total_chars"] / self.stats["duration"] * 60
        self.stats["avg_wpm"] = self.stats["avg_cpm"] / 5

        self.stats["max_cpm"] = max(self.stats["cpm"])
        self.stats["max_wpm"] = max(self.stats["wpm"])
        if self.stats["total_chars"]:
            self.stats["accuracy"] = self.stats["total_chars"] / (self.stats["total_chars"] + self.stats["total_errors"])

# ts =TypingSession()
# ts.reset_stats()
# ts.start_session()
# import time
# time.sleep(5)
# ts.finish_session()
# print(ts.stats["duration"])