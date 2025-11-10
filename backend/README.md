# Audio-to-Sheet Music Backend

FastAPI backend для транскрипции аудиофайлов в нотную запись с использованием Basic Pitch.

## Возможности

- 🎵 Транскрипция аудио в MIDI формат
- 📝 Конвертация в MusicXML
- 🚀 Async API с FastAPI
- 📁 Управление файлами и автоочистка
- 🔒 Валидация и обработка ошибок

## Установка

### 1. Установить pip (если не установлен)

```bash
python3 -m ensurepip --upgrade
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Настроить окружение

```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

## Запуск

### Development режим

```bash
python main.py
```

Или с uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен по адресу: `http://localhost:8000`

## API Endpoints

### Health Check

```bash
GET /api/health
```

### Upload Audio

```bash
POST /api/upload
Content-Type: multipart/form-data

file: <audio_file>
```

Response:
```json
{
  "transcription_id": "uuid",
  "status": "uploaded",
  "message": "File uploaded successfully",
  "created_at": "2025-11-10T..."
}
```

### Transcribe Audio

```bash
POST /api/transcribe/{transcription_id}
```

Response:
```json
{
  "transcription_id": "uuid",
  "status": "completed",
  "message": "Transcription completed successfully",
  "midi_file": "/path/to/file.mid",
  "musicxml_file": "/path/to/file.musicxml",
  "created_at": "2025-11-10T..."
}
```

### Download File

```bash
GET /api/download/{transcription_id}/{file_type}
```

`file_type`: `midi` или `musicxml`

### Get Status

```bash
GET /api/status/{transcription_id}
```

### Delete Transcription

```bash
DELETE /api/transcription/{transcription_id}
```

## Поддерживаемые форматы

- WAV
- MP3
- OGG
- FLAC
- M4A

## Технологии

- **FastAPI** - современный async web framework
- **Basic Pitch** - ML модель от Spotify для audio-to-MIDI
- **Music21** - библиотека для работы с музыкальными нотами
- **Librosa** - анализ аудио
- **Uvicorn** - ASGI сервер

## Структура проекта

```
backend/
├── main.py              # FastAPI приложение
├── audio_processor.py   # Обработка аудио и транскрипция
├── requirements.txt     # Python зависимости
├── .env.example         # Пример конфигурации
├── uploads/             # Загруженные файлы
└── temp/                # Временные файлы
```

## Примеры использования

### С curl

```bash
# Upload file
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@/path/to/audio.mp3"

# Transcribe
curl -X POST "http://localhost:8000/api/transcribe/{transcription_id}"

# Download MIDI
curl -O "http://localhost:8000/api/download/{transcription_id}/midi"
```

### С Python

```python
import requests

# Upload
with open('audio.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )
    transcription_id = response.json()['transcription_id']

# Transcribe
response = requests.post(
    f'http://localhost:8000/api/transcribe/{transcription_id}'
)

# Download
response = requests.get(
    f'http://localhost:8000/api/download/{transcription_id}/midi'
)
with open('output.mid', 'wb') as f:
    f.write(response.content)
```

## Troubleshooting

### Ошибка установки зависимостей

Если возникают проблемы с установкой `basic-pitch` или `librosa`:

```bash
# Установить системные зависимости (Amazon Linux)
sudo dnf install -y libsndfile-devel

# Обновить pip
pip install --upgrade pip setuptools wheel
```

### Ошибка "No module named 'tensorflow'"

Basic Pitch требует TensorFlow. Он должен установиться автоматически, но если нет:

```bash
pip install tensorflow==2.13.0
```

## Лицензия

MIT
