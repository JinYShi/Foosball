#!/usr/bin/python3

import os,re
from flask import Flask, render_template, session, make_response
import sqlite3
from flask import g
from flask import request
from flask import Flask, url_for,redirect
import datetime
import time

app = Flask(__name__)

#=================================================================
#database settle down
#=================================================================

def connect_db():
    return sqlite3.connect('foosball.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

#========================================================================
# Main API function
#========================================================================


@app.route('/', methods=['GET','POST'])
def begin():
    print("hey")
    re = request.form.get('record', '')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("time: "+st)
    team1_player1 = request.form.get('team1_player1', '')
    team1_player2 = request.form.get('team1_player2', '')
    team1_player3 = request.form.get('team1_player3', '')
    team1_player4 = request.form.get('team1_player4', '')
    team2_player1 = request.form.get('team2_player1', '')
    team2_player2 = request.form.get('team2_player2', '')
    team2_player3 = request.form.get('team2_player3', '')
    team2_player4 = request.form.get('team2_player4', '')
    team1win = request.form.get('team1win', '')
    team2win = request.form.get('team2win', '')
    print("team1_player1 "+team1_player1)
    print("team1_player2 "+team1_player2)
    print("team1_player3 "+team1_player3)
    print("team1_player4 "+team1_player4)
    print("team2_player1 "+team2_player1)
    print("team2_player2 "+team2_player2)
    print("team2_player3 "+team2_player3)
    print("team2_player4 "+team2_player4)
    if team1win != "":
        team1win = int(team1win)
    else:
        team1win = 0
    if team2win != "":
        team2win = int(team2win)
    else:
        team2win= 0
    print("t1: "+str(team1win))
    print("t2: "+str(team2win))

    if re == "true":
        checkPlayer = checkPlayerInput([team1_player1, team1_player2, team1_player3, team1_player4,
                                  team2_player1, team2_player2, team2_player3, team2_player4])
        print("heihei "+str(checkPlayer))
        if checkPlayer == False:
            return render_template('unsuccess.html')

        match_id = createMatch()
        if team1win != team2win:
            if team1_player1 != "":
                doRecodMatch(team1_player1, team1win, match_id)
            if team1_player2 != "":
                doRecodMatch(team1_player2, team1win, match_id)
            if team1_player3 != "":
                doRecodMatch(team1_player3, team1win, match_id)
            if team1_player4 != "":
                doRecodMatch(team1_player4, team1win, match_id)
            if team2_player1 != "":
                doRecodMatch(team2_player1, team2win, match_id)
            if team2_player2 != "":
                doRecodMatch(team2_player2, team2win, match_id)
            if team2_player3 != "":
                doRecodMatch(team2_player3, team2win, match_id)
            if team2_player4 != "":
                doRecodMatch(team2_player4, team2win, match_id)
        else:
            if team1_player1 != "":
                doRecodMatch(team1_player1, 2,match_id)
            if team1_player2 != "":
                doRecodMatch(team1_player2, 2, match_id)
            if team1_player3 != "":
                doRecodMatch(team1_player3, 2, match_id)
            if team1_player4 != "":
                doRecodMatch(team1_player4, 2, match_id)
            if team2_player1 != "":
                doRecodMatch(team2_player1, 2, match_id)
            if team2_player2 != "":
                doRecodMatch(team2_player2, 2, match_id)
            if team2_player3 != "":
                doRecodMatch(team2_player3, 2, match_id)
            if team2_player4 != "":
                doRecodMatch(team2_player4, 2, match_id)
        g.db.commit()
        return render_template('success.html')
    return render_template('home.html')

@app.route('/#record', methods=['GET','POST'])
def record():
    return render_template('record.html')

@app.route('/search', methods=['GET','POST'])
def search():
    return render_template('search.html')

@app.route('/result', methods=['GET','POST'])
def result():
    player1 = request.form.get('player1', '')
    player2 = request.form.get('player2', '')
    check = checkWinRateInput([player1,player2])
    if check == False:
        return render_template('unsuccess_winrate.html')
    compare = False
    users = list()
    if player2 != '' and player1 != '':
        compare = True
        user1 = getUserbyID(player1)
        user2 = getUserbyID(player2)
        win_rate1 = getWinRate(user1[2],user1[3])
        win_rate2 = getWinRate(user2[2],user2[3])
        users.append({
            "player_name" : user1[1],
            "win_rate" : win_rate1
            })
        users.append({
            "player_name" : user2[1],
            "win_rate" : win_rate2
        })
    else:
        users=list()
        if player1 == '' and player2 == '':
            return render_template('unsuccess_winrate.html')
        if player1 != '':
            user = getUserbyID(player1)
            win_rate = getWinRate(user[2],user[3])
            users.append({
                "player_name" : user[1],
                "win_rate" : win_rate
                })
        if player2 != '':
            user = getUserbyID(player2)
            win_rate =getWinRate(user[2],user[3])
            users.append({
                "player_name" : user[1],
                "win_rate" : win_rate
                })
    if player1 == player2 and len(users)>1:
        users.pop()
        compare = False
    print(compare)
    print(users)
    return render_template('result.html',compare=compare,ulist= users)

###############################helper function #################################
#helper function for winrate
def getWinRate(win, total):
    if total ==0 :
        return 0
    return win/total
#helper function for update match detail
def doRecodMatch(playerstr, win, match_id):
    user_id = checkUser(playerstr)
    print("userid is "+str(user_id))
    updateMatch(match_id, user_id, win)
    updateUserState(playerstr, win)


# helper function to check if the input is in correct mode
# also check for the format of input
def checkPlayerInput(playerlist):
    is_exist1 = False
    for player in playerlist[0:3]:
        if player != '':
            is_exist1 = True
            break
    is_exist2 = False
    for player in playerlist[4:7]:
        if player != '':
            is_exist2 = True
            break
    if not is_exist1 or not is_exist2:
        return False
    for player in playerlist:
        m = re.match(r'[0-9]+\-[a-zA-Z]+',player)
        print("heh")
        if not m and player != '':
            return False
    return True

#check for the correct input for win rate
def checkWinRateInput(playerlist):
    for player in playerlist:
        if player != '':
            user = getUserbyID(player)
            if not user:
                return False

    for player in playerlist:
        m = re.match(r'[0-9]+',player)
        print("heh")
        if not m and player != '':
            return False
    return True

#check if the user is in the database, if not, insert a new one
def checkUser(user):
    l = user.split("-")
    id = l[0]
    name = l[1]
    user = getUserbyID(id)
    print(user)
    if user :
        return user[0]
    g.db.execute('INSERT INTO Users (user_ID,user_name,num_win,num_total) VALUES (?,?,?,?)', [str(id),name, 0,0])
    # g.db.commit()
    return id

#update the user match detail in table User
def updateUserState(user,state):
    l = user.split("-")
    id = l[0]
    user = getUserbyID(id)
    print("get a user",)
    print(user)
    if user:
        user_ID = user[0]
        num_win = user[2]
        num_total = user[3]
        print("going to update "+str(user_ID)+" state "+str(state))
        if state == 1:
            g.db.execute('UPDATE Users SET num_win=? WHERE user_ID=?', [num_win+1, user_ID])
            # g.db.commit()

        g.db.execute('UPDATE Users SET num_total=? WHERE user_ID=?', [num_total + 1, user_ID])
        return
        # g.db.commit()
    return

#helper function for getting a user by userID
def getUserbyID(id):
    print(id)
    cur = g.db.execute('select user_ID,user_name, num_win, num_total from Users where user_ID=?',[id])
    user = cur.fetchall()
    if user :
        print(user[0])
        return user[0]
    else:
        return

# create a new match with an unique ID
def createMatch():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cur = g.db.execute("select match_ID from Match where match_ID = (SELECT MAX(match_ID) FROM Match)")
    match_ID = cur.fetchall()
    print(match_ID)
    if match_ID:
        new_ID = int(match_ID[0][0]) + 1
    else:
        new_ID = 0
    g.db.execute('INSERT INTO Match (match_ID,match_time) VALUES (?,?)', [new_ID, st])
    # g.db.commit()

    return new_ID

# update the match detail table with state 0-lose,1-win,2-even
def updateMatch(match_ID, user_ID, state):
    g.db.execute('INSERT INTO Match_state (match_ID,user_ID,state) VALUES (?,?,?)', [match_ID,user_ID,state])
    # g.db.commit()
    return



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
