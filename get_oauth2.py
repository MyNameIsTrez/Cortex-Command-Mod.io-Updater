import modio

with open("api_key.txt") as f:
	client = modio.Client(api_key=f.read().rstrip("\n"))
	print(client)

with open("email.txt") as f:
	client.email_request(f.read().rstrip("\n"))

#check your email for the security code
code = input("Code: ")

oauth2 = client.email_exchange(code)

with open("oauth2.txt", "w") as f:
	f.write(oauth2)
