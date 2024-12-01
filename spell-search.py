import sys
import os.path
import json
from dnd_common import createLocalSpellData, outputSpell

###################################################################
# spell-search.py                                                 #
#-----------------------------------------------------------------#
# This script is designed to search for a certain spell from the  #
# full list of D&D 5e spells, based on the complete list scraped  #
# from the D&D 5e API.                                            #
###################################################################

def searchSpell(spellData,searchString):
	for spell in spellData["results"]:
		if searchString in spell["name"].lower():
			outputSpell(spell)

def main():
	if os.path.exists("spells.json"):
		spell_data = json.load( open("spells.json","r") )

		if spell_data["countDownloaded"] != spell_data["count"]:
			print("Incomplete Local Spell Data Found! Initiating Database Build...")
			createLocalSpellData()
		else:
			searchSpell(spell_data, ' '.join(sys.argv[1:]).lower())
	else:
		print("No Local Spell Data Found! Initiating Database Build...")
		createLocalSpellData()


if __name__ == "__main__":
	main()