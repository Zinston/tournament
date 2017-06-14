# Tournament
_Tournament_ manages a Swiss-system tournament with a pair number of players.

## Installation
* Clone the GitHub repository : `git clone https://github.com/Zinston/tournament.git`
* [Install](https://wiki.postgresql.org/wiki/Detailed_installation_guides) PostgreSQL
* Initialize the database in PostgreSQL : `\i tournament.sql` (within the tournament root folder)

## Usage
* While _Tournament_ contains a few handy functions for managing a Swiss-system tournament, it doesn't actually do anything on its own.
* Simply put, the code in this repository can be used to build any application requiring the ability to pair players in a Swiss-system tournament.
* Using `python tournament_test.py` allows you to **test** that all functions in `tournament.py` work.
* Functions in `tournament.py` allow you to :
  * add, delete and count players
  * fetch the players' win records as well as how many matches they played
  * pair the players for new matches according to the Swiss style
  * and and delete matches

### What's a Swiss-system tournament anyway ?
A [Swiss-system tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament) is a non-eliminating tournament format. All competitors play in each round unless there is an odd number of them. Competitors meet one-to-one in each round and are paired using a set of rules designed to ensure that each competitor plays opponents with a similar running score. The winner is the competitor with the highest aggregate points earned in all rounds.

## Limitations
* _Tournament_ only works with **pair** numbers of players.

## Contributing
Ideas, contributions and improvements are more than welcome. When adding a feature, please write a test function for it in `tournament_test.py`.

## License
_Tournament_ is released under the [MIT License](tournament/LICENSE.txt).
