#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    # we cannot delete the contents in cols, we have to set contents in cols as zeros
    c.execute("update scores set points = 0 where points != 0;")
    c.execute("update rounds set matches = 0 where matches != 0")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    # remove  all contents after delete players
    c.execute("delete from scores;")
    c.execute("delete from rounds;")
    c.execute("delete from players;")
    c.execute("ALTER SEQUENCE players_id_seq RESTART WITH 1")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    res = c.fetchall()
    db.close()
    # res is a list of tuples, so we have to return first element in first tuple
    return res[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    # have to initilize the player, scores and rounds three tables when add a new player
    c.execute("insert into players (name) values(%s);",(name,))
    c.execute("insert into scores (id, points)" \
        " values((select id from players where name = (%s)), 0);", (name,))
    c.execute("insert into rounds (id, matches)" \
        " values((select id from players where name = (%s)), 0);", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    # beacuse we only set col as zeros, so we still can get correct join after we delete matches info
    c.execute("select players.id, name, points, matches from players, scores, rounds" \
        " where players.id = scores.id and players.id = rounds.id order by points desc;")
    res = c.fetchall()
    db.close()
    return res

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    # updated three tables after report score
    c.execute("update scores set points = points + 1 where id = (%s)", (winner,))
    c.execute("update rounds set matches = matches + 1" \
        " where id = (%s) or id =(%s)", (winner, loser))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    # we sorted the players by their points 
    c.execute("select players.id, name from players, scores" \
        " where players.id = scores.id order by points desc")
    rows = c.fetchall()
    db.close()
    res = []
    # we put adjacent players into a tuple as a pair for the next match
    for i in xrange(len(rows)/2):
        res.append((rows[2*i][0], rows[2*i][1], rows[2*i+1][0], rows[2*i+1][1]))
    return res

def findChampion():
    db = connect()
    c = db.cursor()
    c.execute("select players.id, name from players, scores" \
        " where players.id = scores.id order by points desc limit 3")
    rows = c.fetchall()
    db.close()
    return rows

