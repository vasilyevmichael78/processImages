from pydantic import BaseModel

class ImageUploadSchema(BaseModel):
    filename: str

class ImageResponseSchema(BaseModel):
    id: int
    filename: str
    original: str
    thumbnail: str

class TransformationRequest(BaseModel):
    transformation: str

    