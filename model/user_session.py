class UserSession:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.password_hash = None
        self.recovery_hash = None
        self.avatar = None

    def get_uid(self):
        return self.user_id
    
    def set_user(self, user_info):
        self.user_id = user_info["user_id"]
        self.username = user_info["username"]
        self.password_hash = user_info["password_hash"]
        self.recovery_hash = user_info["recovery_hash"]
        self.avatar = user_info["avatar"]
    
    def get_user(self):
        return {"user_id": self.user_id, "username": self.username, "password_hash": self.password_hash, "recovery_hash": self.recovery_hash, "avatar":self.avatar}