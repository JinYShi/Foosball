#!/usr/bin/python3
import datetime
import time

class Match:

    def __int__(self, match_ID, time, playerList, winnerList):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.matchID = match_ID
        self.time = st
        self.playerList = playerList
        self.winnerList = winnerList
