from PIL import Image
import pytesseract as OCR
import api_key
from openai import OpenAI as AI

receipts = ['image.jpg']
amounts = []
merchants = []

OCR.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"

client = AI(api_key = api_key.key)

for receipt in receipts:
	text = OCR.image_to_string(receipt)
	print(text)

	req = client.chat.completions.create(
		model="gpt-3.5.turbo",
		messages = [{
			"role": "user",
			"content": f"parse the following receipt as JSON data: {text}",
		}]
	)

	print(req.choices[0].message.content)
