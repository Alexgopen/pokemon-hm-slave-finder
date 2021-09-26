echo "Beginning Serebii scraping."

cd scraper

echo "Scraping pokemon html from Serebii"
python3 scrape_serebii.py
echo "Scraping pokemon data from raw html"
python3 get_pokemon_from_raw_html.py
echo "Scraping pokemon sprites from Serebii (this may take awhile)"
python3 get_pokemon_img.py

cd - > /dev/null

cp scraper/cache/hm_data.json site/static
cp -r scraper/cache/img site/static

echo "Done"
read -p "Press enter to continue"