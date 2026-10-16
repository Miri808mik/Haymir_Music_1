#!/usr/bin/env python3
"""Build a lightweight Minecraft Bedrock 1.19 co-op adventure add-on."""
import json, shutil, uuid, zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "_build"
if WORK.exists():
    shutil.rmtree(WORK)
BP, RP = WORK / "CoopAdventure_BP", WORK / "CoopAdventure_RP"
for p in (BP / "items", BP / "recipes", BP / "functions", RP / "textures" / "items"):
    p.mkdir(parents=True, exist_ok=True)

def uid(): return str(uuid.uuid4())
bph, bpm, rph, rpm = [uid() for _ in range(4)]
def write_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

write_json(BP / "manifest.json", {
    "format_version": 2,
    "header": {"name":"Co-op Adventure 1.19 BP",
        "description":"Co-op gear, recipes, loot and survival challenges.",
        "uuid":bph,"version":[1,0,0],"min_engine_version":[1,19,0]},
    "modules":[{"type":"data","uuid":bpm,"version":[1,0,0]}],
    "dependencies":[{"uuid":rph,"version":[1,0,0]}]})
write_json(RP / "manifest.json", {
    "format_version": 2,
    "header": {"name":"Co-op Adventure 1.19 RP",
        "description":"Original pixel item icons for Co-op Adventure.",
        "uuid":rph,"version":[1,0,0],"min_engine_version":[1,19,0]},
    "modules":[{"type":"resources","uuid":rpm,"version":[1,0,0]}]})

items = [
("void_blade","Void Blade",(132,65,225),12,[["minecraft:obsidian","minecraft:amethyst_shard","minecraft:obsidian"],["","minecraft:netherite_ingot",""],["","minecraft:blaze_rod",""]]),
("storm_hammer","Storm Hammer",(50,190,245),10,[["minecraft:iron_ingot","minecraft:lightning_rod","minecraft:iron_ingot"],["","minecraft:netherite_ingot",""],["","minecraft:blaze_rod",""]]),
("ember_dagger","Ember Dagger",(245,80,35),8,[["minecraft:blaze_powder","minecraft:iron_ingot","minecraft:blaze_powder"],["","minecraft:gold_ingot",""],["","minecraft:stick",""]]),
("guardian_charm","Guardian Charm",(60,225,155),0,[["minecraft:emerald","minecraft:diamond","minecraft:emerald"],["minecraft:gold_ingot","minecraft:totem_of_undying","minecraft:gold_ingot"],["","minecraft:amethyst_shard",""]]),
("sunbow","Sunbow",(255,190,45),0,[["minecraft:string","minecraft:blaze_rod","minecraft:string"],["minecraft:gold_ingot","minecraft:amethyst_shard","minecraft:gold_ingot"],["","minecraft:stick",""]]),
("frost_orb","Frost Orb",(100,220,255),0,[["minecraft:packed_ice","minecraft:diamond","minecraft:packed_ice"],["","minecraft:heart_of_the_sea",""],["","minecraft:amethyst_shard",""]]),
("ranger_token","Ranger Token",(100,195,95),0,[["minecraft:leather","minecraft:emerald","minecraft:leather"],["","minecraft:compass",""],["","minecraft:iron_ingot",""]]),
("phoenix_core","Phoenix Core",(255,85,40),0,[["minecraft:blaze_powder","minecraft:ghast_tear","minecraft:blaze_powder"],["minecraft:gold_ingot","minecraft:nether_star","minecraft:gold_ingot"],["","minecraft:diamond",""]]),
("miner_drill","Miner Core",(175,185,200),0,[["minecraft:iron_ingot","minecraft:diamond","minecraft:iron_ingot"],["","minecraft:gold_ingot",""],["","minecraft:iron_pickaxe",""]]),
("healer_totem","Healer Totem",(255,100,175),0,[["minecraft:gold_ingot","minecraft:glistering_melon_slice","minecraft:gold_ingot"],["minecraft:emerald","minecraft:diamond","minecraft:emerald"],["","minecraft:amethyst_shard",""]]),
("shadow_star","Shadow Star",(80,65,125),0,[["minecraft:obsidian","minecraft:ender_pearl","minecraft:obsidian"],["","minecraft:amethyst_shard",""],["","minecraft:ender_pearl",""]]),
("beast_bait","Beast Bait",(155,100,55),0,[["minecraft:rotten_flesh","minecraft:bone","minecraft:rotten_flesh"],["","minecraft:leather",""],["","minecraft:bone",""]]),
]
atlas={"resource_pack_name":"Co-op Adventure 1.19","texture_name":"atlas.items","texture_data":{}}
for ident, label, color, damage, recipe in items:
    comp={"minecraft:icon":{"texture":ident},"minecraft:display_name":{"value":label},
          "minecraft:max_stack_size":1 if ident not in ("ranger_token","beast_bait") else 16}
    if damage:
        comp["minecraft:damage"]=damage
        comp["minecraft:hand_equipped"]=True
    write_json(BP/"items"/(ident+".json"), {"format_version":"1.16.100",
        "minecraft:item":{"description":{"identifier":"coop:"+ident,"category":"Equipment"},"components":comp}})
    im=Image.new("RGBA",(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    col=(*color,255); dark=(25,18,42,255)
    if ident in ("void_blade","storm_hammer","ember_dagger","sunbow","miner_drill"):
        d.line((3,13,12,3),fill=dark,width=4); d.line((3,13,12,3),fill=col,width=2)
        d.line((2,12,5,15),fill=(190,155,100,255),width=2)
        if ident=="storm_hammer": d.rectangle((7,1,14,5),fill=col,outline=dark)
        if ident=="sunbow": d.arc((2,2,13,14),250,110,fill=col,width=2)
    else:
        d.polygon([(8,1),(13,5),(12,11),(8,15),(4,11),(2,5)],fill=col,outline=dark)
        d.polygon([(8,3),(11,6),(8,12),(5,6)],fill=(225,245,255,190))
        if ident=="phoenix_core":
            d.line((8,0,8,15),fill=(255,230,100,255),width=1); d.line((1,8,14,8),fill=(255,230,100,255),width=1)
    im.save(RP/"textures"/"items"/(ident+".png"))
    atlas["texture_data"][ident]={"textures":"textures/items/"+ident}
write_json(RP/"textures"/"item_texture.json",atlas)

symbols="ABCDEFGHI"
for ident, label, color, damage, recipe in items:
    key, pattern={},[]
    for ri,row in enumerate(recipe):
        line=""
        for ci,ingredient in enumerate(row):
            if ingredient:
                ch=symbols[ri*3+ci]; key[ch]={"item":ingredient}; line+=ch
            else: line+=" "
        pattern.append(line.rstrip())
    write_json(BP/"recipes"/(ident+".json"), {"format_version":"1.12.0",
        "minecraft:recipe_shaped":{"description":{"identifier":"coop:recipe_"+ident},
        "tags":["crafting_table"],"pattern":pattern,"key":key,
        "result":{"item":"coop:"+ident,"count":1}}})

functions = {
"start.mcfunction":["title @a title §dCO-OP ADVENTURE","title @a subtitle §bGear up. Explore. Survive together!",
"give @a iron_sword 1","give @a bow 1","give @a arrow 32","give @a cooked_beef 16",
"give @a torch 32","give @a golden_apple 2","give @a shield 1",
"effect @a night_vision 120 0 true","say §d[Adventure] §fStarter kit delivered to everyone!"],
"wave.mcfunction":["say §c[Adventure] Wave incoming! Stay together!","summon zombie ~3 ~ ~",
"summon zombie ~-3 ~ ~","summon skeleton ~ ~ ~4","summon spider ~ ~ ~-4","summon husk ~5 ~ ~5"],
"boss.mcfunction":["say §5[Adventure] The arena boss has arrived!","summon ravager ~ ~ ~",
"summon evoker ~4 ~ ~","summon pillager ~-4 ~ ~","summon vindicator ~ ~ ~4",
"effect @e[type=ravager,r=12] strength 90 1 true","effect @e[type=ravager,r=12] resistance 90 0 true"],
"loot.mcfunction":["say §6[Adventure] Supply drop!","give @p diamond 3","give @p emerald 8",
"give @p golden_apple 2","give @p experience_bottle 16"],
"heal.mcfunction":["effect @a instant_health 1 1 true","effect @a saturation 1 1 true","say §a[Adventure] Team healed!"],
"stormnight.mcfunction":["time set night","weather thunder 600","say §8[Adventure] Storm night started. Survive the waves!"]}
for name, lines in functions.items():
    (BP/"functions"/name).write_text("\n".join(lines)+"\n",encoding="utf-8")

readme = """# Co-op Adventure — Minecraft Bedrock Android 1.19

A lightweight two-player adventure add-on with original pixel icons, 12 custom craftable items, and command-driven co-op encounters.

## Install
1. Download the .mcaddon release asset and open it with Minecraft.
2. Create/edit a world and activate both **Co-op Adventure 1.19 BP** and **Co-op Adventure 1.19 RP**.
3. Enable cheats, then run /function start.
4. If your exact Bedrock 1.19 build requires creator experiments for custom items, enable the relevant toggle in a copied test world first.

## Co-op commands
- /function start — team starter kit
- /function wave — spawn an enemy wave near the command executor
- /function boss — arena-style encounter with a ravager and illagers
- /function loot — supply drop for the nearest player
- /function heal — heal the team
- /function stormnight — thunderstorm survival challenge

## Item set
Void Blade, Storm Hammer, Ember Dagger, Guardian Charm, Sunbow, Frost Orb, Ranger Token, Phoenix Core, Miner Core, Healer Totem, Shadow Star and Beast Bait.

Bedrock creator APIs differ between minor versions. Test in a copied world first. This is a Bedrock add-on, not a Java Edition mod.
"""
(ROOT/"README.md").write_text(readme,encoding="utf-8")
package=ROOT/"Coop_Adventure_Bedrock_1.19.mcaddon"
with zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED) as z:
    for folder in (BP,RP):
        for file in folder.rglob("*"):
            if file.is_file(): z.write(file,file.relative_to(WORK))
with zipfile.ZipFile(package) as z:
    assert z.testzip() is None
print(f"Built {package} ({package.stat().st_size} bytes); {len(items)} items, {len(items)} recipes, {len(functions)} functions.")
