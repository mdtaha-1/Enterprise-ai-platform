from fastapi import APIRouter
from pydantic import BaseModel
from app.image.generator import generate_image

router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate_image_endpoint(request: ImageRequest):
    """Generate an image from a text prompt"""
    try:
        image_base64, image_path = generate_image(request.prompt)
        return {
            "message": "Image generated successfully",
            "prompt": request.prompt,
            "image_base64": image_base64,
            "saved_to": image_path
        }
    except Exception as e:
        return {"error": str(e)}