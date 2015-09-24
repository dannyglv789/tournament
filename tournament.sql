-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- CREATE TABLE 

/* creating DATABASE and establishing connection */
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

/* Table Schema */
CREATE TABLE players (
	player_id serial PRIMARY KEY,
	player_name text
);

CREATE TABLE matches (
	match_id serial PRIMARY KEY,
	winner serial references players(player_id),
	loser serial references players(player_id)
);

/* Create Views for standings*/
CREATE VIEW player_wins AS SELECT players.player_id, players.player_name, COUNT(matches.winner) as num_wins from
               players left join matches on players.player_id = matches.winner 
               GROUP BY player_id ORDER BY num_wins desc;

CREATE VIEW total_matches AS SELECT players.player_id, COUNT(matches.match_id) AS matches_played
               FROM players join matches on players.player_id = matches.winner or players.player_id = matches.loser GROUP BY player_id;
			   
CREATE VIEW our_standings AS SELECT player_wins.player_id, player_name, num_wins, coalesce(total_matches.matches_played,0) AS matches
               FROM player_wins left join total_matches on player_wins.player_id = total_matches.player_id ORDER BY num_wins desc;
