import sys
import os.path
import json
# from dnd_common import createLocalSpellData, outputSpell
from dnd_common import getSpellData, outputSpell

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
	spell_data = getSpellData()
	searchSpell(spell_data, ' '.join(sys.argv[1:]).lower())


if __name__ == "__main__":
	main()