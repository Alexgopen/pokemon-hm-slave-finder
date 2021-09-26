import requests
import os
import time

art_urls = [
    "https://www.serebii.net/pokearth/sprites/rb/{}.png",
    "https://www.serebii.net/pokearth/sprites/gold/{}.png",
    "https://www.serebii.net/pokearth/sprites/rs/{}.png",
    "https://www.serebii.net/pokearth/sprites/dp/{}.png"
]

pokemon_count = [
    151,
    251,
    386,
    493
]

def get_pokemon_art(gen):
    print("Getting img for gen {}".format(gen), flush=True)
    gen -= 1

    save_directory = "cache/img/gen{}".format(gen+1)
    os.makedirs(save_directory, exist_ok=True)

    for i in range(1, pokemon_count[gen] + 1):
        filename = str(i).zfill(3)

        img_url = art_urls[gen].format(filename)
        save_path = "{}/{}.png".format(save_directory, filename)

        if os.path.isfile(save_path):
            print("Skipping sprite {} because we already have it!".format(filename), flush=True)
            continue

        r = requests.get(img_url)

        if r.status_code != 200:
            print("{} returned a {}!".format(img_url, r.status_code), flush=True)
            time.sleep(30)
            continue

        with open(save_path, "wb+") as file:
            for chunk in r:
                file.write(chunk)

        print("{} saved".format(save_path), flush=True)
        time.sleep(1)

if __name__ == '__main__':
    for gen in range(1, 4+1):
        get_pokemon_art(gen)