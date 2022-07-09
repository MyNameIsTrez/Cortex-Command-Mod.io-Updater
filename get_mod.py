import modio

with open("api_key.txt") as api_key_file, open("oauth2.txt") as oauth2_file:
	client = modio.Client(api_key=api_key_file.read(), auth=oauth2_file.read())

game = client.get_game(508)
print(game.name)

mod = game.get_mod(2175523)
print(mod.get_file())
