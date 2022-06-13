import sqlite3
import requests
import json

def baseballSavantRequest(pk):
    #grabbingSavant info
    url = "https://baseballsavant.mlb.com/gf?game_pk="+str(pk)

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    
    return json_data

def tableSetup(path):
    #checking if path exist
    if path == None:
        path = 'dodgers.db' 
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    #checking if table exist/creating if not
    cursor.execute('''CREATE TABLE IF NOT EXISTS pitch
                (play_id TEXT PRIMARY KEY,inning INT,ab_number INT,outs INT,stand TEXT, p_throws TEXT, pitcher_name TEXT, team_batting TEXT, team_fielding TEXT, 
                result TEXT,strikes INT,balls INT,pre_strikes INT,pre_balls INT,call_name TEXT,pitch_type TEXT,start_speed INT,extension INT,zone INT,
                spin_rate INT,hit_speed INT,hit_distance INT,hit_angle INT,is_barrel INT,is_bip_out TEXT,pitch_number INT,player_total_pitches INT, game_pk INT
                )''')
    connection.commit()
    
    cursor = connection.execute('select * from pitch')
    names = list(map(lambda x: x[0], cursor.description))
    #returning column names
    return (names)

def insertinto(path,identifier,value):
    #inserting into table
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    sql= 'INSERT INTO pitch ('+identifier+') VALUES('+value+')'
    cursor.execute(sql)
    connection.commit()

    
def main(pk,path):
    if path == None:
        path = 'dodgers.db' 
    json_data=baseballSavantRequest(pk)
    names=tableSetup(path)
    
    for key in (json_data['team_home']):
        identifier=''
        value=''
        #grabbing specific info needed based on column names
        for x in names:
            try:

                if type(key[x]) == float or type(key[x]) == int:
                   
                    identifier+=x + ','
                    value+=str(key[x]) + ','
                else:
                    identifier+=x + ','
                    value+="'"+key[x]+"'" + ','
            except:
                continue

        identifier = identifier[:-1]
        value = value[:-1]
        insertinto(path,identifier,value)

        
    for key in (json_data['team_away']):
        identifier=''
        value=''
        for x in names:
            try:

                if type(key[x]) == float or type(key[x]) == int:
                  
                    identifier+=x + ','
                    value+=str(key[x]) + ','
                else:
                    identifier+=x + ','
                    value+="'"+key[x]+"'" + ','
            except:
                continue

        identifier = identifier[:-1]
        value = value[:-1]
        insertinto(path,identifier,value)
    

main(635886,'dodgers.db')