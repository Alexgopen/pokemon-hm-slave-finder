import os
import json
from bs4 import BeautifulSoup
from scrape_serebii import hms

allPokemon = []

def get_pokemon_from_file(file, gen):
    pokemon = []

    soup = BeautifulSoup(file, "lxml")

    nameTd = 3
    tableSkip = 1
    dexTabSkip = 0
    rowIndex = 2

    # For some reason Serebii changed the format of their attackdex pages but
    # ONLY for gen 3
    if gen == 3:
        tableSkip = 0
        nameTd = 2
        dexTabSkip = 3
        rowIndex = 1
    dextables = soup.select(".dextable")

    # Skip the first one because it's just the move description
    for dextable in dextables[tableSkip:]:
        for row in dextable.select("tr")[rowIndex:]:
            try:
                name = row.select("td")[nameTd].text
                name = name.replace("Yellow Only", "")
                
                id = row.select("td")[0].text.replace("#", "")

                p = {
                    "name": name,
                    "id": id
                }

                if not p in pokemon:
                    pokemon.append(p)
                if not p in allPokemon:
                    allPokemon.append(p)
            except:
                pass
    
    # More Gen 3 inconsistent formatting on Serebii
    if gen == 3:
        dextabs = soup.select(".dextab")
        for dextab in dextabs[dexTabSkip:]:
            for row in dextab.select("tr")[rowIndex:]:
                try:
                    name = row.select("td")[nameTd].text
                    name = name.replace("Yellow Only", "")
                    
                    id = row.select("td")[0].text.replace("#", "")

                    p = {
                        "name": name,
                        "id": id
                    }

                    if not p in pokemon:
                        pokemon.append(p)
                    if not p in allPokemon:
                        allPokemon.append(p)
                except:
                    pass

    return pokemon

def get_hm_pokemon_for_gen(gen):
    if gen == 0:
        raise Exception("Gen 0 isn't real!")

    print("Gen {}".format(gen), flush=True)

    input_dir = "cache/raw_html/gen{}".format(gen)

    generation = {}
    hmsJson = {}
    tmsJson = {}

    for f in os.listdir(input_dir):
        move = os.path.splitext(f)[0]
        
        despaced_hms = [hm.replace(" ", "") for hm in hms[gen-1]]
        
        if move in despaced_hms:
            with open("{}/{}".format(input_dir, f)) as file:
                hmsJson[move] = get_pokemon_from_file(file, gen)
        else:
            with open("{}/{}".format(input_dir, f)) as file:
                tmsJson[move] = get_pokemon_from_file(file, gen)

    generation["hms"] = hmsJson        
    generation["tms"] = tmsJson
    return generation

if __name__ == '__main__':
    data = {}

    for gen in range(1, 4+1):
        genPokemon = get_hm_pokemon_for_gen(gen)

        data["gen{}".format(gen)] = genPokemon

    with open("cache/all_pokemon.json", "w+") as file:
        file.write(json.dumps(allPokemon, sort_keys=True, indent=4))

    with open("cache/hm_data.json", "w+") as file:
        file.write(json.dumps(data, sort_keys=True, indent=4))
