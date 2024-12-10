from pydantic import BaseModel

class Item(BaseModel):
    id: int
    item_name: str
    category: str
    price: float
    quantity: int
    subtotal: float

class ItemsRequest(BaseModel):
    items: list[Item]

class ItemResponse(Item):
    category: str  # Mengubah category sesuai prediksi
