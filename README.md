# The Legend of Pokémon: Zelda's Corruption

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.3-2C9F2C?style=for-the-badge&logo=python&logoColor=white)
![PyTMX](https://img.shields.io/badge/PyTMX-3.32-4B8BBE?style=for-the-badge)
![pyscroll](https://img.shields.io/badge/pyscroll-2.31-4B8BBE?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/Fan_project-non--commercial-lightgrey?style=for-the-badge)

A fan-made **2D adventure game** that mixes two worlds: the exploration and
storytelling of *The Legend of Zelda* with the creature-collecting and turn-based
battles of *Pokémon*. Walk around a hand-drawn world, talk to people, catch and
train Pokémon, and take on gym leaders to save the kingdom.

Built from scratch in **Python** with the Pygame library.

---

## See it in action

The short clip below shows the main character walking through the game world.

https://github.com/Polturgust/Zelmon-project/raw/main/assets/intro_vid.mp4

> If the video does not play directly in your browser, you can
> [click here to download and watch it](assets/intro_vid.mp4).

---

## The story

Princess Zelda has been defeated by the **Yiga Clan**, who corrupted her Pokémon
and spread a poisonous energy across the kingdom of Hyrule.

You play **the Hero**. Defeat the **three gyms**, collect the **three pendants**,
claim the legendary sword, and purify the corrupted Pokémon to bring light back to
the kingdom, earning the title of **Pokémon Master**.

---

## What you can do in the game

- **Explore an open world** – walk freely across towns, routes, caves and buildings.
- **Talk to characters** – non-player characters have their own names, types and dialogue.
- **Catch and collect Pokémon** – build your own team as you travel.
- **Turn-based battles** – fight wild Pokémon and trainers, and swap your Pokémon mid-fight.
- **Gym challenge** – beat three gyms (ice, rock and plant) to progress through the story.
- **Heal at Pokémon Centers** – enter buildings and recover your team.
- **Save your progress** – a full save system lets you continue your adventure later.
- **Controller support** – move around using a controller's left joystick, not just the keyboard.

---

## The world map

Every area you can visit was drawn by hand. Here is the full map of the game,
stitched together into a single picture. (This image is large and may take a
moment to load.)

![Full game map](assets/moam.png)

---

## Built with

| Tool | What it does here |
| --- | --- |
| [Python 3.9+](https://www.python.org/) | The programming language the whole game is written in. |
| [Pygame](https://www.pygame.org/docs/) | Draws the graphics, plays sound, and handles the keyboard and controller. |
| [PyTMX](https://pytmx.readthedocs.io/en/latest/contents.html) | Loads the hand-drawn maps. |
| [pyscroll](https://github.com/bitcraft/pyscroll) | Scrolls the world smoothly as the player moves. |
| [SQLite](https://docs.python.org/3/library/sqlite3.html) | Stores Pokémon stats, player data, and saved games. |

---

## How to play it yourself

You do not need to be a programmer to run the game. Follow these steps:

1. **Get the project** – download this repository as a `.zip` (green *Code* button,
   then *Download ZIP*) and unzip it, or clone it if you use Git.
2. **Install Python** – version 3.9 or newer.
   [Download it here](https://www.python.org/downloads/).
3. **Install the required add-ons** – open a terminal (Command Prompt on Windows),
   then run:
   ```bash
   cd path/to/Zelmon-project
   pip install -r requirements.txt
   ```
4. **Start the game** – from the same terminal:
   ```bash
   cd sources
   python main.py      # on Windows
   python3 main.py     # on Linux or macOS
   ```

That's it. The game window will open and your adventure begins.

---

## Credits and copyright

This is a **non-commercial fan project**. The graphics do not belong to us. The
maps were drawn using tilesets made of elements we did not create ourselves.

- Character spritesheets: [The Spriters Resource](https://www.spriters-resource.com/game_boy_advance/thelegendofzeldatheminishcap/)
- Pokémon sprites: [Pokencyclopedia.info](https://www.pokencyclopedia.info/en/index.php?id=sprites/gen4/spr_hgss)

The logo was drawn by us using assets that do not belong to us:

- [Triforce logo](https://gamepedia.cursecdn.com/zelda_gamepedia_en/9/9c/TLoZ_Series_Triforce_Artwork.png)
- Legendary sword artwork
- Poké Ball artwork
- [Royal Crest emblem](https://gamepedia.cursecdn.com/zelda_gamepedia_en/thumb/0/0b/TLoZ_Series_Royal_Crest_Artwork.png/1200px-TLoZ_Series_Royal_Crest_Artwork.png)
- ["Infected" font](https://www.dafont.com/infected.font)
- ["TRIFORCE" font](https://zeldauniverse.net/media/fonts/)

*The Legend of Zelda* and *Pokémon* are trademarks of Nintendo and The Pokémon
Company. This project is a fan tribute and is not affiliated with or endorsed by them.
