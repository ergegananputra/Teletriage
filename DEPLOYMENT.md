# 🚀 Teletriage Auto-Update Guide

## Cara Update Server dari GitHub Tanpa Admin

### 📋 PERSYARATAN:
1. Server sudah punya akses SSH
2. Git sudah terinstall di server
3. Python sudah terinstall di server
4. Repository sudah di-clone di server

---

## 🔧 METODE 1: Script Python (Recommended)

### Langkah 1: Upload script ke server
```bash
# Di komputer lokal Anda
scp auto_update.py user@your-server:/path/to/teletriage/
```

### Langkah 2: Jalankan script di server
```bash
# SSH ke server
ssh user@your-server

# Pindah ke direktori project
cd /path/to/teletriage

# Jalankan auto-update
python3 auto_update.py
```

### Apa yang dilakukan script:
- ✅ Fetch latest changes dari GitHub
- ✅ Cek apakah ada update baru
- ✅ Pull latest changes
- ✅ Install/update dependencies
- ✅ Run tests (opsional)
- ✅ Restart services

---

## 🔧 METODE 2: Script Bash (Simple)

### Langkah 1: Upload script ke server
```bash
# Di komputer lokal Anda
scp update.sh user@your-server:/path/to/teletriage/
```

### Langkah 2: Jadikan executable dan jalankan
```bash
# SSH ke server
ssh user@your-server

# Pindah ke direktori project
cd /path/to/teletriage

# Jadikan executable
chmod +x update.sh

# Jalankan update
./update.sh
```

---

## 🔄 METODE 3: Cron Job (Auto Update Otomatis)

### Setup auto update setiap jam:
```bash
# SSH ke server
ssh user@your-server

# Buka crontab
crontab -e

# Tambahkan baris ini (update setiap jam)
0 * * * * cd /path/to/teletriage && python3 auto_update.py >> /var/log/teletriage_update.log 2>&1
```

### Atau update setiap 6 jam:
```bash
# Update setiap 6 jam
0 */6 * * * cd /path/to/teletriage && python3 auto_update.py >> /var/log/teletriage_update.log 2>&1
```

---

## 📋 METODE 4: Manual Git Pull (Simplest)

### Langkah 1: SSH ke server
```bash
ssh user@your-server
```

### Langkah 2: Pull latest changes
```bash
cd /path/to/teletriage
git pull origin main
pip install -r requirements.txt
```

### Langkah 3: Restart aplikasi
```bash
# Jika pakai systemd
sudo systemctl restart teletriage

# Jika pakai streamlit manual
pkill -f streamlit
streamlit run run_system.py
```

---

## 🔐 SETUP AWAL (One-time)

### 1. Clone repository di server
```bash
cd /var/www
git clone https://github.com/michaelgoland1-GLD/Teletriage.git teletriage
cd teletriage
```

### 2. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Setup git credentials (opsional - untuk push)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Test koneksi ke GitHub
```bash
git fetch origin
```

---

## 🎯 RECOMMENDED WORKFLOW

### Untuk update cepat:
```bash
# SSH ke server
ssh user@your-server

# Pindah ke project
cd /path/to/teletriage

# Jalankan auto-update
python3 auto_update.py
```

### Untuk auto update otomatis:
```bash
# Setup cron job
crontab -e

# Tambahkan baris ini
0 */6 * * * cd /path/to/teletriage && python3 auto_update.py >> /var/log/teletriage_update.log 2>&1
```

---

## 📊 MONITORING

### Cek log update:
```bash
# Jika pakai cron job
tail -f /var/log/teletriage_update.log
```

### Cek status git:
```bash
cd /path/to/teletriage
git status
git log --oneline -5
```

---

## ⚠️ TROUBLESHOOTING

### Error: Permission denied
```bash
# Fix permission
chmod +x auto_update.py
chmod +x update.sh
```

### Error: Git pull failed
```bash
# Cek remote
git remote -v

# Reset remote jika perlu
git remote set-url origin https://github.com/michaelgoland1-GLD/Teletriage.git
```

### Error: Pip install failed
```bash
# Update pip
pip3 install --upgrade pip

# Install requirements
pip3 install -r requirements.txt
```

---

## 🎉 SELESAI!

Sekarang Anda bisa update server dari GitHub tanpa perlu melalui admin server. Cukup jalankan script auto-update di server Anda!

**Rekomendasi:** Gunakan cron job untuk auto update otomatis setiap 6 jam.
