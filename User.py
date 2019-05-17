class User:

    def __init__(self, name):
        self.name = name
        self.friends = []

    def addFriend(self, friendName):
        self.friends.append(friendName)