import modio


def main():
	with open("api_key.txt") as f:
		client = modio.Client(api_key=f.read().rstrip("\n"))
		print(client)

	with open("email.txt") as f:
		print(f.read().rstrip("\n"))
		client.email_request(f.read().rstrip("\n"))

	# Check your email for the security code
	code = input("Code: ")

	oauth2 = client.email_exchange(code)

	with open("oauth2.txt", "w") as f:
		f.write(oauth2)


if __name__ == "__main__":
	main()
