# План проекта: Audio-to-Sheet Music Transcription

## Описание проекта
Полнофункциональное веб-приложение для транскрипции аудиофайлов в нотную запись с использованием открытых AI моделей. Приложение позволяет загружать аудиофайлы, конвертировать их в MIDI и отображать результат в виде нотного стана с возможностью экспорта.

## Цели и задачи
- [x] Создать backend API для обработки аудио и транскрипции
- [x] Интегрировать Basic Pitch (Spotify) для audio-to-MIDI конвертации
- [x] Разработать современный frontend с Next.js и React
- [x] Реализовать визуализацию нотного стана
- [x] Добавить функции проигрывания и экспорта
- [ ] (Опционально) Реализовать запись с микрофона в реальном времени

## Технологический стек
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Python 3, FastAPI, Uvicorn
- **ML/Audio**: Basic Pitch, Music21, Librosa
- **Визуализация нот**: OpenSheetMusicDisplay или ABCjs
- **Audio playback**: Tone.js
- **Инфраструктура**: Amazon Linux 2023, Node.js 22

## Этапы разработки

### Этап 1: Backend (Python + FastAPI) ✓
- [x] Создать структуру backend проекта
- [x] Настроить requirements.txt с зависимостями
- [x] Реализовать FastAPI endpoints:
  - POST /api/upload - загрузка аудиофайла
  - POST /api/transcribe - транскрипция в MIDI
  - GET /api/download/{file_id} - скачивание результата
  - GET /api/health - проверка статуса
- [x] Интегрировать Basic Pitch для транскрипции
- [x] Реализовать конвертацию в MIDI и MusicXML
- [x] Добавить обработку ошибок и валидацию

### Этап 2: Frontend (Next.js + React)
- [ ] Создать Next.js проект с TypeScript и Tailwind
- [ ] Разработать компоненты:
  - AudioUploader - drag & drop загрузка файлов
  - SheetMusicDisplay - отображение нотного стана
  - AudioPlayer - проигрывание аудио/MIDI
  - DownloadButtons - экспорт результатов
- [ ] Настроить API proxy для backend
- [ ] Реализовать state management
- [ ] Добавить темную/светлую тему

### Этап 3: Интеграция и тестирование
- [ ] Протестировать backend endpoints
- [ ] Протестировать frontend компоненты
- [ ] Интеграционное тестирование полного flow
- [ ] Тестирование с различными аудиоформатами
- [ ] Проверка responsive дизайна
- [ ] Build testing (npm run build, type checking)

### Этап 4: Дополнительные функции (опционально)
- [ ] Запись с микрофона через Web Audio API
- [ ] Real-time транскрипция
- [ ] Экспорт в PDF
- [ ] Сохранение истории транскрипций

## Архитектура

```
/vercel/sandbox/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI приложение
│   ├── audio_processor.py  # Обработка аудио
│   ├── midi_converter.py   # MIDI конвертация
│   ├── requirements.txt    # Python зависимости
│   ├── .env.example        # Пример конфигурации
│   └── uploads/            # Временные файлы
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── page.tsx       # Главная страница
│   │   ├── components/    # React компоненты
│   │   └── api/           # API routes (proxy)
│   ├── public/            # Статические файлы
│   └── package.json       # Node зависимости
├── PLAN.md                # Этот файл
└── README.md              # Документация

```

## Ключевые технические решения

### Backend
- **Basic Pitch**: Open-source модель от Spotify для audio-to-MIDI
- **Music21**: Библиотека для работы с музыкальными нотами
- **FastAPI**: Современный async Python framework
- **File Management**: Временное хранилище с автоочисткой

### Frontend
- **Next.js App Router**: Современная архитектура
- **Tailwind CSS**: Utility-first CSS framework
- **OpenSheetMusicDisplay**: Рендеринг нотного стана
- **Tone.js**: Web Audio API для проигрывания MIDI

## Временные рамки
- **Начало проекта**: 10 ноября 2025
- **Backend**: 1-2 часа
- **Frontend**: 2-3 часа
- **Интеграция и тестирование**: 1-2 часа
- **Планируемое завершение базовой версии**: 10 ноября 2025

## Риски и ограничения
- **Качество транскрипции**: Зависит от качества входного аудио и сложности музыки
- **Производительность**: Обработка больших файлов может занимать время
- **Real-time**: Требует оптимизации и может быть сложна в реализации
- **Форматы**: Поддержка ограничена форматами, которые поддерживает Basic Pitch

## Следующие шаги
1. ✅ Создать структуру backend проекта
2. ✅ Установить Python зависимости
3. ✅ Реализовать FastAPI endpoints
4. → Создать Next.js frontend
5. → Интегрировать компоненты
6. → Тестирование
