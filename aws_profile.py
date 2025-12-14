import json, os
from config import PROFILE_PATH


class PlayerProfile:
    def __init__(self, name, badges=None, total_quizzes=0, total_correct=0):
        """ A Player should have the following attributes: name, badges, total quizzes taken, and total number of questions correct."""
        self.name = name
        self.badges = badges or {}
        self.total_quizzes = total_quizzes
        self.total_correct = total_correct
    

    @classmethod
    def from_dict(cls, name, data):
        return cls(
            name = name,
            badges=data.get("badges", {}),
            total_quizzes = data.get("total_quizzes", 0),
            total_correct = data.get("total_correct", 0),
        )
    

    def to_dict(self):
        return {
            "badges": self.badges,
            "total_quizzes": self.total_quizzes,
            "total_correct": self.total_correct,
        }
    

    def record_quiz_result(self, badge_name, score, total, pass_percentage):
        """This method will return percentage and previous best score"""

        percent = (score / total) * 100 if total else 0
        self.total_quizzes += 1
        self.total_correct += score

        previous_best = self.badges.get(badge_name, {}).get("best_score", 0)
        if percent > previous_best:         # clarification note: previous_best < passing_score would mean you never earned the badge before
            self.badges[badge_name] = {"best_score": round(percent, 2)}
        return percent, previous_best



class ProfileStore:
    def __init__(self, path=PROFILE_PATH):
        self.path = path
        self._profiles = self.load_profiles()


    def load_profiles(self):
        if not os.path.exists(self.path):
            return {}
        
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    

    def save_profile(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._profiles, f, indent=2)
    

    def get_or_create_player(self, name):
        """This will return existing player profle or create a new one."""
        raw = self._profiles.get(name)
        if raw is None:
            # for new player
            profile = PlayerProfile(name)
            self._profiles[name] = profile.to_dict()
            return profile
        # for existing player: they get converted from dict to PlayerProfile object
        return PlayerProfile.from_dict(name, raw)
    

    def update_profile(self, profile):
        self._profiles[profile.name] = profile.to_dict()
        self.save_profile()