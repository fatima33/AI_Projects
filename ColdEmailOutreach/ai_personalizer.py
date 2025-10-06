import google.generativeai as genai

genai.configure(api_key="xyz")

def generate_email(company_name, contact_name):
	model = genai.GenerativeModel("gemini-1.5-flash")
	prompt = f"""
	Write a short, professional cold email to {contact_name} at {company_name}.
	Offer a free demo of our solution to improve their workflow efficiency.
	Keep under 120 words, warm but businesslike.
	"""
	response = model.generate_content(prompt)
	return response.text
