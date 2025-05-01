class UserSession:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.avatar = None
    
    def set_user(self, user_info):
        self.user_id = user_info["user_id"]
        self.username = user_info["username"]
        self.avatar = user_info["avatar"]
    
    def get_user(self):
        return {"user_id": self.user_id, "username": self.username, "avatar":self.avatar}