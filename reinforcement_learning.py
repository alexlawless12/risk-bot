import os
import sys
import json
import argparse
from datetime import datetime

# Function to parse the RISKBOARD section


def parse_riskresult(section, n_players):
    result_sections = section.split('|')
    player_info = result_sections[1:n_players+1]
    additional_info = result_sections[n_players+1:]
    return player_info, additional_info

# Main function to parse the log file


def parse_log_file(log_content, n_players):
    q_values = []
    for line in log_content.split('\n'):
        if line.startswith("RISKRESULT"):
            risk_result, additional_info = parse_riskresult(line, n_players)
            heuristic_win = float(risk_result[0].split(',')[1])
            q_values.append(heuristic_win)
    return q_values


def find_newest_folder(logs_dir):
    # Get all directories in logs_dir
    directories = [d for d in os.listdir(
        logs_dir) if os.path.isdir(os.path.join(logs_dir, d))]
    # Sort directories based on creation time
    sorted_dirs = sorted(directories, key=lambda d: os.path.getctime(
        os.path.join(logs_dir, d)), reverse=True)
    # Return the newest directory
    return sorted_dirs[0] if sorted_dirs else None


def load_weights(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config.get('weights', {})


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Process log files and build Q-table.")
    parser.add_argument("-w", "--ai-scripts", nargs='+',
                        help="Paths to AI scripts")
    parser.add_argument("-c", "--config-file",
                        help="Path to config file", default="./ai/config.json")
    args = parser.parse_args()

    # Load weights from config file
    weights = load_weights(args.config_file)

    # Find newest folder in ./logs directory
    logs_dir = "./logs"
    newest_folder = find_newest_folder(logs_dir)
    if not newest_folder:
        print("No folders found in ./logs directory.")
        return

    # Loop through all files in the newest folder
    folder_path = os.path.join(logs_dir, newest_folder)
    q_table = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # Get number of players from end of filename
            n_players = int(filename.split('_')[-1].split('.')[0])
            with open(file_path, 'r') as file:
                log_content = file.read()

            # Execute parse_log_file on each file
            q_values = parse_log_file(log_content, n_players)
            q_table[filename] = {
                "q_values": q_values,
                "weights": weights
            }

    # Write Q-table to a JSON file
    q_table_file = "q_table.json"
    with open(q_table_file, 'w') as f:
        json.dump(q_table, f, indent=4)

    print("Q-table generated and saved as", q_table_file)


if __name__ == "__main__":
    main()
