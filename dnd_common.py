import os.path
import json
import time
import requests

###################################################################
# dnd-common.py                                                   #
#-----------------------------------------------------------------#
# This is a common file that contains functions shared between    #
# all of the D&D 5e scripts.                                      #
###################################################################


def getSpellData():
	script_dir = os.path.dirname(os.path.realpath(__file__))
	spell_file_location = os.path.join(script_dir,"spells.json")

	if os.path.exists(spell_file_location):
		spell_data = json.load( open(spell_file_location,"r") )

		if spell_data["countDownloaded"] != spell_data["count"]:
			print("Incomplete Local Spell Data Found! Initiating Database Build...")
			createLocalSpellData()
		else:
			return spell_data
	else:
		print("No Local Spell Data Found! Initiating Database Build...")
		createLocalSpellData()

	spell_data = json.load( open(spell_file_location,"r") )
	return spell_data


def createLocalSpellData():
	"""
		Used to interact with the D&D 5e API and download all 
		spells within their database to build a local JSON file
		of all spells. Also resumes the download from the point
		it left off if the process gets interrupted for any
		reason.

		Returns True if it successfully creates the file
	"""
	base_url = "https://www.dnd5eapi.co/api/spells/"
	script_dir = os.path.dirname(os.path.realpath(__file__))
	spell_file_location = os.path.join(script_dir,"spells.json")

	URL_READ_DELAY = 3

	payload = {}
	headers = {
		"Accept":"application/json"
	}

	data = None

	if os.path.exists(spell_file_location):
		response = json.load( open(spell_file_location,"r") )

		# If this is true, all spell data is already downloaded
		# so we shouldn't bother doing it again
		if response["countDownloaded"] == response["count"]:
			return True

		data = response
	else:
		response = requests.request("GET",base_url,headers=headers,data=payload)
			
		if response.status_code != 200:
			# Network request failed; assume that there has
			# been catastrophic failure and end program early.
			# User can always restart download where they left off
			response.raise_for_status()
			return False

		data = response.json()
		time.sleep(URL_READ_DELAY)


	for i,item in enumerate(data["results"]):
		curURL = base_url + item['index']

		if "desc" in item and \
			"range" in item and \
			"duration" in item and \
		  	"concentration" in item and \
		  	"casting_time" in item and \
		  	"classes" in item:
			print(f"Spell {i+1} of {data['count']} already downloaded; skipping")
		else:
			resp = requests.request("GET",curURL,headers=headers,data=payload)

			if resp.status_code != 200:
				# Network request failed; assume that there has
				# been catastrophic failure and end program early.
				# User can always restart download where they left off
				resp.raise_for_status()
				return False

			curData = resp.json()

			item["desc"] = curData["desc"]
			item["range"] = curData["range"]
			item["duration"] = curData["duration"]
			item["concentration"] = curData["concentration"]
			item["casting_time"] = curData["casting_time"]

			curClasses = []
			for dndClass in curData["classes"]:
				curClasses.append(dndClass["name"])

			item["classes"] = curClasses
			data["countDownloaded"] = i+1

			with open(spell_file_location,"w") as spellFile:
				spellFile.write(json.dumps(data))

			print(f"Downloaded spell {i+1} of {data['count']}")
			time.sleep(URL_READ_DELAY)

	return True


def outputSpell(curSpell):
	"""
		When given a spell array within curSpell, this
		function simply outputs the spell through print
		statements. No returns.
	"""
	concentrationStr = "";

	if curSpell["concentration"]:
		concentrationStr = " (C)"

	titleString = f"* {curSpell['name']}{concentrationStr} *"

	print("*"*len(titleString))
	print(titleString)
	print("*"*len(titleString))

	print(f"Level {curSpell['level']}")
	print(f"Range: {curSpell['range']}")
	print(f"Duration: {curSpell['duration']}")
	print(f"Casting Time: {curSpell['casting_time']}")
	print(f"Classes: {', '.join(curSpell['classes'])}")
	print(f"---------------------------")

	for line in curSpell["desc"]:
		print(f"{line}\n")


if __name__ == "__main__":
	print(createLocalSpellData())