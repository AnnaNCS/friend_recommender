#!/usr/bin/env python3

from User import User
class SocialNetwork:

    def __init__(self):
        '''Constructor; initialize an empty social network
        '''
        self.users = {}

    def list_users(self):
        '''List all users in the network

        Returns:
            [str]: A list of usernames
        '''
        userList = []
        for user in self.users:
            userList.append(user)
        return userList


    def add_user(self, user):
        '''Add a user to the network

        This user will have no friends initially.

        Arguments:
            user (str): The username of the new user

        Returns:
            None
        '''
        self.users[user] = User(user)

    def add_friend(self, user, friend):
        '''Adds a friend to a user

        Note that "friends" are one-directional - this is the equivalent of
        "following" someone.

        If either the user or the friend is not a user in the network, they
        should be added to the network.

        Arguments:
            user (str): The username of the follower
            friend (str): The username of the user being followed

        Returns:
            None
        '''
        try:
            userObj = self.users[user]
        except Exception as e:
            userObj = User(user)
            self.users[user] = userObj

        try:
            friendObj = self.users[friend]
        except Exception as e:
            friendObj = User(friend)
            self.users[friend] = friendObj

        userObj.friends.append(friendObj)



    def get_friends(self, user):
        '''Get the friends of a user

        Arguments:
            user (str): The username of the user whose friends to return

        Returns:
            [str]: The list of usernames of the user's friends

        '''

        friendsList = []
        for friend in self.users[user].friends:
            friendsList.append(friend.name)
        return friendsList

    def suggest_friend(self, user):
        '''Suggest a friend to the user

        See project specifications for details on this algorithm.

        Arguments:
            user (str): The username of the user to find a friend for

        Returns:
            str: The username of a new candidate friend for the user
        '''
        score = {}
        friendsList = []
        #print("__"*10)
        #print(user)
        #print("__"*10)
        for friend in self.users[user].friends:
            friendsList.append(friend.name)
        ## score users : Start
        for otherUser in self.users:
            names = []
            if otherUser != user:
                for name in self.users[otherUser].friends:
                    names.append(name.name)
                intersection = len(list(set(friendsList).intersection(names)))
                union = (len(friendsList) + len(names)) - intersection
                score[otherUser] = float(intersection / union)
        #print(score)
        ## score users : end

        ## create list with potential recommends : start
        maxIndex = score[max(score, key=score.get)]
        simUsersFriends = []
        for friendUser in score:
            if score[friendUser] == maxIndex:
                #print(friendUser, maxIndex)
                for friend in self.users[friendUser].friends:
                    if (friend.name not in simUsersFriends) and \
                            (friend.name not in friendsList) and (friend.name != user):
                        simUsersFriends.append(friend.name)
        #print(simUsersFriends)
        if len(simUsersFriends) == 0:
            return None #if 'if' statement goes through, after none the program stops

        ## create list with potential recommends : end

        ## score recommends : start
        scoreFriends = {}

        for friend in simUsersFriends:
            scoreFriends[friend] = len(self.users[friend].friends)

        #print(scoreFriends)
        recommendation = max(scoreFriends, key=scoreFriends.get)

        ## score recommends : end
        return recommendation

    def to_dot(self):
        result = []
        result.append('digraph {')
        result.append('    layout=neato')
        result.append('    overlap=scalexy')
        for user in self.list_users():
            for friend in self.get_friends(user):
                result.append('    "{}" -> "{}"'.format(user, friend))
        result.append('}')
        return '\n'.join(result)


def create_network_from_file(filename):
    '''Create a SocialNetwork from a saved file

    Arguments:
        filename (str): The name of the network file

    Returns:
        SocialNetwork: The SocialNetwork described by the file
    '''
    network = SocialNetwork()
    with open(filename) as fd:
        for line in fd.readlines():
            line = line.strip()
            users = line.split()
            network.add_user(users[0])
            for friend in users[1:]:
                network.add_friend(users[0], friend)
    return network


def main():
    network = create_network_from_file('simple.network')
    print(network.to_dot())
    print(network.suggest_friend('francis'))

if __name__ == '__main__':
    main()
