from ggst_requests import get_match_data, char_dict
import csv
import time

data_cols = ['P1Char', 'P2Char', 'Floor', 'WinnerSide', 'Winner', 'Loser', 'TimeStamp']

before = time.time()
with open('test.csv', 'w', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(data_cols)
    for char1, char1Num in char_dict.items():
        for char2, char2Num in char_dict.items():
            # if char1 == char2: # skip dittos
            #     continue
            # print(f"getting data for {char1} vs {char2}")
            game_data = get_match_data(min_floor=8,
                                       max_floor=11,
                                       char1_num=char1Num,
                                       char2_num=char2Num,
                                       pages=30,
                                       replays_per_page=100)

            for game in game_data:
                writer.writerow([game.p1,
                                 game.p2,
                                 game.floor,
                                 game.winner_side,
                                 [char for char, charNum in char_dict.items() if charNum == game.winner][0],
                                 [char for char, charNum in char_dict.items() if charNum == game.loser][0]])

after = time.time()

print(f"{after - before}")
