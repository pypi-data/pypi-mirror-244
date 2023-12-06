# F1DataScraper #

## What is this? ##
This module extract Formula 1 data, encompassing drivers, races, teams, and fastest laps, through a parser.

Categories from which you can pull data:

- Drivers Standings (`drivers`)
- Race Results (`races`)
- Teams Standing (`teams`)
- Fastest Laps Results (`fastest_laps`)


## Quick Guide ##
The module is based on the following structure:

    
    from f1datascraper import FormulaOneParser, parse_drivers_data

	parser = FormulaOneParser()
	drivers_data = parser.parse_drivers_data({YEAR})
    
Which Python provides by standard.


----------


### Using ###

**Installation**

Using the library is as simple and convenient as possible:
Installing the package with `pip`:

	pip install f1datascraper

**Getting Started**

Examples of all operations:

Import the `FormulaOneParser` class:

	from f1datascraper import FormulaOneParser

Initialize a `parser` object:

	parser = FormulaOneParser()

Parsing Data
Call the parsing methods on the parser object, passing in the year:

**`parse_{category}_data` takes as an argument only one argument which is `{YEAR}`**

	drivers_data = parser.parse_drivers_data(2021)
	races_data = parser.parse_races_data(2023)
	teams_data = parser.parse_teams_data(2018) 
	fastest_laps = parser.parse_fastest_laps_data(1999)


----------

## Developer ##
My profile: [ryazhenkofc](https://github.com/ryazhenkofc) 
