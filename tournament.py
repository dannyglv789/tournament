#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import bleach 
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.close()
    """Remove all the match records from the database."""


def deletePlayers():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()
    """Remove all the player records from the database."""


def countPlayers():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("SELECT COUNT(player_id) FROM players")
    results = c.fetchone()
    print results
    db.close()
    return results[0]
    """Returns the number of players currently registered."""


def registerPlayer(name):
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    our_clean_content = bleach.clean(name, strip=True)
    c.execute("INSERT into players(player_name) values (%s)", (our_clean_content,))
    db.commit()
    db.close()
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    '''c.execute("CREATE VIEW player_wins AS SELECT players.player_id, \
               players.player_name, COUNT(matches.winner) as num_wins from \
               players left join matches on players.player_id = matches.winner \
               GROUP BY player_id ORDER BY num_wins desc")
    
    c.execute("CREATE VIEW total_matches AS SELECT players.player_id, \
               COUNT(matches.match_id) AS matches_played \
               FROM players join matches on players.player_id \
               = matches.winner or players.player_id = matches.loser GROUP BY player_id")

    c.execute("CREATE VIEW our_standings AS SELECT player_wins.player_id, player_name, num_wins, coalesce(total_matches.matches_played,0) AS matches \
               FROM player_wins left join total_matches on player_wins.player_id = total_matches.player_id ORDER BY num_wins desc") '''
    
    c.execute("SELECT * FROM our_standings")
    db.commit()
    results = c.fetchall()
    print "PLAYER ID - PLAYER NAME - WINS - MATCHES"
    for i in results:
        print i
    db.close()
    return results
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


def reportMatch(winner, loser):
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("INSERT into matches(winner, loser) VALUES(%s, %s)", (winner, loser))
    db.commit()
    # results = c.fetchall()
    db.close()
    # return results
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swissPairings():
    standings = playerStandings()
    pairs = []
    for row in standings:
        pair = (standings[0][0],standings[0][1],standings[1][0],standings[1][1])
        pair_2 = (standings[2][0],standings[2][1],standings[3][0],standings[3][1])
    print "PAIRINGS" 
    pairs.append(pair)
    pairs.append(pair_2)
    print pairs
    return pairs
    
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


