import random

##########################################################################
# random-magic-item.py                                                   #
#----------------------------------------------------------------------- #
# This script is designed to roll up details for a random magic item     #
# based on the table from "Telecanter's Receding Rules". You can find    #
# said table here:                                                       #
#                                                                        #
# https://recedingrules.blogspot.com/2010/03/spell-like-effect-spur.html #
##########################################################################

def randomMode():
	mode = [ "Wielder","Touch","Distance","Area Effect" ]
	return random.choice(mode)


def randomIntent():
	intent = [
		"Attack","Defense","Utility","Transport",
		"[REROLL TWICE]","[REROLL THRICE]"
	]
	intent_abbreviated = intent[0:4]

	rand_intent = random.choice(intent)

	if rand_intent == "[REROLL TWICE]":
		intent1 = random.choice(intent_abbreviated)
		intent_abbreviated.remove(intent1)
		intent2 = random.choice(intent_abbreviated)

		rand_intent = f"{intent1} / {intent2}"
	elif rand_intent == "[REROLL THRICE]":
		intent1 = random.choice(intent_abbreviated)
		intent_abbreviated.remove(intent1)
		intent2 = random.choice(intent_abbreviated)
		intent_abbreviated.remove(intent2)
		intent3 = random.choice(intent_abbreviated)

		rand_intent = f"{intent1} / {intent2} / {intent3}"

	return rand_intent


def randomRange():
	rangeList = []

	for i in range(10,80,10):
		rangeList.append(f"{i}ft")

	rangeList.append("Sight")

	return random.choice(rangeList)


def randomDuration():
	duration = [
		"Instant","1 round","1-6 rounds","1 turn","1-6 turns",
		"1 hour","1-6 hours","1 day","1-6 days","Permanent"
	]

	return random.choice(duration)


def randomEffect():
	effect = [
		"Alter","Animate","Compel","Conjure","Delude",
		"Dispel/Disappear","Distort","Divine","Evoke",
		"Shield","Summon","Transmute"
	]

	return random.choice(effect)


def randomMedium():
	medium = [
		"Animal", "Vegetable", "Mineral", "Metal", "Fire",
		"Earth", "Water", "Air", "Shadow", "Light",
		"Sound", "Dead", "Infernal", "Time", "Space/Dimension",
		"Human", "Demi-human", "Humanoid", "Monster", "Terrain"
	]

	return random.choice(medium)


def main():
	print(f"Mode:       {randomMode()}")
	print(f"Intent:     {randomIntent()}")
	print(f"Range:      {randomRange()}")
	print(f"Duration:   {randomDuration()}")
	print(f"Effect:     {randomEffect()}")
	print(f"Medium:     {randomMedium()}")


if __name__ == "__main__":
	main()