import os.path
import random
import time
import json
from dnd_common import createLocalSpellData, outputSpell

###################################################################
# random-scroll.py                                                #
#-----------------------------------------------------------------#
# This script is designed to give the user a random d&d magic     #
# scroll, based on spells scraped from the D&D 5e API             #
###################################################################

def randomScroll(spell_data,max_lvl=None,dndClass=None):
	fullClassList = [
						"Barbarian","Bard","Cleric","Druid",
						"Fighter","Monk","Paladin","Ranger",
						"Rogue","Sorcerer","Warlock","Wizard"
					]

	if max_lvl is not None and (max_lvl < 0 or max_lvl > 9):
		return False

	if dndClass is not None and dndClass not in fullClassList:
		return False

	all_spells = spell_data["results"]

	choiceInsuficient = True
	curSpell = None

	while choiceInsuficient:
		curSpell = random.choice(all_spells)

		if curSpell['level'] > 0 and \
		 (max_lvl is None or curSpell['level'] <= max_lvl) and \
		 (dndClass is None or dndClass in curSpell['classes']):
			choiceInsuficient = False

	outputSpell(curSpell)
	

def main():
	if os.path.exists("spells.json"):
		spell_data = json.load( open("spells.json","r") )

		if spell_data["countDownloaded"] != spell_data["count"]:
			print("Incomplete Local Spell Data Found! Initiating Database Build...")
			createLocalSpellData()
		else:
			randomScroll(spell_data,3,"Cleric")
	else:
		print("No Local Spell Data Found! Initiating Database Build...")
		createLocalSpellData()



if __name__ == "__main__":
	main()