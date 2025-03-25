import requests
from bs4 import BeautifulSoup
import random

# # Step 1: Send a request to the webpage
# url = "https://www.mlb.com/dodgers/roster/starting-lineups"
# response = requests.get(url)

def generate_leg(url: str, position: int, obverse: str) -> str:

    # Step 2: Check if the request was successful
    response = requests.get(url)
    if response.status_code == 200:
        
        # Step 3: Parse the webpage content with BeautifulSoup and the lxml parser
        soup = BeautifulSoup(response.content, 'lxml')
        # print(soup.prettify())

        # get lineups for the away and home teams
        away_team = soup.find('ol', class_='starting-lineups__team starting-lineups__team--away').text.splitlines()
        home_team = soup.find('ol', class_='starting-lineups__team starting-lineups__team--home').text.splitlines()[1:]
        full_lineup = away_team + home_team

        if obverse == "Heads":
            return(full_lineup[position] + " for 2 Hits/Runs/RBIs")
        else:
            return(full_lineup[position] + " for 1 Hit")

        # # randomize the parlay
        # players = []
        # player = random.randint(1, 18)
        # for leg in ["first", "second", "third"]:
        #     while player in players:
        #         player = random.randint(1, 18)
        #     players.append(player)

        #     coin_flip = random.choice(["Heads", "Tails"])
        #     if coin_flip == "Heads":
        #         prop = "2 Hits/Runs/RBIs"
        #     else:
        #         prop = " 1 Hit"

        #     print("The " + leg + " leg is " + full_lineup[player] + " for " + prop)

        # print("Good luck!")

    else:
        return(f"Failed to retrieve data. Status code: {response.status_code}")