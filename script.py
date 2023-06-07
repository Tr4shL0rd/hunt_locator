from bs4 import BeautifulSoup 
import requests
import sys
import webbrowser
from pyperclip import copy
TARGET = None
if len(sys.argv) == 1:
    TARGET = "_".join(input("Target: ")).title()
BASE_URL = "https://ffxiv.consolegameswiki.com/wiki/"
TARGET = "_".join(sys.argv[1:]).title()
URL = f"{BASE_URL}{TARGET}"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
location_tables = soup.find(class_="location table")
fates = soup.find(id="FATEs")
trs = location_tables.find_all("tr")[1:]

locations = []
for location_id,tr in enumerate(trs,start=1):
    tr_text = tr.text.strip().replace("\n", " ").replace("(", " ").replace(")", " ")
    tr_data = tr_text.split()
    zone_name = " ".join(tr_data[:-3])
    coordinates = tr_data[-3:-1]
    #½print(coordinates)
    if "Unknown" in coordinates:
        zone_name = f"{zone_name} {coordinates[0]}"
        coordinates.pop(0)
    if "Unknown" not in coordinates:
        copy(f"{''.join(coordinates)} : {zone_name}")
    #print(zone_name)
    level_range = tr_data[-1]
    coords = "".join(coordinates)
    print(f"location id: {location_id}")
    print(f"Zone Name: {zone_name}")
    print(f"Coordinates: {coords}")
    print(f"Level range: {level_range}")
    print()
    locations.append(f"{coords} : {zone_name}")
if len(locations) > 1:
    location_choice = int(input(f"more than one location. please select a location[1-{len(locations)}]: ").lower().strip() or 1)-1
    if location_choice > len(locations):
        print(f"location id {location_choice} is not valid")
    elif location_choice == 0:
        copy(f"/ctp {locations[0]}")
    else:
        copy(f"/ctp {locations[location_choice]}")
print(f"selected {locations[location_choice]}")
if fates is not None:
    open_page = input(f'{TARGET.replace("_", " ")} may be FATE exclusive. Open wiki page? [Y/n]: ').lower() or "y"
    if open_page.lower() == "y" or open_page.lower() == "":
        webbrowser.open(URL)
