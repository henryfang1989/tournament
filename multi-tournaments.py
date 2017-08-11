from tournament import *
import random
import math

# define method to display standings
def showStandings():
	standings = playerStandings()
	for i, standing in enumerate(standings):
		print("%2d : %9d, %9s, %9d, %9d" 
			%(i+1, standing[0], standing[1], standing[2], standing[3]))

# clean up all info in database
deleteMatches()
deletePlayers()

# set the number of players
numPlayers = 16

# register all players
for i in xrange(numPlayers):
	registerPlayer("player" + str(i+1))

# display play standing before tournament
print("Standings before tournament")
showStandings()

# finish all matches
for i in xrange(int(math.log(numPlayers, 2))):
	pairs = swissPairings()
	for playerID1, name1, playerID2, name2 in pairs:
		winner = random.choice([playerID1, playerID2])
		loser = playerID2 if winner == playerID1 else playerID1
		reportMatch(winner, loser)
	print("Standings after %d matches" % (i+1))
	showStandings()

# print 1st, 2nd and 3rd players
players = findChampion()
for i, player in enumerate(players):
	print("%2d : %9d, %9s" %(i+1, player[0], player[1]))







