# Co-op Adventure — Bedrock 1.19

Two-player adventure add-on for Android Bedrock, with 12 craftable custom items, pixel icons and quick co-op challenges.

## Build the add-on
This branch contains the generator and GitHub Actions workflow. The workflow builds the .mcaddon package and publishes a GitHub Release when the repository permits the workflow to run.

To build locally, install Python 3 and Pillow, then run:
- python -m pip install pillow
- python CoopAdventure/build_pack.py

The output is CoopAdventure/Coop_Adventure_Bedrock_1.19.mcaddon.

## Install
1. Open the .mcaddon file with Minecraft on Android.
2. Edit or create a world and activate both **Co-op Adventure 1.19 BP** and **Co-op Adventure 1.19 RP**.
3. Enable cheats and run /function start.

## Co-op commands
- /function start — starter kit for everyone
- /function wave — enemy wave
- /function boss — ravager and illager arena encounter
- /function loot — supply drop
- /function heal — heal the team
- /function stormnight — thunderstorm survival challenge

## Custom items
Void Blade, Storm Hammer, Ember Dagger, Guardian Charm, Sunbow, Frost Orb, Ranger Token, Phoenix Core, Miner Core, Healer Totem, Shadow Star and Beast Bait.

Bedrock creator APIs can differ between 1.19 minor releases. Test in a copied world first.
