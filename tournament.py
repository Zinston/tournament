#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
      return psycopg2.connect("dbname=tournament")
    except psycopg2.Error, e:
      print e

def execute_query(query):
  """Executes a query in the database.

  Args:
      query: the sql query string."""
  db = connect()
  c = db.cursor()
  c.execute(query)
  db.commit()
  db.close()

def deleteMatches():
    """Remove all the match records from the database."""
    execute_query("delete from match;")


def deletePlayers():
    """Remove all the player records from the database."""
    execute_query("delete from players;")


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(id) as num from players;")
    players = c.fetchall()
    db.close()
    return int(players[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values (%s);", (name,))
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
    c.execute("""select players.id as id, players.name as name, coalesce(playing_players_standings.wins, 0) as wins, coalesce(playing_players_standings.matches, 0) as matches
                 from players left join
                    (select matches_played.id as id, name, wins, matches
                    from
                      (select players.id as id, players.name as name, coalesce(count(match.id), 0) as matches
                      from players, match
                      where players.id = match.winner or players.id = match.loser
                      group by players.id)
                      as matches_played
                    left join
                      (select players.id as id, coalesce(count(match.id), 0) as wins
                      from players, match
                      where match.winner = players.id
                      group by players.id)
                      as matches_won
                    on matches_played.id = matches_won.id
                    group by matches_played.id, matches_played.name, matches_won.wins, matches_played.matches)
                    as playing_players_standings
                 on players.id = playing_players_standings.id
                 group by players.id, playing_players_standings.name, playing_players_standings.wins, playing_players_standings.matches
                 order by wins desc;""")
    player_standings = c.fetchall()
    db.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db = connect()
    c = db.cursor()
    c.execute("insert into match (winner, loser) values (%s, %s);", (winner, loser))
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

    standings = playerStandings()
    pairings = []
    i = 0
    for i in range(0,len(standings)):
        if i%2 == 0:
            pairings.append((standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]))
    return pairings


