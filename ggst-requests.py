import requests
import time

ggst_api_url = "https://ggst-game.guiltygear.com"


class match_result():
    def __init__(self):
        self.winner = -1
        self.loser = -1
        self.floor = ''
        self.date_time = ''


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


def get_match_data(min_floor=1, max_floor=11, char1_num=0, char2_num=0, replays_per_page=100, pages=100):
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

        request_string = "9295B2323131303237313133313233303038333834AD36316135656434663436" \
                         f"31633202A5302E302E38039401CC{page_num:02x}{replays_per_page:02x}9AFF00{game_data_string}"

        data = {"data": f"{request_string}"}
        headers = {"USER_AGENT": "Steam", "CACHE_CONTROL": "no-cache"}
        res = requests.post(request_url, data=data, headers=headers)

        if len(res.content) < 63:
            print('No Matches Found')
            return []
        all_matches = res.content.split(b'\x01\x00\x00\x00')
        all_matches.pop()  # delete empty index at end
        for match in all_matches:
            match_data = match.split(b'\x95\xb2')
            # res_data[0]: {floor}{p1_char}{p2_char}
            # res_data[1]: \x95\xb2{p1_id [18 chars]}\xa_{p1_name}\xb1{p1_some_number}\xaf{p1_online_id}\x07
            # res_data[2]: \x95\xb2{p2_id}\xa_{p2_name}\xb1{p2_some_number}\xaf{p2_online_id}\t{winner}\xb3{timestamp}

            winner = match_data[2].split(b'\xb3')[0][-1]
            date_time = match_data[2].split(b'\xb3')[1][0:19]

            tmp_res = match_result()
            if winner == 1:
                tmp_res.winner = char1_num
                tmp_res.loser = char2_num
            else:
                tmp_res.winner = char2_num
                tmp_res.loser = char1_num
            tmp_res.floor = f'{match_data[0][-3]}'
            # if 99 -> celestial(floor 11)
            tmp_res.date_time = f'{date_time}'  # Datetime sometimes not accessible, will have to check for proper
                                                # formatting later on

            game_results.append(tmp_res)

    return game_results


# start = time.time()
def example():
    char1 = char_dict['Millia']
    char2 = char_dict['Potemkin']
    game_data = get_match_data(min_floor=10,
                               max_floor=10,
                               char1_num=char1,
                               char2_num=char2,
                               pages=1,
                               replays_per_page=100)
    # end = time.time()

    for game in game_data:
        print(game.winner, game.loser, game.floor, game.date_time)


example()
