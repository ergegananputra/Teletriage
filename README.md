# Teletriage Local Version

## Run With Docker Compose (Recommended)

```bash
docker compose up --build
```

Frontend: `http://127.0.0.1:6501`
Backend: `http://127.0.0.1:6502`

## Optional Local Run (Without Docker)

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
