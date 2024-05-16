import json

# Function to parse the RISKBOARD section


def parse_riskresult(section, n_players):
    result_sections = section.split('|')
    player_info = result_sections[1:n_players+1]
    additional_info = result_sections[n_players+1:]
    return player_info, additional_info


# Main function to parse the log file
def parse_log_file(log_file, n_players):
    for line in log_file.split('\n'):
        if line.startswith("RISKRESULT"):
            risk_result, additional_info = parse_riskresult(line, n_players)
            heuristic_win = float(risk_result[0].split(',')[1])
    print(heuristic_win)


def main():
    file_path = './logs/20240514-2310_“Attacker”_“Random1”_“Random2”/_“Random2”_“Random1”_“Attacker”_11_20240514-2310_players_3.log'
    # Get number of players from end of filename
    n_players = int(file_path.split('_')[-1].split('.')[0])

    with open(file_path, 'r') as file:
        log_content = file.read()

    parse_log_file(log_content, n_players)


if __name__ == "__main__":
    main()
