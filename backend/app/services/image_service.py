from PIL import Image, ImageEnhance
import os
from pathlib import Path
import uuid
import logging
import aiofiles
from fastapi import UploadFile
import tempfile
import io

logging.basicConfig(level=logging.INFO)
UPLOAD_FOLDER = "uploads"

async def save_image(image_file: UploadFile, filename: str):
    """Save original image and create a thumbnail with versioning."""
    version_id = str(uuid.uuid4())[:8]  # Generate a short unique version ID
    new_filename = f"{filename}-{version_id}"
    image_dir = Path(UPLOAD_FOLDER) / new_filename / version_id
    os.makedirs(image_dir, exist_ok=True)

    # Save original
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    async with aiofiles.open(temp_file.name, 'wb') as out_file:
        content = await image_file.read()
        await out_file.write(content)

    image = Image.open(temp_file.name)
    original_path = image_dir / f"{new_filename}.jpeg"
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.save(original_path, format="JPEG")

    # Save thumbnail
    thumbnail_path = image_dir / f"{filename}_thumbnail-{version_id}.jpeg"
    image.thumbnail((150, 150))
    image.save(thumbnail_path, format="JPEG")

    os.remove(temp_file.name)  # Clean up the temporary file

    return str(original_path), str(thumbnail_path), version_id, new_filename

async def apply_transformation(image_path: str, transformation: str):
    """Applies transformations like rotate, flip, resize, etc."""
    async with aiofiles.open(image_path, 'rb') as file:
        content = await file.read()
        with Image.open(io.BytesIO(content)) as img:
            version_id = str(uuid.uuid4())[:8]
            output_dir = Path(image_path).parent.parent
            new_image_dir = output_dir / version_id
            new_image_path = new_image_dir / f"{version_id}.jpeg"
            thumbnail_path = new_image_dir / f"thumbnail-{version_id}.jpeg"

            # Create the directory if it does not exist
            os.makedirs(new_image_dir, exist_ok=True)

            if transformation == "rotate":
                img = img.rotate(90)
            elif transformation == "flip":
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif transformation == "grayscale":
                img = img.convert("L")
            elif transformation == "brightness":
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.5)  # Increase brightness

            img.save(new_image_path, format="JPEG")

            # Create a thumbnail
            img.thumbnail((150, 150))
            img.save(thumbnail_path, format="JPEG")

    return str(new_image_path), str(thumbnail_path), version_id



