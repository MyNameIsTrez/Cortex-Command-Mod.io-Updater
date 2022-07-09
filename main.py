import json, requests, time


def main():
	game_id = 508
	api_key = "ab779d10d97eadfb36b43c27ec6292a3"

	headers = {
		'Accept': 'application/json'
	}

	step = 100
	offset = 0
	while True:
		r = requests.get(f'https://api.mod.io/v1/games/{game_id}/mods?_limit={step}&_offset={offset}', params={
			'api_key': api_key
		}, headers = headers)

		x = r.json()
		# print(len(x["data"]))

		for mod in x["data"]:
			if is_pre3(mod):
				url = mod["modfile"]["download"]["binary_url"]
				mod_file = requests.get(url)
				with open(f"downloads/{mod['name']}.zip", "wb") as f:
					f.write(mod_file.content)

		offset += step

		if x["result_count"] < step:
			break

		time.sleep(5)


	# with open("response.json", "w") as f:
	# 	x = r.json()
	# 	print(len(x["data"]))
	# 	json.dump(x, f)


def is_pre3(mod):
	return any(tag["name"] == "Pre-Release 3.0" for tag in mod["tags"])


if __name__ == "__main__":
	main()
