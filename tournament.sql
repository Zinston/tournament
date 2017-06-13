-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
	id		serial	PRIMARY KEY,
	name	text
);

-- create table tournaments (
--	id		serial	PRIMARY KEY,
--	player 	integer	REFERENCES players (id),
--	winner	integer
--);

create table match (
	id		serial	PRIMARY KEY,
--	tnmt	integer	REFERENCES tournaments (id),
	winner	integer	REFERENCES players (id),
	loser	integer	REFERENCES players (id)
);

-- create table round (
--	id		serial	PRIMARY KEY,
--	tnmt 	integer	REFERENCES tournaments (id),
--	match	integer	REFERENCES match (id)
--);

create or replace view matches_played as
    select players.id as id, players.name as name, coalesce(count(match.id), 0) as matches
    from players, match
    where players.id = match.winner or players.id = match.loser
    group by players.id;

create or replace view matches_won as
    select players.id as id, coalesce(count(match.id), 0) as wins
    from players, match
    where match.winner = players.id
    group by players.id;

create or replace view playing_players_standings as
    select matches_played.id as id, name, wins, matches
    from matches_played left join matches_won
    on matches_played.id = matches_won.id
    group by matches_played.id, matches_played.name, matches_won.wins, matches_played.matches;