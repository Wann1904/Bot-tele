from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True) # ID Telegram atau ID User dari Flutter
    tipe = Column(String)                # 'pemasukan' atau 'pengeluaran'
    nominal = Column(Float)
    kategori = Column(String)            # contoh: makanan, gaji, transport
    catatan = Column(String, nullable=True)
    tanggal = Column(DateTime, default=datetime.utcnow)