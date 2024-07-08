import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from dateutil.parser import parse as date_parse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from prettytable import PrettyTable, ALL


driver = webdriver.Chrome()
driver.get("https://www.livesportsontv.com")

# Get the HTML after the page is fully loaded
html2 = driver.execute_script("return document.documentElement.innerHTML;")
driver.quit()


now = datetime.now()
formatted_date = now.strftime("%m/%d/%y")

soup = BeautifulSoup(html2, 'html.parser')

pretty = soup.prettify()

today = datetime.now()

formatted_date = today.strftime("%a, %b ") + str(today.day)
htmltxt = pretty.splitlines()
flag = False
sports_info_raw = []
for line in htmltxt:
    line = line.strip()
    if line == f'GAMES TODAY, {formatted_date}':
        flag = True
    if flag:
        sports_info_raw.append(line)
    if line == 'News':
        flag = False

time = []
league = []
teams = []
date = []
sport = []
rows = []

for i in range(len(sports_info_raw)):
    if sports_info_raw[i] == '<h3>':
        i += 1
        sport = sports_info_raw[i]
        for j in range(i, len(sports_info_raw)):
            if sports_info_raw[j] == '<h3>':
                i = j - 1
                break
            if sports_info_raw[j] == '<h4 class="date-events__league-header-title">':
                league = sports_info_raw[j+1]
            elif sports_info_raw[j] == '<time>':
                time = sports_info_raw[j+1]
            elif sports_info_raw[j] == '<div class="event__participant event__participant--home">':
                if sports_info_raw[j+5] == '<div class="event__participant event__participant--away">':
                    teams = sports_info_raw[j+1] + " vs " + sports_info_raw[j+6]
                else:
                    teams = sports_info_raw[j+1]
            elif sports_info_raw[j] == '<div class="date-events__sport-header-date">':
                date = sports_info_raw[j+1]
            elif sports_info_raw[j] == '<div class="event__odds_wrapper">':
                rows.append({'Time': time,'Sport': sport, 'League': league, 'Teams': teams, 'Date': date})



sports_df = pd.DataFrame(rows)
sports_df.to_csv('livesportstoday.csv', index=False)



prettytable = PrettyTable()
prettytable.field_names = ['Time', 'Sport', 'League', 'Teams', 'Date']
for row in rows:
    prettytable.add_row([row['Time'], row['Sport'], row['League'], row['Teams'], row['Date']])
prettytable.hrules = ALL
prettytable.vrules = ALL
printer = prettytable.get_string()
with open('sports_table.txt', 'w') as f:
    f.write(printer)

print(prettytable)

