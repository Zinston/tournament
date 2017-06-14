#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
        """Connect to the PostgreSQL database.
           Returns a database connection."""
        try:
            return psycopg2.connect("dbname=tournament")
        except psycopg2.Error, e:
            print e


def execute_query(query, values=None):
    """Executes a query in the database.
       Returns fetched results (None if no results)

    Args:
            query: the sql query string.
            values: a tuple containing values to insert into the database."""
    db = connect()
    c = db.cursor()
    if values is not None:
        c.execute(query, values)
    else:
        c.execute(query)
    try:
        results = c.fetchall()
    except:
        results = None
        db.commit()
    db.close()
    return results


def deleteMatches():
        """Remove all the match records from the database."""
        execute_query("delete from match;")


def deletePlayers():
        """Remove all the player records from the database."""
        execute_query("delete from players;")


def countPlayers():
        """Returns the number of players currently registered."""
        players = execute_query("select count(id) as num from players;")
        return int(players[0][0])


def registerPlayer(name):
        """Adds a player to the tournament database.

        The database assigns a unique serial id number for the player.
        (This should be handled by your SQL database schema,
        not in your Python code.)

        Args:
            name: the player's full name (need not be unique).
        """

        execute_query("insert into players (name) values (%s);", (name,))


def playerStandings():
        """Returns a list of the players and their win records, sorted by wins.

        The first entry in the list should be the player in first place,
        or a player tied for first place if there is currently a tie.

        Returns:
            A list of tuples, each of which contains (id, name, wins, matches):
                id: the player's unique id (assigned by the database)
                name: the player's full name (as registered)
                wins: the number of matches the player has won
                matches: the number of matches the player has played
        """

        return execute_query("""
            select players.id, players.name,
                (select count(match.id) from match
                    where match.winner=players.id) as wins,
                (select count(match.id) from match
                    where match.winner = players.id
                    or match.loser = players.id) as match
            from players
            order by wins desc;""")


def reportMatch(winner, loser):
        """Records the outcome of a single match between two players.

        Args:
            winner:  the id number of the player who won
            loser:  the id number of the player who lost
        """

        execute_query("""insert into match (winner, loser)
                     values (%s, %s);""", (winner, loser))


def swissPairings():
        """Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered,
        each player appears exactly once in the pairings.
        Each player is paired with another player with an equal
        or nearly-equal win record, that is, a player adjacent
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
        for i in range(0, len(standings), 2):
            pairings.append((standings[i][0],
                             standings[i][1],
                             standings[i+1][0],
                             standings[i+1][1]))
        return pairings
