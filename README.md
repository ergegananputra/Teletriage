# Teletriage Local Version

## Run

```bash
pip install -r requirements.txt
python run_system.py
```

Frontend: `http://127.0.0.1:8501`
Backend: `http://127.0.0.1:8000`

## Default admin

Username: `admin`
Password: `ChangeMe123!`

## Notes
- Pasien menggunakan form stabil tanpa auto-refresh.
- Admin memakai auto-refresh agar data masuk terlihat real-time.
- GPS pasien dikirim background dari browser ke backend.
- SQLite dipakai untuk versi local.
