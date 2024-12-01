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

	payload = {}
	headers = {
		"Accept":"application/json"
	}

	data = None

	if os.path.exists("spells.json"):
		response = json.load( open("spells.json","r") )

		# If this is true, all spell data is already downloaded
		# so we shouldn't bother doing it again
		if response["countDownloaded"] == response["count"]:
			return True

		data = response
	else:
		response = requests.request("GET",base_url,headers=headers,data=payload)
		data = response.json()
		time.sleep(5)

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

			with open("spells.json","w") as spellFile:
				spellFile.write(json.dumps(data))

			print(f"Downloaded spell {i+1} of {data['count']}")
			time.sleep(5)


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