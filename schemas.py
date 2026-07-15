from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransaksiCreate(BaseModel):
    user_id: str
    tipe: str      # 'pemasukan' / 'pengeluaran'
    nominal: float
    kategori: str
    catatan: Optional[str] = None

class TransaksiResponse(TransaksiCreate):
    id: int
    tanggal: datetime

    class Config:
        from_attributes = True