import streamlit as st
import requests
from bs4 import BeautifulSoup
import random


# title
st.title("Robot Parlay 📈")

# --- User Input ---
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