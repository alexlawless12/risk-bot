import os
import json
import subprocess
import time

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


def run_match(heuristic_script, random_script, log_dir):
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Construct the command to run the game
    command = [
        "python", "play_risk_ai.py",
        "-w", heuristic_script, "Heuristic",
        random_script, "Random", "-v"
    ]

    # Run the game and store logs
    result = subprocess.run(command, capture_output=True, text=True)
    log_filename = os.path.join(log_dir, f"log_{int(time.time())}.txt")
    with open(log_filename, 'w') as log_file:
        log_file.write(result.stdout)

    return log_filename


def load_q_table(q_table_file):
    if os.path.exists(q_table_file):
        with open(q_table_file, 'r') as f:
            q_table = json.load(f)
    else:
        q_table = {}
    return q_table


def save_q_table(q_table, q_table_file):
    with open(q_table_file, 'w') as f:
        json.dump(q_table, f, indent=4)


def load_weights(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config.get('weights', {})


def update_weights(q_table, config_file):
    # Load the current weights
    weights = load_weights(config_file)

    for filename, data in q_table.items():
        q_values = data["q_values"]
        avg_q_value = sum(q_values) / len(q_values) if q_values else 0

        # Update weights based on avg_q_value
        for key in weights:
            weights[key] += 0.01 * avg_q_value
            # Ensure no weight goes above 1
            weights[key] = min(weights[key], 1.0)

    # Save the updated weights back to the config file
    with open(config_file, 'w') as f:
        json.dump({"weights": weights}, f, indent=4)


def main():
    heuristic_script = "./ai/heuristic_ai.py"
    random_script = "./ai/random_ai.py"
    config_file = "./ai/config.json"
    q_table_file = "q_table.json"
    log_dir = "./logs"

    # Load the initial Q-table
    q_table = load_q_table(q_table_file)

    # Training loop
    num_games = 1  # Number of games to run for training
    for _ in range(num_games):
        log_filename = run_match(heuristic_script, random_script, log_dir)

        # Parse the log file and update the Q-table
        with open(log_filename, 'r') as file:
            log_content = file.read()
        n_players = 2  # Example, adjust based on actual number of players
        q_values = parse_log_file(log_content, n_players)

        q_table[log_filename] = {
            "q_values": q_values,
            "weights": load_weights(config_file)
        }

        # Save the updated Q-table
        save_q_table(q_table, q_table_file)

        # Update the weights based on Q-table
        update_weights(q_table, config_file)


if __name__ == "__main__":
    main()
