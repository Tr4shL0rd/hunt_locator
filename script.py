from bs4 import BeautifulSoup 
import requests
import sys
from pyperclip import copy

BASE_URL = "https://ffxiv.consolegameswiki.com/wiki/"
TARGET = "_".join(sys.argv[1:]).title()
URL = f"{BASE_URL}{TARGET}"
page = requests.get(URL)
#print("DEBUG:", URL)
soup = BeautifulSoup(page.content, "html.parser")
location_tables = soup.find(class_="location table")
trs = location_tables.find_all("tr")[1:]
#print(trs)
for tr in trs:
    tr_text = tr.text.strip().replace("\n", " ").replace("(", " ").replace(")", " ")
    tr_data = tr_text.split()
    zone_name = ' '.join(tr_data[:-3])
    coordinates = tr_data[-3:-1]
    #½print(coordinates)
    if "Unknown" in coordinates:
        zone_name = f"{zone_name} {coordinates[0]}"
        coordinates.pop(0)
    if "Unknown" not in coordinates:
        copy(f"{''.join(coordinates)} : {zone_name}")
    #print(zone_name)
    level = tr_data[-1]
    print("Zone Name:", zone_name)
    print("Coordinates:", "".join(coordinates))
    print("Level:", level)
    print()
