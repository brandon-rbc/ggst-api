import requests
import time

ggst_api_url = "https://ggst-game.guiltygear.com"


class match_result():
    def __init__(self):
        self.p1 = -1
        self.p2 = -1
        self.winner = -1
        self.loser = -1
        self.floor = ''
        self.date_time = ''
        self.winner_side = -1


char_dict = {
    "Sol": 1,
    "Ky": 2,
    "May": 3,
    "Axl": 4,
    "Chipp": 5,
    "Potemkin": 6,
    "Faust": 7,
    "Millia": 8,
    "Zato": 9,
    "Ramlethal": 10,
    "Leo": 11,
    "Nagoriyuki": 12,
    "Giovanna": 13,
    "Anji": 14,
    "Ino": 15,
    "Goldlewis": 16,
    "Jacko": 17,
    "HappyChaos": 18,
    "Baiken": 19,
}


def format_game_info(min_floor, max_floor, char1_num, char2_num):
    return f"{min_floor:02x}{max_floor:02x}90{char1_num:02x}{char2_num:02x}{0x00:02x}0001"


def get_match_data(min_floor=1, max_floor=11, char1_num=255, char2_num=255, replays_per_page=100, pages=100):
    # Parameter Checking
    if pages > 100:
        raise ValueError(f"cannot query over 100 pages, 'f{pages}' requested")
    if replays_per_page > 127:
        raise ValueError(f"cannot query over 127 replays per page, 'f{replays_per_page}' requested")
    if 0 > min_floor or min_floor > 12:
        raise ValueError(f"Please choose a bottom floor between 1 and 11, f{min_floor} requested")
    if 0 > max_floor or max_floor > 12:
        raise ValueError(f"Please choose a bottom floor between 1 and 11, f{min_floor} requested")
    if min_floor > max_floor:
        raise ValueError(f"min_floor {min_floor} is greated than max_floor {max_floor}")

    request_url = f"{ggst_api_url}/api/catalog/get_replay"

    game_results = []
    for page_num in range(pages):
        game_data_string = format_game_info(min_floor=min_floor,
                                            max_floor=max_floor,
                                            char1_num=char1_num,
                                            char2_num=char2_num)

        # https://github.com/halvnykterist/ggst-api-rs/blob/7087563272b9c829db8860a4b3952b1a65ea855c/src/requests.rs#L88-L92
        request_string = f"9295B2323131303237313133313233303038333834AD3631613565643466343631633202A5302E3" \
                         f"12E30039401CC{page_num:02x}{replays_per_page:02x}9AFF00{game_data_string}"

        data = {"data": f"{request_string}"}
        headers = {"USER_AGENT": "Steam", "CACHE_CONTROL": "no-cache"}
        res = requests.post(request_url, data=data, headers=headers)

        if len(res.content) < 71:
            print('No Matches Found')
            return []
        all_matches = res.content.split(b'\x01\x00\x00\x00')
        all_matches.pop()  # delete empty index at end
        for match in all_matches:
            match_data = match.split(b'\x95\xb2')
            # res_data[0]: {floor}{p1_char}{p2_char}
            # res_data[1]: \x95\xb2{p1_id [18 chars]}\xa_{p1_name}\xb1{p1_some_number}\xaf{p1_online_id}\x07
            # res_data[2]: \x95\xb2{p2_id}\xa_{p2_name}\xb1{p2_some_number}\xaf{p2_online_id}\t{winner}\xb3{timestamp}

            p1 = match_data[0][-2]
            p2 = match_data[0][-1]
            if p1 == 0 or p2 == 0: # sometimes returns character values of zero, not sure what it means yet
                continue

            winner = match_data[2].split(b'\xb3')[0][-1]
            if not winner == 1 or not winner == 2: # if winner not found, just skip that match
                continue
            date_time = match_data[2].split(b'\xb3')[-1][0:19]

            tmp_res = match_result()
            tmp_res.p1 = p1
            tmp_res.p2 = p2
            if winner == 1:
                tmp_res.winner = p1
                tmp_res.loser = p2
                tmp_res.winner_side = 1
            else:
                tmp_res.winner = p2
                tmp_res.loser = p1
                tmp_res.winner_side = 2
            tmp_res.floor = f'{match_data[0][-3]}'
            # if 99 -> celestial(floor 11)
            tmp_res.date_time = f'{date_time}'  # Datetime sometimes not accessible, will have to check for proper
                                                # formatting later on

            game_results.append(tmp_res)

    return game_results


# start = time.time()
def example():
    char1 = char_dict['Axl']
    char2 = char_dict['Chipp']
    game_data = get_match_data(min_floor=9,
                               max_floor=11,
                               char1_num=char1,
                               char2_num=char2,
                               pages=5,
                               replays_per_page=100)
    # end = time.time()

    for game in game_data:
        nameWinner = [char for char, charNum in char_dict.items() if charNum == game.winner][0]
        nameLoser = [char for char, charNum in char_dict.items() if charNum == game.loser][0]
        print(game.winner, game.loser, game.floor, game.date_time, nameWinner, nameLoser, game.winner_side)


# example()
