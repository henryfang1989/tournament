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
    c.execute("delete from scores;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players;")
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
    c.execute("insert into players (name) values(%s);",(name,))
    c.execute("insert into scores (points) values(0);")
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
    b = connect()
    c = db.cursor()
    c.execute("select name, points from players, scores where players.id = scores.id order by points;")
    res = c.fetchall()
    db.close()
    return res

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    b = connect()
    c = db.cursor()
    c.execute("select points from scores where id = (%d)", (winner,))
    p = c.fetchall()[0][0] + 1
    c.execute("insert into scores (points) values (%d)", (p,))
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
    b = connect()
    c = db.cursor()
    c.execute("select players.id, name from players, scores on players.id = scores.id order by points")
    rows = c.fetchall()
    db.close()
    res = []
    for i in xrange(len(rows)/2):
        res.append((rows[i][0], rows[i][1], rows[i+1][0], rows[i+1][1]))
    return res



