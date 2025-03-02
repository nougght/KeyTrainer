from dataclasses import dataclass, field
import json, typing


@dataclass
class Profile:
    id: int
    nickname: str
    created_at: str
    settings: dict

@dataclass
class ProfilesList:
    profiles: typing.List[Profile] = field(default_factory=list)

    def add_profile(self, profile: Profile):
        self.profiles.append(profile)
    
    def remove_profile(self, profile_id: int):
        self.profiles = [prof for prof in self.profiles if prof.id != profile_id]

    def save_to_json(self):
        pass
    
    def load_from_json(self):
        pass