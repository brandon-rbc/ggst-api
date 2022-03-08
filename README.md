# ggst-api-py

A barebones wrapper for Guilty Gear Strive's REST API  
  
https://github.com/halvnykterist/ggst-api-rs was used to deconstruct the api and inspired the formation of the rest of my code.
More information on how the code works can also be found at that link above.


Calling the below method will allow the user to obtain at max 100 pages of 127 replays:
```python3
def get_match_data(min_floor,
                   max_floor,
                   char1_num,
                   char2_num,
                   pages
                   replays_per_page)
```

## Example
The below code returns and prints data from 5 pages of 100 replays, those of which
have Millia and Potemkin throughout floors 6 and 8

```python3
char1 = char_dict['Millia']
char2 = char_dict['Potemkin']
game_data = get_match_data(min_floor=6,
                           max_floor=8,
                           char1_num=char1,
                           char2_num=char2,
                           pages=1,
                           replays_per_page=10)
for game in game_data:
    nameWinner = [char for char, charNum in char_dict.items() if charNum == game.winner][0]
    nameLoser = [char for char, charNum in char_dict.items() if charNum == game.loser][0]
    print(game.winner, game.loser, game.floor, game.date_time, nameWinner, nameLoser, game.winner_side)
```
Please note that load times may be long for the api due to the data having to be obtained from Japan
