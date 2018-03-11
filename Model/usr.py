#!/usr/bin/python3

class User:

    def __int__(self,user_ID,user_name):
        self.user_ID = user_ID
        self.user_name = user_name
        self.num_win = 0
        self.num_total = 0
        # a new user is initialized
        print("new user: "+user_name+" "+user_ID)

    def winner(self):
        self.num_total += 1
        self.num_win += 1

    def loser(self):
        self.num_total += 1
