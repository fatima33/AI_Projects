from google import genai
from google.genai import types
import asyncio
from pyppeteer import launch

from config import GEMINI_API_KEY


async def scrape_reviews(url):
	reviews = []
	browser = await launch({"headless":True, "args":["--window-size=800,3200"]})
	page = await browser.newPage()
	await page.setViewport({"width":800,"height":3200})
	await page.goto(url)
	await page.waitForSelector('.jJc9Ad')
	elements = await page.querySelectorAll('.jJc9Ad')

	for element in elements:
		try:
			await page.waitForSelector('.w8nwRe')
			more_btn = await element.querySelector('.w8nwRe')
			await page.evaluate('button => button.click()',more_btn)
			await page.waitFor(5000)
			await page.waitForSelector('.MyEned')
		except:
			pass

		snippet = await element.querySelector('.MyEned')
		if snippet:
			text = await page.evaluate('selected => selected.textContent', snippet)
			reviews.append(text.strip())
		else:
			print("No review found in this element")

	await browser.close()

	return reviews

def summarize(reviews):
	prompt = "I collected some reviews of a place I was considering visiting. Can you summarize the reviews concise in two lines for me?"
	for review in reviews:
		prompt += "\n"+review

	client = genai.Client(api_key=GEMINI_API_KEY)

	response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    ),
)
	print(response.text)

url = input("Enter a url: ")

reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))

summarize(reviews)