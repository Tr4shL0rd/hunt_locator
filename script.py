from bs4 import BeautifulSoup 
import requests
import sys
import webbrowser
from pyperclip import copy
import re

def is_page(soup_var:any):
    
    no_article = soup_var.find_all(class_="noarticletext mw-content-ltr")
    #print(len(no_article))
    if len(no_article) == 0:
        return True
    #print("There is currently no text in this page." in no_article[0].text)
    return False if "There is currently no text in this page." in no_article[0].text else True

def get_info():

    LOWER_CASE_WORDS = ["of", "the"]
    BASE_URL = "https://ffxiv.consolegameswiki.com/wiki/"
    target = None
    if len(sys.argv) == 1:
        target = "_".join(input("Target: ")).title()
    target = "_".join(sys.argv[1:]).title()

    # convert target string to a list
    target_name_split = target.split("_")
    #TODO: really stupid double nesting. use ZIP instead!
    for bad_word in LOWER_CASE_WORDS:
        for word in target_name_split:

            if bad_word.lower() == word.lower():
                # replace word at index
                target_name_split[target_name_split.index(word)] = bad_word.lower()
    # fix for targets with hyphens in name (probably broken)
    if len(target.split()) == 1:
        target = target.lower()
    URL = f"{BASE_URL}{target}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    if not is_page(soup):
        print(f"\"{target}\" is not valid.")
        exit()
    location_tables = soup.find(class_="location table")
    fates = soup.find(id="FATEs")
    try:
        trs = location_tables.find_all("tr")[1:]
    except AttributeError:
        # matches the coords of a wiki page
        pattern = r'\(\w+\d+,\w+\d+\)'
        location_name = soup.find_all(class_="mw-headline")
        coords = soup.find_all("p")
        location_pretty_name = location_name[1].text
        #match = re.findall(pattern, coords)
        for coord in coords:
            matches = re.findall(pattern, coord.text)
            if matches:
                places = coord.text
                break
        print(f"location: {location_pretty_name}")
        print(f"coords: {places}")
        copy(f"/ctp {places.split()[0]} : {location_pretty_name}")
        exit()
        #input()

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
        else:
            copy(f"/ctp {locations[location_choice]}")
        print(f"selected {locations[location_choice]}")
    else:
        copy(f"/ctp {locations[0]}")
    if fates is not None:
        open_page = input(f'{target.replace("_", " ")} may be FATE exclusive. Open wiki page? [Y/n]: ').lower() or "y"
        if open_page.lower() == "y" or open_page.lower() == "":
            webbrowser.open(URL)

if __name__ == "__main__":
    get_info()
