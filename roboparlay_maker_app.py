import streamlit as st
import requests
from bs4 import BeautifulSoup
import random


# title
st.title("Robot Parlay 📈")

# --- User Input ---
# Step 1: Ask the user to select the sport
league = st.selectbox("Which league is your parlay for?", ["MLB", "NHL"])

# Step 2: Show different inputs depending on the sport
if league == "MLB":
    teamname = st.text_input("Enter the team you want to bet on: Only enter the team name and not the city/state (e.g. bluejays)").lower()
    number_legs = st.number_input("How many legs do you want your parlay to be?", min_value=3, max_value=5, step=1)

    start = st.button("Generate Parlay")
    placeholder1 = st.empty()
    placeholder2 = st.empty()
    placeholder3 = st.empty()
    placeholder4 = st.empty()
    placeholder5 = st.empty()

    lineup_url = "https://www.mlb.com/" + teamname +"/roster/starting-lineups"

    if start:
        try:
            response = requests.get(lineup_url)
            soup = BeautifulSoup(response.content, 'lxml')

            # get lineups for the away and home teams
            away_team = soup.find('ol', class_='starting-lineups__team starting-lineups__team--away').text.splitlines()
            home_team = soup.find('ol', class_='starting-lineups__team starting-lineups__team--home').text.splitlines()[1:]
            full_lineup = away_team + home_team

            players = random.sample(range(1, 19), number_legs)

            counter = 1
            for player in players:
                flip = random.choice(["Heads", "Tails"])
                if flip == "Heads":
                    globals()[f'placeholder{counter}'].markdown(full_lineup[player] + " for 2 Hits/Runs/RBIs")
                else:
                    globals()[f'placeholder{counter}'].markdown(full_lineup[player] + " for 1 Hit")
                counter += 1


        except Exception as e:
            st.error(f"An error occurred: {e}")
    
elif league == "NHL":
    teamname1 = st.text_input("Enter the first team you want to bet on (format: vegas-golden-knights)").lower()
    teamname2 = st.text_input("Enter the second team you want to bet on (format: winnipeg-jets)").lower()
    number_legs = st.number_input("How many legs do you want your parlay to be?", min_value=3, max_value=5, step=1)


    start = st.button("Generate Parlay")
    placeholder1 = st.empty()
    placeholder2 = st.empty()
    placeholder3 = st.empty()
    placeholder4 = st.empty()
    placeholder5 = st.empty()

    lineup_url1 = "https://www.dailyfaceoff.com/teams/" + teamname1 +"/line-combinations"
    lineup_url2 = "https://www.dailyfaceoff.com/teams/" + teamname2 +"/line-combinations"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    players = []

    if start:
        try:
            response1 = requests.get(lineup_url1, headers = headers)
            soup1 = BeautifulSoup(response1.content, 'lxml')

            top6_1 = soup1.find_all('div', class_='flex flex-row justify-center')
            for player in (top6_1[:6]):
                players.append(player.text.strip())

            response2 = requests.get(lineup_url2, headers = headers)
            soup2 = BeautifulSoup(response1.content, 'lxml')

            top6_2 = soup2.find_all('div', class_='flex flex-row justify-center')
            for player in (top6_2[:6]):
                players.append(player.text.strip())

            chosen = random.sample(range(0, 12), number_legs)

            counter = 1
            for choice in chosen:
                globals()[f'placeholder{counter}'].markdown(players[choice] + " for a Point")
                counter += 1

            placeholder5 = str(players)

        except Exception as e:
            st.error(f"An error occurred: {e}")