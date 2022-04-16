import os
import requests
import time

serebii_root = "https://www.serebii.net/"
raw_html_path = "cache/raw_html"

attackdex_paths = [
    "attackdex-rby",
    "attackdex-gs",
    "attackdex", # !?
    "attackdex-dp",
	"attackdex-bw"
]

hms = [
    # Gen 1
    ["cut", "surf", "fly", "strength", "flash"],
    
    # Gen 2
    ["cut", "fly", "surf", "strength", "flash", "whirlpool", "waterfall"],

    # Gen 3
    ["cut", "fly", "surf", "strength", "flash", "rock smash", "waterfall", "dive"],
    
    # Gen 4
    ["cut", "fly", "surf", "strength", "defog", "rock smash", "waterfall", "rock climb", "whirlpool"],
	
	# Gen 5
    ["cut", "fly", "surf", "strength", "waterfall", "dive"],
]

other_moves = [
    # Gen 1
    ["double team", "amnesia", "swords dance", "horn drill", "guillotine", "fissure", "dragon rage", "psywave", "seismic toss", "night shade", "dig", "teleport", "toxic", "leech seed", "super fang", "confuse ray", "spore", "sleep powder", "sing", "glare", "lovely kiss", "hypnosis", "stun spore", "thunder wave"],
    
    # Gen 2
    ["rapid spin", "spikes", "double team", "amnesia", "swords dance", "belly drum", "safeguard", "baton pass", "sacred fire", "horn drill", "guillotine", "fissure", "dragon rage", "perish song", "nightmare", "heal bell", "psywave", "mind reader", "lock-on", "seismic toss", "night shade", "dig", "teleport", "toxic", "leech seed", "thief", "false swipe", "headbutt", "super fang", "mean look", "confuse ray", "swagger", "glare", "stun spore", "thunder wave", "spore", "sleep powder", "sing", "lovely kiss", "hypnosis"],

    # Gen 3
    ["fake out", "cosmic power", "amnesia", "iron defense", "rapid spin", "spikes", "calm mind", "bulk up", "dragon dance", "double team", "wish", "covet", "amnesia", "swords dance", "belly drum", "safeguard", "baton pass", "block", "sacred fire", "will-o-wisp", "horn drill", "guillotine", "fissure", "dragon rage", "perish song", "nightmare", "heal bell", "aromatherapy", "sheer cold", "psywave", "mind reader", "lock-on", "seismic toss", "night shade", "dig", "teleport", "toxic", "leech seed", "thief", "false swipe", "role play", "endeavor", "super fang", "mean look", "skill swap", "confuse ray", "flatter", "glare", "swagger", "stun spore", "yawn", "thunder wave", "spore", "sleep powder", "sing", "lovely kiss", "hypnosis", "grass whistle"],
    
    # Gen 4
    ["barrier", "stockpile", "charge beam", "curse", "roar", "whirlwind", "fake out", "cosmic power", "amnesia", "iron defense", "psybeam", "silver wind", "ancient power", "power gem", "psychic", "extrasensory", "signal beam", "bug buzz", "rapid spin", "spikes", "toxic spikes", "stealth rock", "calm mind", "bulk up", "dragon dance", "nasty plot", "double team", "wish", "covet", "amnesia", "nasty plot", "swords dance", "belly drum", "safeguard", "baton pass", "block", "lava plume", "sacred fire", "will-o-wisp", "horn drill", "guillotine", "fissure", "dragon rage", "perish song", "nightmare", "heal bell", "aromatherapy", "sheer cold", "psywave", "mind reader", "lock-on", "seismic toss", "night shade", "dig", "teleport", "toxic", "leech seed", "thief", "false swipe", "role play", "flash", "endeavor", "super fang", "mean look", "skill swap", "headbutt", "glare", "confuse ray", "flatter", "stun spore", "thunder wave", "swagger", "yawn", "spore", "sleep powder", "sing", "lovely kiss", "hypnosis", "grass whistle"],

	# Gen 5
    ["shadowball", "brickbreak", "psychic", "payback", "shadowclaw", "echoedvoice", "x-scissor", "work up", "scald", "acrobatics", "barrier", "stockpile", "charge beam", "curse", "roar", "whirlwind", "fake out", "cosmic power", "amnesia", "iron defense", "psybeam", "silver wind", "ancient power", "power gem", "psychic", "extrasensory", "signal beam", "bug buzz", "rapid spin", "spikes", "toxic spikes", "stealth rock", "calm mind", "bulk up", "dragon dance", "nasty plot", "double team", "wish", "covet", "amnesia", "nasty plot", "swords dance", "belly drum", "safeguard", "baton pass", "block", "lava plume", "sacred fire", "will-o-wisp", "horn drill", "guillotine", "fissure", "dragon rage", "perish song", "nightmare", "heal bell", "aromatherapy", "sheer cold", "psywave", "mind reader", "lock-on", "seismic toss", "night shade", "dig", "teleport", "toxic", "leech seed", "thief", "false swipe", "role play", "flash", "endeavor", "super fang", "mean look", "skill swap", "headbutt", "glare", "confuse ray", "flatter", "stun spore", "thunder wave", "swagger", "yawn", "spore", "sleep powder", "sing", "lovely kiss", "hypnosis", "grass whistle"],

]

def scrape_attackdex(gen):
    if gen == 0:
        raise Exception("Gen 0 isn't real!")

    gen -= 1

    attackdex = serebii_root + attackdex_paths[gen]

    save_directory = "{}/gen{}".format(raw_html_path, gen+1)

    os.makedirs(save_directory, exist_ok=True)
    
    all_moves = hms[gen] + other_moves[gen]
        
    print(all_moves, flush=True)

    for _, move in enumerate(all_moves):
        move = move.replace(" ", "")

        move_url = "{}/{}.shtml".format(attackdex, move)
        save_path = "{}/{}.cshtml".format(save_directory, move)

        if os.path.isfile(save_path):
            print("Skipping {} because we already have it!".format(move), flush=True)
            continue

        print("Fetching {}...".format(move_url), flush=True)
        r = requests.get(move_url)

        if r.status_code != 200:
            print("{} returned a {}!".format(move_url, r.status_code), flush=True)
            time.sleep(2)
            continue

        with open(save_path, "w+") as file:
            file.write(r.text)

        print("{} saved".format(save_path), flush=True)
        time.sleep(2)

def main():
    for g in range(1, 5+1):
        print("Fetching gen {} moves:".format(g), flush=True)
        scrape_attackdex(g)
        print("", flush=True)

if __name__ == '__main__':
    main()
