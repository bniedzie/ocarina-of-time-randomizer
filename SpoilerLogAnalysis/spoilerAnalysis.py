###############################################################################
# This script reads large numbers of Zelda Ocarina of Time Randomizer
# spoiler logs and produces CSVs analyzing item placement, sphere count,
# and way of the hero location distributions.
#
# Author: Benjamin Niedzielski
# Last Modified: June 14, 2020
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
inputFolder = 'logs';
inputFileStart = 'OoT_17332_H8DC651YD1-';
inputFileEnd = '_Spoiler.json';
numOfLogs = 5;

#Contains files giving all items and locations
worldFolder = 'worldLists';
itemListFile = 'itemListStandard';
locationListFile = 'locationListStandard';
locationMapFile = 'locationMap.json'

############################################
# Output files
############################################
outputFolder = 'sampleResults';
itemCSV = 'items.csv';
sphereCSV = 'sphere.csv';
barrenCSV = 'woth.csv';

############################################
# Constants for the game world.
# Filled from the above file paths.
# These files Can be modified to include
# scrub and shopsanity or for future changes.
############################################

# Locations to show in the CSV.  Results will display in this order
locations = [];
# Dictionary with check as key, and its major location as value, based on LocationList.py
locationMap = {};
# List of major areas in the game
areas = [];
# List of items to show in the CSV, in the desired display order
items = [];

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
# Reads in files containing information
# about each location and item in the game.
#
# Populates appropriate variables for use.
#############################################
def loadWorld():
    #Handle item list
    with open(worldFolder + '\\' + itemListFile) as f:
        #First two lines are comments about versioning
        f.readline();
        f.readline();
        for item in f:
            items.append(item.strip());

    #Handle location list
    with open(worldFolder + '\\' + locationListFile) as f:
        #First two lines are comments about versioning
        f.readline();
        f.readline();
        for location in f:
            locations.append(location.strip());

    #handle map of location to major area
    with open(worldFolder + '\\' + locationMapFile) as f:
        locationMap = json.load(f);
        #Remove versioning information
        if 'Version' in locationMap:
            del locationMap['Version'];
        for area in sorted(set(locationMap.values())):
            areas.append(area);

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
    with open(outputFolder + '/' + itemCSV, 'w', newline='') as csvfile:
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
    with open(outputFolder + '/' + sphereCSV, 'w', newline='') as csvfile:
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
    with open(outputFolder + '/' + barrenCSV, 'w', newline='') as csvfile:
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
    try:
        loadWorld();
        filesRead = loadFiles();
        writeResults(filesRead);
    except:
        print("Please ensure that the file paths you have specified are correct, the input files are of the correct format, and you do not have open any of the output files.");

if __name__ == "__main__":
    main();
