import psycopg2

db = psycopg2.connect("dbname=tournament")
c = db.cursor()
createPlayers = "CREATE TABLE players (id serial PRIMARY KEY, name text);"
createScores = "CREATE TABLE scores (id serial REFERENCES players, points integer);"
createRounds = "CREATE TABLE rounds (id serial REFERENCES players, matches integer);"
c.execute(createPlayers)
c.execute(createScores)
c.execute(createRounds)
db.commit()
db.close()