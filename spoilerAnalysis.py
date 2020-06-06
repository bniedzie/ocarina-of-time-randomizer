###############################################################################
# This script reads large numbers of Zelda Ocarina of Time Randomizer
# spoiler logs and produces CSVs analyzing item placement, sphere count,
# and way of the hero location distributions.
#
# Author: Benjamin Niedzielski
# Last Modified: June 5, 2020
#
# This script may be shared and modified, so long as the original author
# data and this license information is unaltered.
#
# Zelda Ocarina of Time Randomizer can be found at https://ootrandomizer.com/.
###############################################################################

import json;
import csv;

############################################
# Change these values based on your file
# structure and desired number of logs.
############################################
inputFolder = 'output';
inputFileStart = 'OoT_98155_9PN91HR56Z-';
inputFileEnd = '_Spoiler.json';
numOfLogs = 10000;

############################################
# Output files
############################################
itemCSV = 'items.csv';
sphereCSV = 'sphere.csv';
barrenCSV = 'woth.csv';

############################################
# Constants for the game world.
# Can be modified to include scrub and
# shopsanity or for future changes.
############################################

# Locations to show in the CSV.  Results will display in this order
locations = ["Links Pocket", "Queen Gohma", "King Dodongo", "Barinade", "Phantom Ganon", "Volvagia", "Morpha", "Bongo Bongo", "Twinrova", "Song from Saria", "Sheik Forest Song", "Song from Ocarina of Time", "Sheik at Colossus", "Sheik at Temple", "Impa at Castle", "Sheik in Kakariko", "Song at Windmill", "Song from Composer Grave", "Sheik in Crater", "Song from Malon", "Sheik in Ice Cavern", "Kokiri Sword Chest", "Mido Chest Top Left", "Mido Chest Top Right", "Mido Chest Bottom Left", "Mido Chest Bottom Right", "Skull Kid", "Ocarina Memory Game", "Target in Woods", "LW Deku Scrub Deku Stick Upgrade", "Underwater Bottle", "Lake Hylia Sun", "Lake Hylia Freestanding PoH", "Diving in the Lab", "Child Fishing", "Adult Fishing", "Gerudo Valley Crate Freestanding PoH", "Gerudo Valley Waterfall Freestanding PoH", "Gerudo Valley Hammer Rocks Chest", "Gerudo Fortress Rooftop Chest", "Horseback Archery 1000 Points", "Horseback Archery 1500 Points", "Haunted Wasteland Structure Chest", "Colossus Freestanding PoH", "Desert Colossus Fairy Reward", "Zelda", "Hyrule Castle Fairy Reward", "Ganons Castle Fairy Reward", "10 Big Poes", "Child Shooting Gallery", "Bombchu Bowling Bomb Bag", "Bombchu Bowling Piece of Heart", "Treasure Chest Game", "Dog Lady", "Man on Roof", "Anju as Adult", "Anjus Chickens", "10 Gold Skulltula Reward", "20 Gold Skulltula Reward", "30 Gold Skulltula Reward", "40 Gold Skulltula Reward", "50 Gold Skulltula Reward", "Impa House Freestanding PoH", "Windmill Freestanding PoH", "Adult Shooting Gallery", "Graveyard Freestanding PoH", "Gravedigging Tour", "Shield Grave Chest", "Heart Piece Grave Chest", "Composer Grave Chest", "Hookshot Chest", "Dampe Race Freestanding PoH", "Death Mountain Bombable Chest", "DM Trail Freestanding PoH", "Biggoron", "Goron City Leftmost Maze Chest", "Goron City Left Maze Chest", "Goron City Right Maze Chest", "Goron City Pot Freestanding PoH", "Rolling Goron as Child", "Link the Goron", "Darunias Joy", "DM Crater Wall Freestanding PoH", "DM Crater Volcano Freestanding PoH", "Crater Fairy Reward", "Mountain Summit Fairy Reward", "Frog Ocarina Game", "Frogs in the Rain", "Zora River Lower Freestanding PoH", "Zora River Upper Freestanding PoH", "Diving Minigame", "Zoras Domain Torch Run", "King Zora Thawed", "Zoras Fountain Iceberg Freestanding PoH", "Zoras Fountain Bottom Freestanding PoH", "Zoras Fountain Fairy Reward", "Talons Chickens", "Lon Lon Tower Freestanding PoH", "Ganons Tower Boss Key Chest", "Kokiri Forest Storms Grotto Chest", "Lost Woods Generic Grotto Chest", "Deku Theater Skull Mask", "Deku Theater Mask of Truth", "LW Grotto Deku Scrub Deku Nut Upgrade", "Wolfos Grotto Chest", "Remote Southern Grotto Chest", "Field Near Lake Outside Fence Grotto Chest", "HF Grotto Deku Scrub Piece of Heart", "Field West Castle Town Grotto Chest", "Tektite Grotto Freestanding PoH", "Redead Grotto Chest", "Kakariko Back Grotto Chest", "Mountain Storms Grotto Chest", "Top of Crater Grotto Chest", "Zora River Plateau Open Grotto Chest", "Deku Tree Lobby Chest", "Deku Tree Compass Chest", "Deku Tree Compass Room Side Chest", "Deku Tree Basement Chest", "Deku Tree Slingshot Chest", "Deku Tree Slingshot Room Side Chest", "Queen Gohma Heart", "Dodongos Cavern Map Chest", "Dodongos Cavern Compass Chest", "Dodongos Cavern Bomb Flower Platform", "Dodongos Cavern Bomb Bag Chest", "Dodongos Cavern End of Bridge Chest", "Chest Above King Dodongo", "King Dodongo Heart", "Boomerang Chest", "Jabu Jabus Belly Map Chest", "Jabu Jabus Belly Compass Chest", "Barinade Heart", "Forest Temple First Chest", "Forest Temple Chest Behind Lobby", "Forest Temple Outside Hookshot Chest", "Forest Temple Well Chest", "Forest Temple Map Chest", "Forest Temple Falling Room Chest", "Forest Temple Block Push Chest", "Forest Temple Boss Key Chest", "Forest Temple Floormaster Chest", "Forest Temple Bow Chest", "Forest Temple Red Poe Chest", "Forest Temple Blue Poe Chest", "Forest Temple Near Boss Chest", "Phantom Ganon Heart", "Bottom of the Well Front Left Hidden Wall", "Bottom of the Well Front Center Bombable", "Bottom of the Well Right Bottom Hidden Wall", "Bottom of the Well Center Large Chest", "Bottom of the Well Center Small Chest", "Bottom of the Well Back Left Bombable", "Bottom of the Well Freestanding Key", "Bottom of the Well Defeat Boss", "Bottom of the Well Invisible Chest", "Bottom of the Well Underwater Front Chest", "Bottom of the Well Underwater Left Chest", "Bottom of the Well Basement Chest", "Bottom of the Well Locked Pits", "Bottom of the Well Behind Right Grate", "Fire Temple Chest Near Boss", "Fire Temple Fire Dancer Chest", "Fire Temple Boss Key Chest", "Volvagia Heart", "Fire Temple Big Lava Room Open Chest", "Fire Temple Big Lava Room Bombable Chest", "Fire Temple Boulder Maze Lower Chest", "Fire Temple Boulder Maze Upper Chest", "Fire Temple Boulder Maze Side Room", "Fire Temple Boulder Maze Bombable Pit", "Fire Temple Scarecrow Chest", "Fire Temple Map Chest", "Fire Temple Compass Chest", "Fire Temple Highest Goron Chest", "Fire Temple Megaton Hammer Chest", "Ice Cavern Map Chest", "Ice Cavern Compass Chest", "Ice Cavern Iron Boots Chest", "Ice Cavern Freestanding PoH", "Morpha Heart", "Water Temple Map Chest", "Water Temple Compass Chest", "Water Temple Torches Chest", "Water Temple Dragon Chest", "Water Temple Central Bow Target Chest", "Water Temple Boss Key Chest", "Water Temple Cracked Wall Chest", "Water Temple Central Pillar Chest", "Water Temple Dark Link Chest", "Water Temple River Chest", "Shadow Temple Map Chest", "Shadow Temple Hover Boots Chest", "Shadow Temple Compass Chest", "Shadow Temple Early Silver Rupee Chest", "Shadow Temple Invisible Blades Visible Chest", "Shadow Temple Invisible Blades Invisible Chest", "Shadow Temple Falling Spikes Lower Chest", "Shadow Temple Falling Spikes Upper Chest", "Shadow Temple Falling Spikes Switch Chest", "Shadow Temple Invisible Spikes Chest", "Shadow Temple Freestanding Key", "Shadow Temple Wind Hint Chest", "Shadow Temple After Wind Enemy Chest", "Shadow Temple After Wind Hidden Chest", "Shadow Temple Spike Walls Left Chest", "Shadow Temple Boss Key Chest", "Shadow Temple Hidden Floormaster Chest", "Bongo Bongo Heart", "Gerudo Training Grounds Lobby Left Chest", "Gerudo Training Grounds Lobby Right Chest", "Gerudo Training Grounds Stalfos Chest", "Gerudo Training Grounds Beamos Chest", "Gerudo Training Grounds Hidden Ceiling Chest", "Gerudo Training Grounds Maze Path First Chest", "Gerudo Training Grounds Maze Path Second Chest", "Gerudo Training Grounds Maze Path Third Chest", "Gerudo Training Grounds Maze Path Final Chest", "Gerudo Training Grounds Maze Right Central Chest", "Gerudo Training Grounds Maze Right Side Chest", "Gerudo Training Grounds Freestanding Key", "Gerudo Training Grounds Underwater Silver Rupee Chest", "Gerudo Training Grounds Hammer Room Clear Chest", "Gerudo Training Grounds Hammer Room Switch Chest", "Gerudo Training Grounds Eye Statue Chest", "Gerudo Training Grounds Near Scarecrow Chest", "Gerudo Training Grounds Before Heavy Block Chest", "Gerudo Training Grounds Heavy Block First Chest", "Gerudo Training Grounds Heavy Block Second Chest", "Gerudo Training Grounds Heavy Block Third Chest", "Gerudo Training Grounds Heavy Block Fourth Chest", "Spirit Temple Child Left Chest", "Spirit Temple Child Right Chest", "Spirit Temple Child Climb East Chest", "Spirit Temple Child Climb North Chest", "Spirit Temple Compass Chest", "Spirit Temple Early Adult Right Chest", "Spirit Temple First Mirror Right Chest", "Spirit Temple First Mirror Left Chest", "Spirit Temple Map Chest", "Spirit Temple Sun Block Room Chest", "Spirit Temple Statue Hand Chest", "Spirit Temple NE Main Room Chest", "Silver Gauntlets Chest", "Mirror Shield Chest", "Spirit Temple Near Four Armos Chest", "Spirit Temple Hallway Left Invisible Chest", "Spirit Temple Hallway Right Invisible Chest", "Spirit Temple Boss Key Chest", "Spirit Temple Topmost Chest", "Twinrova Heart", "Ganons Castle Forest Trial Chest", "Ganons Castle Water Trial Left Chest", "Ganons Castle Water Trial Right Chest", "Ganons Castle Shadow Trial First Chest", "Ganons Castle Shadow Trial Second Chest", "Ganons Castle Spirit Trial First Chest", "Ganons Castle Spirit Trial Second Chest", "Ganons Castle Light Trial First Left Chest", "Ganons Castle Light Trial Second Left Chest", "Ganons Castle Light Trial Third Left Chest", "Ganons Castle Light Trial First Right Chest", "Ganons Castle Light Trial Second Right Chest", "Ganons Castle Light Trial Third Right Chest", "Ganons Castle Light Trial Invisible Enemies Chest", "Ganons Castle Light Trial Lullaby Chest", "Kokiri Shop Item 1", "Zeldas Letter", "Master Sword Pedestal", "Gift from Saria", "Castle Town Bazaar Item 7", "Goron Shop Item 5", "Gerudo Fortress North F1 Carpenter", "Gerudo Fortress Membership Card", "Deliver Ruto's Letter", "Zora River Plateau Open Grotto Lone Fish", "Ganon", "GS Lon Lon Ranch Rain Shed", "GS Kakariko Guard's House", "GS Kakariko Tree", "GS Castle Market Guard House", "GS Kakariko House Under Construction", "GS Lon Lon Ranch Tree", "GS Kakariko Skulltula House", "GS Hyrule Castle Tree", "Pierre", "GS Kokiri Know It All House", "GS Lake Hylia Small Island", "GS Deku Tree Compass Room", "GS Zora River Tree", "GS Deku Tree Basement Gate", "GS Outside Ganon's Castle", "GS Goron City Center Platform", "GS Mountain Trail Path to Crater", "GS Mountain Trail Above Dodongo's Cavern", "GS Zora's Domain Frozen Waterfall", "GS Dodongo's Cavern East Side Room", "GS Dodongo's Cavern Vines Above Stairs", "GS Mountain Trail Bomb Alcove", "GS Zora River Above Bridge", "GS Forest Temple Lobby", "GS Hyrule Field near Kakariko", "GS Forest Temple Outdoor East", "GS Fire Temple Basement", "GS Forest Temple First Room", "GS Dodongo's Cavern Scarecrow", "GS Deku Tree Basement Vines", "Kakariko Potion Shop Item 5", "GS Spirit Temple Metal Fence", "Sell Big Poe from Castle Town Rupee Room", "GS Goron City Boulder Maze", "GS Zora River Ladder", "GS Kakariko Watchtower", "GS Zora River Near Raised Grottos", "GS Kakariko Above Impa's House", "GS Kokiri House of Twins", "GS Death Mountain Crater Crate", "GS Sacred Forest Meadow", "GS Lake Hylia Lab Wall", "GS Gerudo Valley Small Bridge", "GS Lon Lon Ranch Back Wall", "GS Fire Temple Song of Time Room", "GS Graveyard Wall", "GS Lon Lon Ranch House Window", "Ice Cavern Blue Fire", "GS Jabu Jabu Near Boss", "Magic Bean Salesman", "Zora River Plateau Open Grotto Bug Shrub", "GS Hyrule Castle Grotto", "GS Mountain Trail Bean Patch", "GS Graveyard Bean Patch", "GS Mountain Crater Bean Patch", "GS Kokiri Bean Patch", "GS Gerudo Valley Bean Patch", "GS Lake Hylia Bean Patch", "GS Lost Woods Bean Patch Near Bridge", "GS Lost Woods Bean Patch Near Stage", "GS Dodongo's Cavern Back Room", "GS Desert Colossus Hill", "GS Dodongo's Cavern Alcove Above Stairs", "GS Lost Woods Above Stage", "GS Spirit Temple Bomb for Light Room", "GS Fire Temple Unmarked Bomb Wall", "GS Desert Colossus Bean Patch", "Zora Shop Item 1", "Hyrule Field Big Poe Kill", "GS Desert Colossus Tree", "GS Forest Temple Outdoor West", "GS Forest Temple Basement", "GS Deku Tree Basement Back Room", "GS Spirit Temple Boulder Room", "GS Hyrule Field Near Gerudo Valley", "GS Gerudo Fortress Top Floor", "GS Gerudo Valley Behind Tent", "GS Gerudo Valley Pillar", "GS Lab Underwater Crate", "GS Water Temple South Basement", "GS Gerudo Fortress Archery Range", "Bombchu Shop Item 4", "GS Lake Hylia Giant Tree", "GS Zora's Fountain Tree", "GS Jabu Jabu Water Switch Room", "GS Zora's Fountain Hidden Cave", "Castle Town Potion Shop Item 5", "Bombchu Shop Item 8", "GS Well East Inner Room", "GS Well Like Like Cage", "GS Zora's Fountain Above the Log", "GS Well West Inner Room", "GS Jabu Jabu Lobby Basement Lower", "GS Jabu Jabu Lobby Basement Upper", "GS Spirit Temple Hall to West Iron Knuckle", "GS Ice Cavern Spinning Scythe Room", "GS Shadow Temple Crusher Room", "GS Water Temple Central Room", "GS Wasteland Ruins", "GS Water Temple Falling Platform Room", "GS Spirit Temple Lobby", "GS Shadow Temple Single Giant Pot", "GS Ice Cavern Push Block Room", "GS Shadow Temple Like Like Room", "GS Ice Cavern Heart Piece Room", "GS Water Temple Near Boss Key Chest", "GS Fire Temple East Tower Top", "GS Fire Temple East Tower Climb", "Ganons Castle Water Trial Blue Fire", "GS Shadow Temple Triple Giant Pot", "GS Water Temple Serpent River", "GS Shadow Temple Near Ship"];

# Dictionary with check as key, and its major location as value, based on LocationList.py
locationMap = {'Kokiri Sword Chest': 'Kokiri Forest', 'Mido Chest Top Left': 'Kokiri Forest', 'Mido Chest Top Right': 'Kokiri Forest', 'Mido Chest Bottom Left': 'Kokiri Forest', 'Mido Chest Bottom Right': 'Kokiri Forest', 'Shield Grave Chest': 'the Graveyard', 'Heart Piece Grave Chest': 'the Graveyard', 'Composer Grave Chest': 'the Graveyard', 'Death Mountain Bombable Chest': 'Death Mountain Trail', 'Goron City Leftmost Maze Chest': 'Goron City', 'Goron City Right Maze Chest': 'Goron City', 'Goron City Left Maze Chest': 'Goron City', 'Zoras Domain Torch Run': "Zora's Domain", 'Hookshot Chest': 'the Graveyard', 'Gerudo Valley Hammer Rocks Chest': 'Gerudo Valley', 'Gerudo Fortress Rooftop Chest': "Gerudo's Fortress", 'Haunted Wasteland Structure Chest': 'Haunted Wasteland', 'Redead Grotto Chest': 'Kakariko Village', 'Wolfos Grotto Chest': 'Sacred Forest Meadow', 'Field West Castle Town Grotto Chest': 'Hyrule Field', 'Remote Southern Grotto Chest': 'Hyrule Field', 'Field Near Lake Outside Fence Grotto Chest': 'Hyrule Field', 'Kakariko Back Grotto Chest': 'Kakariko Village', 'Zora River Plateau Open Grotto Chest': "Zora's River", 'Kokiri Forest Storms Grotto Chest': 'Kokiri Forest', 'Lost Woods Generic Grotto Chest': 'the Lost Woods', 'Mountain Storms Grotto Chest': 'Death Mountain Trail', 'Top of Crater Grotto Chest': 'Death Mountain Crater', 'Treasure Chest Game': 'the Market', 'Zoras Fountain Fairy Reward': "Zora's Fountain", 'Hyrule Castle Fairy Reward': 'Hyrule Castle', 'Desert Colossus Fairy Reward': 'Desert Colossus', 'Mountain Summit Fairy Reward': 'Death Mountain Trail', 'Crater Fairy Reward': 'Death Mountain Crater', 'Ganons Castle Fairy Reward': "outside Ganon's Castle", 'Sheik Forest Song': 'Sacred Forest Meadow', 'Sheik in Crater': 'Death Mountain Crater', 'Sheik in Ice Cavern': 'Ice Cavern', 'Sheik at Colossus': 'Desert Colossus', 'Sheik in Kakariko': 'Kakariko Village', 'Sheik at Temple': 'Temple of Time', 'Impa at Castle': 'Hyrule Castle', 'Song from Malon': 'Lon Lon Ranch', 'Song from Saria': 'Sacred Forest Meadow', 'Song from Composer Grave': 'the Graveyard', 'Song from Ocarina of Time': 'Hyrule Field', 'Song at Windmill': 'Kakariko Village', 'Darunias Joy': 'Goron City', 'Diving Minigame': "Zora's Domain", 'Child Fishing': 'Lake Hylia', 'Adult Fishing': 'Lake Hylia', 'Diving in the Lab': 'Lake Hylia', 'Link the Goron': 'Goron City', 'King Zora Thawed': "Zora's Domain", 'Bombchu Bowling Bomb Bag': 'the Market', 'Bombchu Bowling Piece of Heart': 'the Market', 'Bombchu Bowling Bombchus': 'the Market', 'Dog Lady': 'the Market', 'Skull Kid': 'the Lost Woods', 'Ocarina Memory Game': 'the Lost Woods', '10 Gold Skulltula Reward': 'Kakariko Village', '20 Gold Skulltula Reward': 'Kakariko Village', '30 Gold Skulltula Reward': 'Kakariko Village', '40 Gold Skulltula Reward': 'Kakariko Village', '50 Gold Skulltula Reward': 'Kakariko Village', 'Man on Roof': 'Kakariko Village', 'Frog Ocarina Game': "Zora's River", 'Frogs in the Rain': "Zora's River", 'Horseback Archery 1000 Points': "Gerudo's Fortress", 'Horseback Archery 1500 Points': "Gerudo's Fortress", 'Child Shooting Gallery': 'the Market', 'Adult Shooting Gallery': 'Kakariko Village', 'Target in Woods': 'the Lost Woods', 'Deku Theater Skull Mask': 'the Lost Woods', 'Deku Theater Mask of Truth': 'the Lost Woods', 'Anju as Adult': 'Kakariko Village', 'Biggoron': 'Death Mountain Trail', 'Anjus Chickens': 'Kakariko Village', 'Talons Chickens': 'Lon Lon Ranch', '10 Big Poes': 'the Market', 'Rolling Goron as Child': 'Goron City', 'Underwater Bottle': 'Lake Hylia', 'Lake Hylia Sun': 'Lake Hylia', 'Impa House Freestanding PoH': 'Kakariko Village', 'Tektite Grotto Freestanding PoH': 'Hyrule Field', 'Windmill Freestanding PoH': 'Kakariko Village', 'Dampe Race Freestanding PoH': 'the Graveyard', 'Lon Lon Tower Freestanding PoH': 'Lon Lon Ranch', 'Graveyard Freestanding PoH': 'the Graveyard', 'Gravedigging Tour': 'the Graveyard', 'Zora River Lower Freestanding PoH': "Zora's River", 'Zora River Upper Freestanding PoH': "Zora's River", 'Lake Hylia Freestanding PoH': 'Lake Hylia', 'Zoras Fountain Iceberg Freestanding PoH': "Zora's Fountain", 'Zoras Fountain Bottom Freestanding PoH': "Zora's Fountain", 'Gerudo Valley Waterfall Freestanding PoH': 'Gerudo Valley', 'Gerudo Valley Crate Freestanding PoH': 'Gerudo Valley', 'Colossus Freestanding PoH': 'Desert Colossus', 'DM Trail Freestanding PoH': 'Death Mountain Trail', 'DM Crater Wall Freestanding PoH': 'Death Mountain Crater', 'DM Crater Volcano Freestanding PoH': 'Death Mountain Crater', 'Goron City Pot Freestanding PoH': 'Goron City', 'Deku Tree Lobby Chest': 'Deku Tree', 'Deku Tree Slingshot Chest': 'Deku Tree', 'Deku Tree Slingshot Room Side Chest': 'Deku Tree', 'Deku Tree Compass Chest': 'Deku Tree', 'Deku Tree Compass Room Side Chest': 'Deku Tree', 'Deku Tree Basement Chest': 'Deku Tree', 'Chest Above King Dodongo': "Dodongo's Cavern", 'Dodongos Cavern Map Chest': "Dodongo's Cavern", 'Dodongos Cavern Compass Chest': "Dodongo's Cavern", 'Dodongos Cavern Bomb Flower Platform': "Dodongo's Cavern", 'Dodongos Cavern Bomb Bag Chest': "Dodongo's Cavern", 'Dodongos Cavern End of Bridge Chest': "Dodongo's Cavern", 'Boomerang Chest': "Jabu Jabu's Belly", 'Jabu Jabus Belly Map Chest': "Jabu Jabu's Belly", 'Jabu Jabus Belly Compass Chest': "Jabu Jabu's Belly", 'Forest Temple First Chest': 'Forest Temple', 'Forest Temple Chest Behind Lobby': 'Forest Temple', 'Forest Temple Well Chest': 'Forest Temple', 'Forest Temple Map Chest': 'Forest Temple', 'Forest Temple Outside Hookshot Chest': 'Forest Temple', 'Forest Temple Falling Room Chest': 'Forest Temple', 'Forest Temple Block Push Chest': 'Forest Temple', 'Forest Temple Boss Key Chest': 'Forest Temple', 'Forest Temple Floormaster Chest': 'Forest Temple', 'Forest Temple Bow Chest': 'Forest Temple', 'Forest Temple Red Poe Chest': 'Forest Temple', 'Forest Temple Blue Poe Chest': 'Forest Temple', 'Forest Temple Near Boss Chest': 'Forest Temple', 'Fire Temple Chest Near Boss': 'Fire Temple', 'Fire Temple Fire Dancer Chest': 'Fire Temple', 'Fire Temple Boss Key Chest': 'Fire Temple', 'Fire Temple Big Lava Room Bombable Chest': 'Fire Temple', 'Fire Temple Big Lava Room Open Chest': 'Fire Temple', 'Fire Temple Boulder Maze Lower Chest': 'Fire Temple', 'Fire Temple Boulder Maze Upper Chest': 'Fire Temple', 'Fire Temple Boulder Maze Side Room': 'Fire Temple', 'Fire Temple Boulder Maze Bombable Pit': 'Fire Temple', 'Fire Temple Scarecrow Chest': 'Fire Temple', 'Fire Temple Map Chest': 'Fire Temple', 'Fire Temple Compass Chest': 'Fire Temple', 'Fire Temple Highest Goron Chest': 'Fire Temple', 'Fire Temple Megaton Hammer Chest': 'Fire Temple', 'Water Temple Map Chest': 'Water Temple', 'Water Temple Compass Chest': 'Water Temple', 'Water Temple Torches Chest': 'Water Temple', 'Water Temple Dragon Chest': 'Water Temple', 'Water Temple Central Bow Target Chest': 'Water Temple', 'Water Temple Central Pillar Chest': 'Water Temple', 'Water Temple Cracked Wall Chest': 'Water Temple', 'Water Temple Boss Key Chest': 'Water Temple', 'Water Temple Dark Link Chest': 'Water Temple', 'Water Temple River Chest': 'Water Temple', 'Silver Gauntlets Chest': 'Spirit Temple', 'Mirror Shield Chest': 'Spirit Temple', 'Spirit Temple Child Left Chest': 'Spirit Temple', 'Spirit Temple Child Right Chest': 'Spirit Temple', 'Spirit Temple Compass Chest': 'Spirit Temple', 'Spirit Temple Early Adult Right Chest': 'Spirit Temple', 'Spirit Temple First Mirror Right Chest': 'Spirit Temple', 'Spirit Temple First Mirror Left Chest': 'Spirit Temple', 'Spirit Temple Map Chest': 'Spirit Temple', 'Spirit Temple Child Climb East Chest': 'Spirit Temple', 'Spirit Temple Child Climb North Chest': 'Spirit Temple', 'Spirit Temple Sun Block Room Chest': 'Spirit Temple', 'Spirit Temple Statue Hand Chest': 'Spirit Temple', 'Spirit Temple NE Main Room Chest': 'Spirit Temple', 'Spirit Temple Near Four Armos Chest': 'Spirit Temple', 'Spirit Temple Hallway Left Invisible Chest': 'Spirit Temple', 'Spirit Temple Hallway Right Invisible Chest': 'Spirit Temple', 'Spirit Temple Boss Key Chest': 'Spirit Temple', 'Spirit Temple Topmost Chest': 'Spirit Temple', 'Shadow Temple Map Chest': 'Shadow Temple', 'Shadow Temple Hover Boots Chest': 'Shadow Temple', 'Shadow Temple Compass Chest': 'Shadow Temple', 'Shadow Temple Early Silver Rupee Chest': 'Shadow Temple', 'Shadow Temple Invisible Blades Visible Chest': 'Shadow Temple', 'Shadow Temple Invisible Blades Invisible Chest': 'Shadow Temple', 'Shadow Temple Falling Spikes Lower Chest': 'Shadow Temple', 'Shadow Temple Falling Spikes Upper Chest': 'Shadow Temple', 'Shadow Temple Falling Spikes Switch Chest': 'Shadow Temple', 'Shadow Temple Invisible Spikes Chest': 'Shadow Temple', 'Shadow Temple Wind Hint Chest': 'Shadow Temple', 'Shadow Temple After Wind Enemy Chest': 'Shadow Temple', 'Shadow Temple After Wind Hidden Chest': 'Shadow Temple', 'Shadow Temple Spike Walls Left Chest': 'Shadow Temple', 'Shadow Temple Boss Key Chest': 'Shadow Temple', 'Shadow Temple Hidden Floormaster Chest': 'Shadow Temple', 'Shadow Temple Freestanding Key': 'Shadow Temple', 'Bottom of the Well Front Left Hidden Wall': 'Bottom of the Well', 'Bottom of the Well Front Center Bombable': 'Bottom of the Well', 'Bottom of the Well Right Bottom Hidden Wall': 'Bottom of the Well', 'Bottom of the Well Center Large Chest': 'Bottom of the Well', 'Bottom of the Well Center Small Chest': 'Bottom of the Well', 'Bottom of the Well Back Left Bombable': 'Bottom of the Well', 'Bottom of the Well Defeat Boss': 'Bottom of the Well', 'Bottom of the Well Invisible Chest': 'Bottom of the Well', 'Bottom of the Well Underwater Front Chest': 'Bottom of the Well', 'Bottom of the Well Underwater Left Chest': 'Bottom of the Well', 'Bottom of the Well Basement Chest': 'Bottom of the Well', 'Bottom of the Well Locked Pits': 'Bottom of the Well', 'Bottom of the Well Behind Right Grate': 'Bottom of the Well', 'Bottom of the Well Freestanding Key': 'Bottom of the Well', 'Ice Cavern Map Chest': 'Ice Cavern', 'Ice Cavern Compass Chest': 'Ice Cavern', 'Ice Cavern Iron Boots Chest': 'Ice Cavern', 'Ice Cavern Freestanding PoH': 'Ice Cavern', 'Gerudo Training Grounds Lobby Left Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Lobby Right Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Stalfos Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Beamos Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Hidden Ceiling Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Maze Path First Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Maze Path Second Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Maze Path Third Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Maze Path Final Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Maze Right Central Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Maze Right Side Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Underwater Silver Rupee Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Hammer Room Clear Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Hammer Room Switch Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Eye Statue Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Near Scarecrow Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Before Heavy Block Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Heavy Block First Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Heavy Block Second Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Heavy Block Third Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Heavy Block Fourth Chest': 'Gerudo Training Grounds', 'Gerudo Training Grounds Freestanding Key': 'Gerudo Training Grounds', 'Ganons Tower Boss Key Chest': "Ganon's Castle", 'Ganons Castle Forest Trial Chest': "Ganon's Castle", 'Ganons Castle Water Trial Left Chest': "Ganon's Castle", 'Ganons Castle Water Trial Right Chest': "Ganon's Castle", 'Ganons Castle Shadow Trial First Chest': "Ganon's Castle", 'Ganons Castle Shadow Trial Second Chest': "Ganon's Castle", 'Ganons Castle Spirit Trial First Chest': "Ganon's Castle", 'Ganons Castle Spirit Trial Second Chest': "Ganon's Castle", 'Ganons Castle Light Trial First Left Chest': "Ganon's Castle", 'Ganons Castle Light Trial Second Left Chest': "Ganon's Castle", 'Ganons Castle Light Trial Third Left Chest': "Ganon's Castle", 'Ganons Castle Light Trial First Right Chest': "Ganon's Castle", 'Ganons Castle Light Trial Second Right Chest': "Ganon's Castle", 'Ganons Castle Light Trial Third Right Chest': "Ganon's Castle", 'Ganons Castle Light Trial Invisible Enemies Chest': "Ganon's Castle", 'Ganons Castle Light Trial Lullaby Chest': "Ganon's Castle", 'Queen Gohma Heart': 'Deku Tree', 'King Dodongo Heart': "Dodongo's Cavern", 'Barinade Heart': "Jabu Jabu's Belly", 'Phantom Ganon Heart': 'Forest Temple', 'Volvagia Heart': 'Fire Temple', 'Morpha Heart': 'Water Temple', 'Twinrova Heart': 'Spirit Temple', 'Bongo Bongo Heart': 'Shadow Temple', 'HF Grotto Deku Scrub Piece of Heart': 'Hyrule Field', 'LW Deku Scrub Deku Stick Upgrade': 'the Lost Woods', 'LW Grotto Deku Scrub Deku Nut Upgrade': 'the Lost Woods'};

# List of major areas in the game
areas = ['Sacred Forest Meadow', 'Hyrule Field', 'Desert Colossus', 'Temple of Time', 'Hyrule Castle', 'Kakariko Village', 'the Graveyard', 'Death Mountain Crater', 'Lon Lon Ranch', 'Ice Cavern', 'Kokiri Forest', 'the Lost Woods', 'Lake Hylia', 'Gerudo Valley', "Gerudo's Fortress", 'Haunted Wasteland', "outside Ganon's Castle", 'the Market', 'Death Mountain Trail', 'Goron City', "Zora's River", "Zora's Domain", "Zora's Fountain", "Ganon's Castle", 'Deku Tree', "Dodongo's Cavern", "Jabu Jabu's Belly", 'Forest Temple', 'Bottom of the Well', 'Fire Temple', 'Water Temple', 'Shadow Temple', 'Gerudo Training Grounds', 'Spirit Temple'];

# List of items to show in the CSV, in the desired display order
items = ["Forest Medallion", "Water Medallion", "Zora Sapphire", "Spirit Medallion", "Light Medallion", "Fire Medallion", "Goron Ruby", "Kokiri Emerald", "Shadow Medallion", "Serenade of Water", "Song of Time", "Song of Storms", "Prelude of Light", "Zeldas Lullaby", "Eponas Song", "Suns Song", "Sarias Song", "Minuet of Forest", "Requiem of Spirit", "Nocturne of Shadow", "Bolero of Fire", "Piece of Heart", "Bow", "Rupees (200)", "Hylian Shield", "Bombs (5)", "Recovery Heart", "Bombs (10)", "Heart Container", "Progressive Wallet", "Bombs (20)", "Progressive Scale", "Bombchus (10)", "Bottle with Poe", "Arrows (10)", "Arrows (30)", "Rupees (5)", "Magic Meter", "Ice Trap", "Rupees (20)", "Rupee (1)", "Deku Stick (1)", "Bottle with Fish", "Bottle with Letter", "Deku Shield", "Deku Nut Capacity", "Progressive Strength Upgrade", "Arrows (5)", "Nayrus Love", "Bomb Bag", "Rupees (50)", "Boomerang", "Kokiri Sword", "Goron Tunic", "Zora Tunic", "Piece of Heart (Treasure Chest Game)", "Claim Check", "Deku Nuts (10)", "Slingshot", "Biggoron Sword", "Deku Stick Capacity", "Progressive Hookshot", "Boss Key (Forest Temple)", "Small Key (Forest Temple)", "Iron Boots", "Ice Arrows", "Small Key (Bottom of the Well)", "Small Key (Fire Temple)", "Boss Key (Fire Temple)", "Stone of Agony", "Small Key (Water Temple)", "Mirror Shield", "Boss Key (Water Temple)", "Small Key (Shadow Temple)", "Hammer", "Bombchus (20)", "Deku Nuts (5)", "Boss Key (Shadow Temple)", "Light Arrows", "Hover Boots", "Fire Arrows", "Small Key (Gerudo Training Grounds)", "Farores Wind", "Lens of Truth", "Small Key (Spirit Temple)", "Dins Fire", "Boss Key (Spirit Temple)", "Bottle with Blue Fire", "Boss Key (Ganons Castle)", "Bombchus (5)", "Small Key (Ganons Castle)", "Double Defense", "Buy Deku Shield", "Zeldas Letter", "Time Travel", "Ocarina", "Buy Deku Stick (1)", "Buy Goron Tunic", "Small Key (Gerudo Fortress)", "Gerudo Membership Card", "Deliver Letter", "Fish", "Triforce", "Bottle", "Deku Seeds (30)", "Bottle with Bugs", "Bottle with Milk", "Eyeball Frog", "Bottle with Fairy", "Gold Skulltula Token", "Scarecrow Song", "Buy Blue Fire", "Bottle with Big Poe", "Sell Big Poe", "Bottle with Green Potion", "Blue Fire", "Bottle with Blue Potion", "Eyedrops", "Magic Bean", "Prescription", "Bottle with Red Potion", "Bugs", "Buy Zora Tunic", "Big Poe", "Buy Bombchu (10)", "Buy Deku Nut (5)", "Buy Bombchu (20)"];

############################################
# Dicts to populate with data from the logs.
# The values are generally seed count.
############################################
sphereCount = {};
locationsPlaythrough = {};
locationsKeyless = {};
locationsWotH = {};
itemsPlaythrough = {};
itemsWotH = {};
locationsToItems = {};
areaBarren = {};
areaWotH = {};

#############################################
# Reads in each file based on the user-set
# constants and adds their data to the dicts.
#
# Output: the number of files read.
#############################################
def loadFiles():
    totalRead = 0;
    for ii in range(0, numOfLogs):
        with open(inputFolder + "/" + inputFileStart + str(ii) + inputFileEnd) as f:
            data = json.load(f);
            analyze(data);
            totalRead = totalRead + 1;
    return totalRead;

#############################################
# Calls various functions to analyze aspects
# of the spoiler log in question.
#
# Input: data, a dict generated from the json
#        file in the spoiler log.
#############################################
def analyze(data):
    getSphereCount(data);
    getPlaythrough(data);
    getWotH(data);
    getLocationToItems(data);
    getBarrenAreas(data);

#############################################
# Determines the number of spheres in this
# seed, then adds this seed to the dict
# mapping sphere count to number of seeds
# with that count.
#
# Input: data, a dict generated from the json
#        file in the spoiler log.
#############################################
def getSphereCount(data):
    spheres = len(data[":playthrough"]);
    incrementDict(sphereCount, spheres);

#############################################
# Determines the items listed in the
# playthrough, then addes them to the
# corresponding dicts for analysis.
#
# Input: data, a dict generated from the json
#        file in the spoiler log.
#############################################
def getPlaythrough(data):
    for sphere in data[":playthrough"].keys():
        for location in data[":playthrough"][sphere].keys():
            incrementDict(locationsPlaythrough, location);

            item = data[":playthrough"][sphere][location];
            # Certain items, like scrub purchases, include price
            # and so are a dict.  We want only the name.
            if isinstance(item, dict):
                item = item["item"];
            incrementDict(itemsPlaythrough, item);

            if item.find("Small Key") == -1 and item.find("Boss Key") == -1:
                incrementDict(locationsKeyless, location);

#############################################
# Determines the WotH locations, items, and
# areas, then adds them to the corresponding
# dicts for analysis
#
# Input: data, a dict generated from the json
#        file in the spoiler log.
#############################################
def getWotH(data):
    wothAreas = set();
    for location in data[":woth_locations"].keys():
        incrementDict(locationsWotH, location);

        item = data[":woth_locations"][location];
        # Certain items, like scrub purchases, include price
        # and so are a dict.  We want only the name.
        if isinstance(item, dict):
            item = item["item"];
        incrementDict(itemsWotH, item);

        if location in locationMap.keys():
            area = locationMap[location];
            wothAreas.add(area);
    for area in wothAreas:
        incrementDict(areaWotH, area);

#############################################
# Determines which item is in each location
# and adds this to a dict for analysis
#
# Input: data, a dict generated from the json
#        file in the spoiler log.
#############################################
def getLocationToItems(data):
    for location in data["locations"].keys():
        item = data["locations"][location];
        # Certain items, like scrub purchases, include price
        # and so are a dict.  We want only the name.
        if isinstance(item, dict):
            item = item["item"];
        if location in locationsToItems.keys():
            incrementDict(locationsToItems[location], item);
        else:
            locationsToItems[location] = {item : 1};

#############################################
# Gets the list of barren areas in this seed,
# then adds this to the dict mapping area to
# number of times barren.
#
# Input: data, a dict generated from the json
#        file in the spoiler log.
#############################################
def getBarrenAreas(data):
    for area in data[":barren_regions"]:
        incrementDict(areaBarren, area);

#############################################
# Process the results gathered earlier and
# format them as .csv files.
#
# Input: numRead, the number of files
#        successfully read.
#############################################
def writeResults(numRead):
    writeItemSheet(numRead);
    writeSphereSheet(numRead);
    writeWotHSheet(numRead);

#############################################
# Write a CSV file showing how often each
# item and check are required, including
# the frequency each item is at each location
#
# Input: numRead, the number of files
#        successfully read.
#############################################
def writeItemSheet(numRead):
    with open(itemCSV, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',');

        headerRow1 = ["","","","Items:"];
        headerRow2 = ["","","","Play%:"];
        headerRow3 = ["Locations:", "Play%:", "NoKeys%:", "WotH%:"];
        for item in items:
            headerRow1.append(item);
            headerRow2.append(getDictValueSafe(itemsPlaythrough, item) / numRead);
            headerRow3.append(getDictValueSafe(itemsWotH, item) / numRead);
        csvWriter.writerow(headerRow1);
        csvWriter.writerow(headerRow2);
        csvWriter.writerow(headerRow3);

        for location in locations:
            locationRow = [location];
            locationRow.append(getDictValueSafe(locationsPlaythrough, location) / numRead);
            locationRow.append(getDictValueSafe(locationsKeyless, location) / numRead);
            locationRow.append(getDictValueSafe(locationsWotH, location) / numRead);

            for item in items:
                if not (location in locationsToItems.keys()):
                    locationRow.append(0);
                else:
                    locationRow.append(getDictValueSafe(locationsToItems[location], item) / numRead);
            csvWriter.writerow(locationRow);

#############################################
# Write a CSV file showing the number of
# seeds with a given number of spheres
#
# Input: numRead, the number of files
#        successfully read.
#############################################
def writeSphereSheet(numRead):
    with open(sphereCSV, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',');

        headerRow = ["Number of Spheres:"];
        secondRow = [""];
        thirdRow = [""];
        sphereList = sorted(list(sphereCount.keys()));
        for ii in range(sphereList[0], sphereList[len(sphereList) - 1] + 1):
            headerRow.append(ii);
            sphereCountValue = getDictValueSafe(sphereCount, ii);
            secondRow.append(sphereCountValue);
            thirdRow.append(sphereCountValue / numRead);
        csvWriter.writerow(headerRow);
        csvWriter.writerow(secondRow);
        csvWriter.writerow(thirdRow);

#############################################
# Write a CSV file showing how often each
# area is WotH and barren
#
# Input: numRead, the number of files
#        successfully read.
#############################################
def writeWotHSheet(numRead):
    with open(barrenCSV, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',');

        headerRow = [""];
        secondRow = ["WotH%:"];
        thirdRow = ["Barren%:"];
        for area in areas:
            headerRow.append(area);
            secondRow.append(getDictValueSafe(areaWotH, area) / numRead);
            thirdRow.append(getDictValueSafe(areaBarren, area) / numRead);
        csvWriter.writerow(headerRow);
        csvWriter.writerow(secondRow);
        csvWriter.writerow(thirdRow);

#############################################
# Increments the value associated with a key
# in a dict by 1.  Sets the value to 1 if
# the key is not in the dict.
#
# Input: dict, the dict to modify
#        key, the key whose value we increase
#############################################
def incrementDict(dict, key):
    if key in dict.keys():
        dict[key] = dict[key] + 1;
    else:
        dict[key] = 1;

#############################################
# Returns the value associated with key in
# dict, or 0 if the key is not found.
#
# Input: dict, the dict to read from
#        key, the key whose value we want
#############################################
def getDictValueSafe(dict, key):
    if not(key in dict.keys()):
        return 0;
    return dict[key];

#############################################
# Runs the program after setting up
# dicts for storing cumulative data
#############################################
def main():
    filesRead = loadFiles();
    writeResults(filesRead);

if __name__ == "__main__":
    main();
