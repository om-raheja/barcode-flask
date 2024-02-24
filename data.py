from PIL import Image
from openai import OpenAI
import pytesseract as OCR
import os

OCR.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"

client = OpenAI(
	api_key = os.environ.get("OPENAI_API_KEY"),
)

def app():
	# data shit --> where does it come from???
	data = OCR.image_to_string("input.png")
	print(data)

	complete = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages = [
		{
			"role": "user",
			"content": "parse the following data in JSON format: ${data}",
		}
	])

	print(complete.choices[0].message.content)

app()
