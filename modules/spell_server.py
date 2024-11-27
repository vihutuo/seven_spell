import requests
import time
from datetime import datetime
import math

class GameClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_game_state(self):
        """Fetches the current game state (active or inactive round)."""
        response = requests.get(f"{self.base_url}/game-state")

        if response.status_code == 200:
            gs =  response.json()
            time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            gs["time_remaining"]= datetime.strptime(gs["score_submission_deadline_utc"], time_format) -  datetime.strptime(gs["current_time_utc"],time_format)
            gs["time_remaining"] = int(gs["time_remaining"].total_seconds()) - 3 # 3 seconds buffer
            gs["next_round_starts_in"] = datetime.strptime(gs["game_end_time_utc"],
                                                     time_format) - datetime.strptime(gs["current_time_utc"],
                                                                                      time_format)
            gs["next_round_starts_in"] = math.ceil((gs["next_round_starts_in"].total_seconds()))
            return gs
        else:
            raise Exception(f"Failed to fetch game state: {response.text}")

    def fetch_word(self):
        """Fetches the word for the current round."""
        response = requests.get(f"{self.base_url}/fetch-word")

        if response.status_code == 200:
            return response.json()["word"]
        else:
            raise Exception(f"Failed to fetch word: {response.text}")

    def submit_score(self, player_name, score, word):
        """Submits the player's score for the round."""
        data = {
            "player_name": player_name,
            "score": score,
            "word": word
        }
        response = requests.post(f"{self.base_url}/submit-score", json=data)

        if response.status_code == 200:
            print("Score submitted successfully!")
        else:
            raise Exception(f"Failed to submit score: {response.text}")

    def fetch_scores(self):
        """Fetches the scores for the current round."""
        response = requests.get(f"{self.base_url}/get_scores")

        if response.status_code == 200:
            return response.json()["scores"]
        else:
            raise Exception(f"Failed to fetch scores: {response.text}")


# Example usage
if __name__ == "__main__":
    client = GameClient(base_url="http://localhost:8000")  # Replace with the actual server URL

    try:
        # Step 1: Get game state
        game_state = client.get_game_state()
        print(f"Game state: {game_state}")

        if game_state["round_status"] == "active":
            # Step 2: Fetch word for the round
            word = client.fetch_word()
            print(f"Current word for the round: {word}")

            # Step 3: Simulate gameplay and score submission
            player_name = "Player 1"
            score = 10  # Replace with the actual score calculation
            time.sleep(2)  # Simulate some gameplay time

            # Submit score
            client.submit_score(player_name, score, word)

            # Step 4: Fetch scores after the round ends
            scores = client.fetch_scores()
            print(f"Scores: {scores}")
        else:
            print("Round has not started yet, try again later.")
    except Exception as e:
        print(f"Error: {e}")