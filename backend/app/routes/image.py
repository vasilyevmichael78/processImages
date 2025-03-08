from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.image import Image, ImageVersion
from app.services.image_service import save_image, apply_transformation
from app.schemas import ImageUploadSchema, ImageResponseSchema, TransformationRequest
import shutil
import logging
#
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_latest_version(db: Session, image_id: int):
    versions = db.query(ImageVersion).filter(ImageVersion.image_id == image_id).order_by(ImageVersion.id.desc()).all()
    latest_version = versions[0] if versions else None
    if not latest_version:
        logging.error(f"Image version not found: {image_id}")
        raise HTTPException(status_code=404, detail="Image version not found")
    return latest_version



def serve_file(file_path: str, media_type: str):
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="File not found")

    def iterfile():
        with open(file_path, mode="rb") as file:
            yield from file

    return StreamingResponse(iterfile(), media_type=media_type)

@router.post("/upload", response_model=ImageResponseSchema)
async def upload_image(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    file: UploadFile = form.get("image")
    if not file:
        logging.error("File is missing in the request")
        raise HTTPException(status_code=400, detail="File is required")
    
    allowed_extensions = {"jpeg", "jpg", "png"}
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        logging.error(f"Invalid file extension: {file_extension}")
        raise HTTPException(status_code=400, detail="Invalid file extension. Only JPEG, JPG, and PNG are allowed.")
    
    logging.info(f"Received file: {file.filename}")
    filename = file.filename.split(".")[0]
    original_path, thumbnail_path, version_id, new_filename = await save_image(file, filename)

    new_image = Image(filename=new_filename, original_path=original_path, thumbnail_path=thumbnail_path)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    new_version = ImageVersion(image_id=new_image.id, version_id=version_id, processed_path=original_path, processed_thumbnail_path=thumbnail_path)
    db.add(new_version)
    db.commit()

    logging.info(f"Image uploaded successfully: {new_image.id}")
    return ImageResponseSchema(id=new_image.id, filename=new_image.filename, original=new_image.original_path, thumbnail=new_image.thumbnail_path)

@router.get("/", response_model=list[ImageResponseSchema])
async def list_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return [ImageResponseSchema(id=img.id, filename=img.filename, original=img.original_path, thumbnail=img.thumbnail_path) for img in images]

@router.get("/{image_id}", response_model=ImageResponseSchema)
async def get_image(image_id: int, db: Session = Depends(get_db)):
    image = get_image_or_404(db, image_id)
    if not image:
        logging.error(f"Image not found: {image_id}")
        raise HTTPException(status_code=404, detail="Image not found")
    return ImageResponseSchema(id=image.id, filename=image.filename, original=image.original_path, thumbnail=image.thumbnail_path)

@router.delete("/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = get_image_or_404(db, image_id)
    image_folder = Path(image.original_path).parent.parent
    try:
        shutil.rmtree(image_folder)
        logging.info(f"Image folder deleted successfully: {image_folder}")
    except Exception as e:
        logging.error(f"Error deleting image folder: {image_folder}, error: {e}")
        raise HTTPException(status_code=500, detail="Error deleting image folder")

    db.query(ImageVersion).filter(ImageVersion.image_id == image.id).delete()
    db.delete(image)
    db.commit()
    
    logging.info(f"Image deleted successfully: {image_id}")
    return {"message": "Image deleted successfully"}

@router.post("/edit/{image_id}", response_model=ImageResponseSchema)
async def edit_image(image_id: int, request: TransformationRequest, db: Session = Depends(get_db)):
    allowed_transformations = {"rotate", "flip", "grayscale", "brightness"}
    if request.transformation not in allowed_transformations:
        logging.error(f"Invalid transformation: {request.transformation}")
        raise HTTPException(status_code=400, detail=f"Invalid transformation. Allowed transformations are: {', '.join(allowed_transformations)}")

    latest_version = get_latest_version(db, image_id)

    new_path, thumbnail_path, version_id = await apply_transformation(latest_version.processed_path, request.transformation)

    new_version = ImageVersion(image_id=image_id, version_id=version_id, processed_path=new_path, processed_thumbnail_path=thumbnail_path)
    db.add(new_version)
    db.commit()

    logging.info(f"Transformation applied: {image_id}, version: {version_id}")
    return ImageResponseSchema(id=image_id, filename=new_version.image.filename, original=new_path, thumbnail=thumbnail_path)

@router.get("/versions/{image_id}")
async def get_versions(image_id: int, db: Session = Depends(get_db)):
    versions = db.query(ImageVersion).filter(ImageVersion.image_id == image_id).order_by(ImageVersion.id.desc()).all()
    latest_version = get_latest_version(db, image_id)
    return {
        "versions": [{"version_id": v.version_id, "path": v.processed_path, "thumbnail": v.processed_thumbnail_path} for v in versions],
        "latest_version": {
            "version_id": latest_version.version_id,
            "processed_path": latest_version.processed_path
        }
    }

@router.post("/revert/{image_id}/{version_id}")
async def revert_version(image_id: int, version_id: str, db: Session = Depends(get_db)):
    version = db.query(ImageVersion).filter(ImageVersion.image_id == image_id, ImageVersion.version_id == version_id).first()
    if not version:
        logging.error(f"Version not found: {version_id}")
        raise HTTPException(status_code=404, detail="Version not found")
    
    latest_version = get_latest_version(db, image_id)
    latest_version.processed_path = version.processed_path
    latest_version.processed_thumbnail_path = version.processed_thumbnail_path
    db.commit()

    logging.info(f"Reverted successfully: {image_id}, version: {version_id}")
    return {"message": "Reverted successfully", "version_id": version_id}

@router.get("/serve/{image_id}")
async def serve_image(image_id: int, db: Session = Depends(get_db)):
    image = get_image_or_404(db, image_id)
    return serve_file(image.original_path, "image/jpeg")

@router.get("/serve/latest/{image_id}")
async def serve_latest_image(image_id: int, db: Session = Depends(get_db)):
    latest_version = get_latest_version(db, image_id)
    return serve_file(latest_version.processed_path, "image/jpeg")

@router.get("/serve/latest-thumbnail/{image_id}")
async def serve_latest_thumbnail(image_id: int, db: Session = Depends(get_db)):
    latest_version = get_latest_version(db, image_id)
    return serve_file(latest_version.processed_thumbnail_path, "image/jpeg")

@router.get("/serve-by-path/")
async def serve_image_by_path(image_path: str = Query(...)):
    return serve_file(image_path, "image/jpeg")

def get_image_or_404(db, image_id: int):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image