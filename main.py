import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3

# ⚠️ PENTING: Simpan token di environment variable, bukan hardcode!
# Export TOKEN=YOUR_TOKEN di terminal, atau buat file .env
TOKEN = "8881078652:AAEj-804xIW7kZiWA8nQW3yAZBc06O4R9QI"

# Inisialisasi database
def init_db():
    """Buat tabel jika belum ada"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tipe TEXT,
            nominal INTEGER,
            keterangan TEXT,
            tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def simpan(user_id, tipe, nominal, keterangan):
    """Simpan transaksi ke database"""
    try:
        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transaksi(user_id, tipe, nominal, keterangan)
            VALUES (?, ?, ?, ?)
        """, (user_id, tipe, nominal, keterangan))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /start"""
    await update.message.reply_text(
        "Bot berhasil jalan 🚀\n\n"
        "Perintah:\n"
        "/keluar [nominal] [keterangan] - Catat pengeluaran\n"
        "/masuk [nominal] [keterangan] - Catat pemasukan\n"
        "/laporan - Lihat laporan keuangan"
    )

async def keluar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /keluar (pengeluaran)"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Format salah!\n\n"
            "Contoh:\n"
            "/keluar 20000 Makan siang"
        )
        return

    try:
        nominal = int(context.args[0])
        keterangan = " ".join(context.args[1:])

        if simpan(update.effective_user.id, "keluar", nominal, keterangan):
            await update.message.reply_text(
                f"💸 Pengeluaran berhasil dicatat\n\n"
                f"Rp{nominal:,}\n"
                f"Keterangan: {keterangan}"
            )
        else:
            await update.message.reply_text("❌ Gagal menyimpan data")
    except ValueError:
        await update.message.reply_text("❌ Nominal harus berupa angka!")

async def masuk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /masuk (pemasukan)"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Format salah!\n\n"
            "Contoh:\n"
            "/masuk 100000 Gaji"
        )
        return

    try:
        nominal = int(context.args[0])
        keterangan = " ".join(context.args[1:])

        if simpan(update.effective_user.id, "masuk", nominal, keterangan):
            await update.message.reply_text(
                f"💰 Pemasukan berhasil dicatat\n\n"
                f"Rp{nominal:,}\n"
                f"Keterangan: {keterangan}"
            )
        else:
            await update.message.reply_text("❌ Gagal menyimpan data")
    except ValueError:
        await update.message.reply_text("❌ Nominal harus berupa angka!")

async def laporan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /laporan"""
    try:
        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()
        
        user_id = update.effective_user.id
        
        # Total pengeluaran
        cursor.execute(
            "SELECT SUM(nominal) FROM transaksi WHERE user_id = ? AND tipe = 'keluar'",
            (user_id,)
        )
        total_keluar = cursor.fetchone()[0] or 0
        
        # Total pemasukan
        cursor.execute(
            "SELECT SUM(nominal) FROM transaksi WHERE user_id = ? AND tipe = 'masuk'",
            (user_id,)
        )
        total_masuk = cursor.fetchone()[0] or 0
        
        saldo = total_masuk - total_keluar
        
        conn.close()
        
        await update.message.reply_text(
            f"📊 Laporan Keuangan\n\n"
            f"💰 Pemasukan: Rp{total_masuk:,}\n"
            f"💸 Pengeluaran: Rp{total_keluar:,}\n"
            f"💳 Saldo: Rp{saldo:,}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    """Main function"""
    # Inisialisasi database
    init_db()
    
    # Buat aplikasi
    app = Application.builder().token(TOKEN).build()
    
    # Tambah handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("keluar", keluar))
    app.add_handler(CommandHandler("masuk", masuk))
    app.add_handler(CommandHandler("laporan", laporan))
    
    # Run
    print("✅ Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()