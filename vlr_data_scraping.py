#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def create_player_df(urls):
    final_df = pd.DataFrame()  

    for url in urls:
        try:

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)
            driver.implicitly_wait(10)  


            all_matches_data = driver.find_elements(By.CSS_SELECTOR, 'div.stat')  
            playtime = driver.find_elements(By.CSS_SELECTOR, 'span.playtime')  
            matches = driver.find_elements(By.CSS_SELECTOR, 'span.matches')
            player_name = driver.find_elements(By.CSS_SELECTOR, 'span.fit-text-parent')

            all_matches_data = [match.text for match in all_matches_data]
            playtime_data = [match.text for match in playtime]
            match_data = [match.text for match in matches]
            player_name_data = [match.text for match in player_name]

            driver.quit()

            df_player_name = pd.DataFrame(player_name_data, columns=['Player Name'])
            df_all_matches = pd.DataFrame(all_matches_data, columns=['Overview'])
            df_playtime = pd.DataFrame(playtime_data, columns=['Total Playtime'])
            df_matches = pd.DataFrame(match_data, columns=['Total Matches'])

            ## Data Cleaning Overview Data

            df_split = df_all_matches['Overview'].str.split('\n', expand=True)


            df = df_split[[0,1]]

            colum_names = df[0]

            overview_df = df[1]

            data_dict = {}

            for i, value in enumerate(overview_df):
                data_dict[colum_names[i]] = value

            index = range(len(colum_names))

            df_all_matches = pd.DataFrame(data_dict, index=index )

            df_all_matches.drop_duplicates(inplace=True)

            # Final DF

            df_final = pd.concat([df_player_name, df_all_matches, df_playtime, df_matches], axis=1)

            final_df = pd.concat([final_df, df_final], ignore_index=True)



        except Exception as e:
            print(f"Error processing URL '{url}': {e}")

    final_df.to_csv('players_data.csv', index=False)

    return final_df


players_urls = [
  'https://tracker.gg/valorant/profile/riot/Menó%23br10/overview?season=all'
  ,'https://tracker.gg/valorant/profile/riot/sn0w%230777/overview?season=all'
  ,'https://tracker.gg/valorant/profile/riot/VigilanteSht%23GABSS/overview?season=all'
  ,'https://tracker.gg/valorant/profile/riot/LUKAO%23DAVI/overview?season=all'
  ,'https://tracker.gg/valorant/profile/riot/JOOOOOBS%23JOJO/overview?season=all'
  ,'https://tracker.gg/valorant/profile/riot/seal%231p2c/overview?playlist=competitive&season=all'
  ,'https://tracker.gg/valorant/profile/riot/JeffreyDahmerSKL%23LOVE/overview?season=all'
]


create_player_df(players_urls)

