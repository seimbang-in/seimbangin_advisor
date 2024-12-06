import pandas as pd
import random
import re

# Kumpulan kata dan frase yang lebih kompleks untuk setiap kategori
receipt_data = {
    'Makanan dan Minuman': {
        'phrases': [
    "nasi goreng spesial", "sate ayam porsi besar", "pizza medium keju", 
    "kopi hitam panas", "es teh manis", "smoothie buah segar", 
    "bakso komplit", "mie ayam spesial", "burger double cheese",
    "sushi roll salmon", "cappuccino large", "fresh juice mix",
    "soto ayam kuah bening", "nasi liwet komplit", "rendang sapi porsi besar",
    "ayam geprek pedas", "lontong sayur spesial", "sate kambing madu", 
    "martabak cokelat keju", "pisang goreng crispy", "kentang goreng porsi sedang",
    "roti bakar cokelat", "es campur segar", "jus alpukat murni", 
    "wedang ronde", "kopi susu kekinian", "teh tarik hangat", 
    "es kopi gula aren", "donat isi cokelat", "bakso urat kuah pedas", 
    "nasi padang paket hemat", "ayam bakar kecap", "burger ayam spesial",
    "spaghetti bolognese", "sushi sashimi mix", "cappuccino panas kecil",
    "pizza deluxe pepperoni", "brownies kukus lembut", "salad buah segar", 
    "steak sapi saus jamur", "ikan bakar rica", "dimsum ayam udang", 
    "bebek goreng sambal ijo", "sop buntut komplit", "mie instan kuah pedas", 
    "kue cubit mini", "keripik kentang pedas", "sandwich isi telur", 
    "susu murni", "roti sobek pandan", "puding cokelat lembut", 
    "smoothie mangga", "sosis bakar BBQ", "keripik singkong", 
    "tahu isi goreng", "bihun goreng seafood", "ayam crispy saus keju", 
    "kue lapis legit", "es cendol dawet", "jus jeruk murni", 
    "milkshake vanilla", "pancake cokelat", "es krim cone", 
    "omelette sayur", "kerupuk udang", "salad sayur mayones", 
    "nasi goreng kambing", "roti tawar selai", "cupcake cokelat", 
    "es teh lemon", "ayam rica rica", "mie goreng jawa", 
    "pecel lele paket", "sate taichan pedas", "warung nasi uduk", 
    "donat tabur gula", "roti pisang keju", "brownies cokelat almond", 
    "martabak telur", "roti gandum isi ayam", "churros cokelat saus", 
    "ayam goreng lalapan", "popcorn caramel", "es teler jumbo", 
    "macaron aneka rasa", "lasagna", "sate maranggi", 
    "bakwan jagung", "risoles isi ayam", "es kelapa muda", 
    "jus semangka", "daging sapi panggang", "ikan goreng sambal", 
    "pisang cokelat keju", "ayam gulai", "mie ayam jamur", 
    "soto mie", "burger ayam double", "sup tom yam"
],
        'prefixes': ['Rp', 'Total', 'Harga'],
        'suffixes': ['x1', 'porsi', 'paket']
    },
    'Transportasi': {
        'phrases': [
    "bensin motor", "gojek ke kantor", "tol dalam kota", 
    "parkir mobil", "tiket bus trans", "solar untuk truk", 
    "grab ke bandara", "servis motor", "cuci mobil", 
    "ganti oli mesin", "tiket kereta ekonomi", "bayar parkir",
    "bensin mobil", "angkot jarak dekat", "taksi ke mall",
    "ojek online malam", "sewa mobil harian", "kereta api eksekutif", 
    "tiket ferry", "biaya tol antarkota", "bus antarprovinsi",
    "angkot jalur A", "ojek ke sekolah", "cuci motor", 
    "tiket MRT", "parkir motor mall", "grab express", 
    "biaya jemputan", "spbu shell", "pengisian bensin premium", 
    "biaya parkir gedung", "sewa bus wisata", "travel bandara", 
    "taksi bandara", "bengkel mobil besar", "ganti aki mobil", 
    "spare part motor", "service rem mobil", "pembayaran tol e-money", 
    "perbaikan mesin mobil", "isi nitrogen ban", "ban mobil baru", 
    "perbaikan ban motor", "servis AC mobil", "tarif angkot malam", 
    "karcis busway", "sewa kendaraan roda empat", "tiket kereta api", 
    "biaya antar barang", "tarif jemput penumpang", "grab car pagi", 
    "ojek pangkalan", "pengisian bahan bakar solar", "tiket kereta cepat", 
    "bayar parkir basement", "spbu total", "tol luar kota", 
    "sewa motor harian", "ganti oli motor", "penyeberangan ferry", 
    "bus ekonomi AC", "parkir harian mall", "service berkala motor", 
    "tiket perjalanan kereta", "cuci mobil detailing", "modifikasi motor", 
    "perbaikan lampu mobil", "tiket KRL Jabodetabek", "tarif ojek ke pasar", 
    "biaya servis suspensi", "spare part mobil", "tiket commuter line", 
    "service mesin motor", "pembelian oli mesin", "isi bensin pertalite", 
    "tarif tol otomatis", "tarif bus transprovinsi", "tiket perjalanan jauh", 
    "tiket MRT bulanan", "cuci motor biasa", "tambal ban motor", 
    "tambal ban mobil", "ganti rem mobil", "taksi malam hari", 
    "spbu pertamina", "penggantian ban mobil", "sewa mobil dengan supir", 
    "tiket bus malam", "parkir motor gedung", "tiket kereta api bisnis", 
    "ojek ke terminal", "pengisian bahan bakar pertamax", "pengisian nitrogen", 
    "kartu tol elektronik", "tiket angkutan umum", "tiket kapal laut", 
    "biaya antar logistik"
],
        'prefixes': ['Tarif', 'Biaya', 'Total'],
        'suffixes': ['km', 'hari', 'kali']
    },
    'Utilitas': {
        'phrases': [
    "token listrik", "tagihan air PDAM", "pulsa Telkomsel", 
    "internet WiFi bulanan", "TV kabel IndiHome", "paket data XL", 
    "pembayaran PLN", "langganan streaming", "telepon rumah", 
    "iuran sampah", "air minum galon", "internet rumah unlimited", 
    "langganan aplikasi streaming", "pulsa Indosat", "pembelian token listrik", 
    "langganan Spotify", "biaya langganan YouTube Premium", "internet paket keluarga", 
    "pembayaran listrik bulanan", "iuran TV kabel", "langganan Disney+", 
    "pulsa darurat", "biaya WiFi kantor", "pembayaran PDAM", 
    "token listrik prabayar", "langganan cloud storage", "paket data internet harian", 
    "iuran air bersih", "telepon rumah Telkom", "pembayaran IndiHome", 
    "langganan aplikasi edukasi", "iuran lingkungan", "internet fiber optic", 
    "biaya berlangganan aplikasi", "pembayaran bulanan Netflix", "token listrik prabayar 50k", 
    "langganan Amazon Prime", "air minum kemasan", "biaya listrik pascabayar", 
    "paket data mingguan", "pembelian pulsa internet", "internet bulanan rumah", 
    "iuran kebersihan", "tagihan listrik pascabayar", "langganan aplikasi olahraga", 
    "pulsa XL prabayar", "paket data unlimited", "langganan game online", 
    "biaya pemasangan internet", "pembayaran air minum bulanan", "tagihan WiFi bulanan", 
    "pembelian pulsa Telkomsel", "iuran air tanah", "langganan layanan digital", 
    "biaya internet provider lokal", "langganan HBO GO", "token listrik 100 ribu", 
    "paket data Indosat", "langganan Google Drive", "pembayaran hosting website", 
    "iuran RT/RW", "langganan video streaming", "pembayaran TV satelit", 
    "pulsa Axis", "langganan musik digital", "iuran saluran air", 
    "pembelian token listrik 20 ribu", "langganan aplikasi membaca", "tagihan bulanan IndiHome", 
    "langganan platform edukasi", "langganan WiFi bulanan", "biaya iuran keamanan", 
    "biaya TV berlangganan", "pembayaran Spotify Premium", "pulsa internet harian", 
    "iuran televisi digital", "paket data murah", "biaya pemakaian listrik", 
    "internet provider fiber", "token listrik 200 ribu", "langganan aplikasi olahraga", 
    "tagihan air rumah tangga", "langganan majalah digital", "pembelian token PLN", 
    "langganan internet premium", "biaya instalasi WiFi", "langganan aplikasi hiburan", 
    "iuran langganan digital", "langganan Netflix bulanan", "paket data roaming", 
    "biaya pemasangan IndiHome", "langganan platform musik", "iuran bulanan air bersih", 
    "pembayaran WiFi unlimited", "pulsa kartu perdana", "langganan aplikasi produktivitas", 
    "tagihan PLN pascabayar"
],
        'prefixes': ['Tagihan', 'Biaya', 'Total'],
        'suffixes': ['bulan', 'periode', 'aktif']
    },
    'Hiburan': {
        'phrases':[
    "tiket bioskop", "langganan Netflix", "game online", 
    "karaoke malam", "konser musik", "bowling satu jam", 
    "tiket konser", "steam game", "Spotify Premium", 
    "arcade game", "tiket wahana", "sewa PlayStation", 
    "langganan Disney+", "tiket museum", "permainan timezone", 
    "tiket taman hiburan", "sewa alat musik", "langganan YouTube Premium", 
    "tiket teater", "game mobile premium", "tiket waterpark", 
    "nonton film digital", "membership gym", "sewa alat ski", 
    "tiket pertandingan sepak bola", "festival budaya", "langganan Amazon Prime", 
    "tiket acara seni", "langganan aplikasi hiburan", "persewaan film online", 
    "bermain futsal", "nonton konser virtual", "pembelian skin game", 
    "ke taman bermain", "tiket klub malam", "pembelian DLC game", 
    "tiket masuk zoo", "pembelian karakter game", "tiket kolam renang", 
    "ke pertunjukan balet", "langganan layanan streaming", "nonton live music", 
    "pembelian item virtual", "tiket stand-up comedy", "membership komunitas olahraga", 
    "bermain paintball", "voucher game digital", "ke arena trampolin", 
    "tiket pertunjukan sirkus", "voucher game mobile", "pembelian bundle game", 
    "sewa sepatu roda", "langganan aplikasi musik", "ke pameran seni", 
    "tiket roller coaster", "bermain VR game", "langganan aplikasi film", 
    "tiket turnamen esports", "bermain escape room", "pembelian karakter animasi", 
    "nonton drama teater", "membership klub kebugaran", "pembelian tiket pameran", 
    "nonton pertunjukan seni", "tiket bioskop 3D", "langganan platform gaming", 
    "bermain biliar", "ke lapangan golf mini", "pembelian emote game", 
    "ke arena balap gokart", "langganan streaming video", "nonton opera", 
    "tiket festival musik", "membership spa", "ke acara cosplay", 
    "pembelian soundtrack game", "ke acara komik", "tiket bioskop VIP", 
    "langganan TV kabel hiburan", "bermain tenis meja", "tiket wahana taman air", 
    "langganan Crunchyroll", "membership taman olahraga", "tiket acara kuliner", 
    "langganan aplikasi podcast", "ke pameran teknologi", "bermain darts", 
    "tiket wisata budaya", "voucher film digital", "ke acara balapan", 
    "pembelian tiket game online", "tiket bioskop IMAX", "bermain puzzle room", 
    "tiket ke taman safari", "pembelian battle pass game", "tiket VIP konser"
],
        'prefixes': ['Harga', 'Tiket', 'Biaya'],
        'suffixes': ['jam', 'malam', 'hari']
    },
    'Belanja': {
        'phrases': [
    "baju casual", "sepatu olahraga", "tas branded", 
    "smartphone baru", "kosmetik set", "jam tangan", 
    "parfum original", "elektronik murah", "aksesoris HP", 
    "celana jeans", "jaket kulit", "kacamata fashion", 
    "baju formal", "sepatu kantor", "tas ransel", 
    "smartwatch", "lipstik matte", "masker wajah", 
    "earphone bluetooth", "celana pendek", "kaos polos", 
    "blazer wanita", "dompet kulit", "power bank", 
    "headset gaming", "tas selempang", "buku novel", 
    "kerudung syar'i", "kemeja batik", "sandal jepit", 
    "hijab pashmina", "baju anak-anak", "jaket parasut", 
    "gaun pesta", "sandal kulit", "tas laptop", 
    "mouse wireless", "parfum travel", "lip balm", 
    "sarung tangan", "jaket bomber", "earbud", 
    "rok panjang", "baju tidur", "sepatu boots", 
    "tas tote bag", "laptop gaming", "smartphone case", 
    "jam tangan sport", "parfum refill", "lip gloss", 
    "keyboard mekanik", "jaket hoodie", "topi snapback", 
    "baju jersey", "sepatu sneakers", "tas belanja eco", 
    "earphone kabel", "buku pelajaran", "jaket denim", 
    "set kosmetik lengkap", "kaca mata hitam", "tas clutch", 
    "blus wanita", "sepatu formal pria", "power bank slim", 
    "kaos olahraga", "parfum eau de toilette", "buku biografi", 
    "sweater rajut", "sarung tangan motor", "sepatu pantofel", 
    "tas olahraga", "headphone over-ear", "lipstik nude", 
    "sling bag wanita", "tablet murah", "dompet travel", 
    "headset wireless", "kemeja flanel", "sweater hoodie", 
    "rok mini", "topi fedora", "tas punggung anak", 
    "keyboard gaming", "earbud noise cancelling", "kaos lengan panjang", 
    "sepatu slip-on", "tas sling bag pria", "jaket windbreaker", 
    "buku komik", "hijab instan", "mouse gaming", 
    "celana chino", "kaos motif", "jam tangan pintar"
],
        'prefixes': ['Harga', 'Total', 'Diskon'],
        'suffixes': ['unit', 'baru', 'promo']
    },
    'Kesehatan': {
        'phrases': [
    "obat batuk", "vitamin immune", "konsultasi dokter", 
    "masker medis", "hand sanitizer", "suplemen herbal", 
    "rapid test", "obat sakit kepala", "vitamin C", 
    "alat kesehatan", "terapi fisio", "vaksin", 
    "obat flu", "multivitamin anak", "antiseptik cair", 
    "alat pengukur tekanan darah", "inhaler asma", "suplemen tulang", 
    "obat demam", "test kit diabetes", "konsultasi psikolog", 
    "masker kain", "obat alergi", "krim luka bakar", 
    "alat tes kehamilan", "minyak kayu putih", "plester luka", 
    "tablet vitamin D", "krim anti nyeri", "alat bantu jalan", 
    "alat bantu dengar", "obat maag", "kapsul herbal", 
    "salep kulit", "termometer digital", "alat nebulizer", 
    "krim pelembap kulit", "obat mata", "suplemen kolagen", 
    "alat tes kolesterol", "sabun antiseptik", "konsultasi gizi", 
    "obat herbal", "minyak telon", "tablet kalsium", 
    "masker anak-anak", "krim anti bakteri", "obat penurun panas", 
    "suplemen omega-3", "alat tes tekanan darah", "obat diare", 
    "obat luka operasi", "krim penghilang bekas luka", "alat pengukur suhu badan", 
    "kapsul echinacea", "serum vitamin E", "krim anti jamur", 
    "obat pereda nyeri", "suplemen zat besi", "alat bantu pernapasan", 
    "plester kompres demam", "obat pilek", "alat infus portable", 
    "masker N95", "suplemen untuk lansia", "obat antiseptik", 
    "tablet zinc", "injeksi vitamin", "krim eksim", 
    "alat cek saturasi oksigen", "krim pencerah kulit", "obat herbal asma", 
    "alat bantu tidur", "serum wajah vitamin C", "obat kumur antiseptik", 
    "pembalut luka steril", "minuman suplemen kesehatan", "tablet multivitamin wanita", 
    "obat diare anak", "alat ukur gula darah", "krim anti alergi", 
    "obat untuk hipertensi", "masker bedah", "krim untuk jerawat", 
    "suplemen probiotik", "obat pencernaan", "alat bantu fisioterapi", 
    "serum vitamin B5", "krim anti penuaan", "obat herbal untuk tidur", 
    "krim pereda gatal", "pembersih luka", "alat penyemprot hidung", 
    "obat penambah nafsu makan", "minyak herbal", "tablet herbal relaksasi"
],
        'prefixes': ['Biaya', 'Harga', 'Total'],
        'suffixes': ['resep', 'paket', 'satuan']
    },
    'Pendidikan': {
        'phrases': [
    "buku kuliah", "modul belajar", "kursus online", 
    "alat tulis", "bimbel matematika", "ujian sertifikasi", 
    "langganan jurnal", "workshop profesional", "pelatihan bahasa", 
    "buku referensi", "biaya praktikum", "SPP semester", 
    "buku catatan", "kursus coding", "kelas bahasa Inggris", 
    "pensil mekanik", "pelatihan desain grafis", "sertifikasi online", 
    "buku ensiklopedia", "langganan e-book", "alat praktikum", 
    "tas sekolah", "kelas fotografi", "pelatihan bisnis", 
    "kalkulator ilmiah", "papan tulis", "kertas folio", 
    "buku teks matematika", "pelatihan public speaking", "buku sejarah", 
    "penghapus", "kursus komputer", "kelas seni lukis", 
    "langganan jurnal ilmiah", "buku fisika", "biaya pendaftaran ujian", 
    "kursus digital marketing", "modul praktikum", "pelatihan manajemen waktu", 
    "buku catatan harian", "kelas pemrograman", "kertas grafik", 
    "pensil warna", "biaya buku pelajaran", "buku panduan kuliah", 
    "kursus privat", "buku latihan soal", "kelas memasak", 
    "stabilo warna-warni", "kertas HVS", "pelatihan soft skills", 
    "modul pelajaran", "kursus animasi", "buku grammar", 
    "langganan materi online", "tas laptop untuk pelajar", "kelas vokal", 
    "buku cetak bahasa Inggris", "penggaris", "kursus keuangan", 
    "kelas literasi", "buku jurnal akademik", "modul uji kompetensi", 
    "pelatihan robotik", "kelas seni teater", "langganan platform belajar", 
    "kursus editing video", "alat gambar teknik", "buku ulangan harian", 
    "biaya sertifikasi TOEFL", "pelatihan data analysis", "buku software engineering", 
    "kelas pengembangan diri", "kalkulator finansial", "kelas psikologi", 
    "pelatihan penulisan kreatif", "buku literasi digital", "biaya perpustakaan", 
    "kelas bahasa Korea", "kursus fotografi smartphone", "langganan kursus harian", 
    "pelatihan Microsoft Excel", "buku teknik kimia", "modul kursus singkat", 
    "alat ukur geometri", "kursus robotika", "buku panduan presentasi", 
    "kelas retorika", "stiker label untuk buku", "kursus pemrograman Python", 
    "pelatihan Google Workspace", "kelas pembelajaran online", "biaya seminar edukasi", 
    "buku teknik sipil", "kelas riset ilmiah", "modul ekonomi makro"
],
        'prefixes': ['Biaya', 'Total', 'Harga'],
        'suffixes': ['semester', 'program', 'periode']
    }
}

def generate_realistic_receipt_text(category):
    """Membuat teks struk yang lebih realistis"""
    # Pilih komponen secara acak
    phrase = random.choice(receipt_data[category]['phrases'])
    prefix = random.choice(receipt_data[category]['prefixes'])
    suffix = random.choice(receipt_data[category]['suffixes'])

    formats = [
        f"{prefix} {phrase} {suffix}",
        f"{phrase} {suffix}",
        f"{prefix} {phrase}",
        f"{phrase}"
    ]
    
    return random.choice(formats)

def generate_advanced_receipt_dataset(num_samples=25000):
    """Menghasilkan dataset dengan 25000 sampel yang lebih kompleks"""
    data = []
    
    samples_per_category = num_samples // len(receipt_data)
    
    for category in receipt_data:
        for _ in range(samples_per_category):

            text = generate_realistic_receipt_text(category)
            
            if random.random() < 0.2: 
                text = text.lower()
            
            data.append({
                'text': text,
                'category': category
            })
    
    random.shuffle(data)
    
    return pd.DataFrame(data)


advanced_dataset = generate_advanced_receipt_dataset()


advanced_dataset.to_csv('advanced_receipt_classification_dataset.csv', index=False)

print("Pratinjau Dataset:")
print(advanced_dataset.head(10))
print("\nDistribusi Kategori:")
print(advanced_dataset['category'].value_counts())
print("\nPanjang Teks Rata-rata:")
print(advanced_dataset['text'].str.len().mean())

print("\nContoh Dataset untuk Demonstrasi:")
for _, row in advanced_dataset.head(15).iterrows():
    print(f"Teks: '{row['text']}' | Kategori: {row['category']}")