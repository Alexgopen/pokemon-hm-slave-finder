import os
import requests
import time

serebii_root = "https://www.serebii.net/"
raw_html_path = "cache/raw_html"

attackdex_paths = [
    "attackdex-rby",
    "attackdex-gs",
    "attackdex", # !?
    "attackdex-dp"
]

field_moves = [
    # Gen 1
    ["cut", "fly", "surf", "strength", "flash", "dig", "super fang", "confuse ray", "teleport", "spore", "sleep powder", "sing", "glare", "lovely kiss", "hypnosis", "stun spore", "thunder wave"],
    
    # Gen 2
    ["cut", "fly", "surf", "strength", "flash", "dig", "super fang", "mean look", "whirlpool", "waterfall", "headbutt", "false swipe", "confuse ray", "swagger", "glare", "thief", "teleport", "stun spore", "thunder wave", "spore", "sleep powder", "sing", "lovely kiss", "hypnosis"],

    # Gen 3
    ["cut", "fly", "surf", "strength", "flash", "endeavor", "super fang", "role play", "mean look", "skill swap", "dig", "rock smash", "waterfall", "dive", "false swipe", "confuse ray", "flatter", "glare", "swagger", "thief", "teleport", "stun spore", "yawn", "thunder wave", "spore", "sleep powder", "sing", "lovely kiss", "hypnosis", "grass whistle"],
    
    # Gen 4
    ["cut", "fly", "surf", "strength", "flash", "role play", "endeavor", "super fang", "mean look", "dig", "skill swap", "defog", "rock smash", "waterfall", "rock climb", "whirlpool", "headbutt", "glare", "false swipe", "confuse ray", "flatter", "stun spore", "thunder wave", "swagger", "thief", "teleport", "yawn", "spore", "sleep powder", "sing", "lovely kiss", "hypnosis", "grass whistle"],
]

def scrape_attackdex(gen):
    if gen == 0:
        raise Exception("Gen 0 isn't real!")

    gen -= 1

    attackdex = serebii_root + attackdex_paths[gen]

    save_directory = "{}/gen{}".format(raw_html_path, gen+1)

    os.makedirs(save_directory, exist_ok=True)

    for _, move in enumerate(field_moves[gen]):
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
    for g in range(1, 4+1):
        print("Fetching gen {} field moves".format(g), flush=True)
        scrape_attackdex(g)
        print("", flush=True)

if __name__ == '__main__':
    main()
