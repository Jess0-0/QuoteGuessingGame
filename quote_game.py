# http://quotes.toscrape.com/

import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

all_quotes = []
base_url = "http://quotes.toscrape.com/"
url = "/page/1"


def scrape_quotes(all_quotes, base_url, url):

	while url:

		res = requests.get(f"{base_url}{url}")
		soup = BeautifulSoup(res.text, "html.parser")
		quotes = soup.find_all(class_ = "quote")

		for quote in quotes:
			all_quotes.append({
				"text": quote.find(class_ = "text").get_text(),
				"author": quote.find(class_ = "author").get_text(),
				"bio-link": quote.find("a")['href']
			})

		next_btn = soup.find(class_ = "next")
		url = next_btn.find("a")["href"] if next_btn else None
		sleep(0.1)

def ask_again(base_url, url):
	again = input(f"Would you like to play again (y|n)? ")

	while again.lower() not in ('y', 'yes', 'n', 'no'):
		again = input(f"Would you like to play again (y|n)? ")
	
	if again.lower() in ('y', 'yes'):
		print("Okay! Play again!")
		return start_game(base_url, url)
	else:
		print("See you!")

def start_game(base_url, url):

	quote = choice(all_quotes)
	print("Here is a quote: ")
	print(quote["text"])
	print(quote["author"])

	remaining_guesses = 4
	guess = ""

	while guess.lower() != quote["author"].lower() and remaining_guesses > 0:

		guess = input(f"Who is the author of this quote? Guesses remaining: {remaining_guesses} \nYour answer: ")
		remaining_guesses -= 1

		if guess.lower() == quote["author"].lower():
			print("Yay! You got it right :)")
			ask_again(base_url, url)
			break

		if remaining_guesses == 3:

			res = requests.get(f"{base_url}{quote['bio-link']}")
			soup = BeautifulSoup(res.text, "html.parser")
			birth_date = soup.find(class_ = "author-born-date").get_text()
			birth_loc = soup.find(class_ = "author-born-location").get_text()
			print(f"Here's a hint: The author was born on {birth_date} {birth_loc}")

		elif remaining_guesses == 2:
			print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
		elif remaining_guesses == 1:
			print(f"Here's a hint: The author's last name starts with: {quote['author'][quote['author'].rindex(' ') + 1]}")
		else:
			print(f"Sorry you went out of guesses :( The answer is: {quote['author']}")
			ask_again(base_url, url)


scrape_quotes(all_quotes, base_url, url)
start_game(base_url, url)

print("END.")

