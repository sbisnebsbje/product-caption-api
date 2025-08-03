from fastapi import FastAPI, File, UploadFile
import requests

app = FastAPI()

HUGGINGFACE_API_TOKEN = "hf_your_token"  # This will be overridden by Render env var

@app.post("/caption")
async def get_caption(file: UploadFile = File(...)):
    image_bytes = await file.read()

    response = requests.post(
        "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
        headers={
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/octet-stream"
        },
        data=image_bytes
    )

    if response.status_code == 200:
        result = response.json()
        return {"caption": result[0]["generated_text"]}
    else:
        return {"error": "Captioning failed"}
