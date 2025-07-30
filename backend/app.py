from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import shutil
import os
import tempfile

from tools.agent_tool import find_anuschka_bag_for_style

app = FastAPI(title="Persona Matcher AI Backend", version="1.0.0")

# Allow local Vite dev server and any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, be restrictive
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    input_text: str


@app.get("/")
async def root():
    return {"message": "Persona Matcher AI Backend is running"}


@app.post("/recommend/text")
async def recommend_from_text(payload: TextRequest):
    """Return bag recommendations given a natural-language style description."""
    try:
        products = find_anuschka_bag_for_style.invoke(payload.input_text)
        return {"recommendations": products}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/recommend/image")
async def recommend_from_image(file: UploadFile = File(...)):
    """Return bag recommendations based on an uploaded image.

    NOTE: The current implementation simply forwards the temporary file path
    to the existing recommendation tool, which primarily expects a text
    description. You can later swap this out for a vision-enabled model.
    """
    # Save the uploaded image to a temporary file
    try:
        suffix = os.path.splitext(file.filename)[1] or ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        products = find_anuschka_bag_for_style.invoke(tmp_path)
        return {"recommendations": products}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
