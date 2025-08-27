# Название проекта

Краткое описание вашего проекта (одно-два предложения).

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
---

## 🚀 Оглавление

* [О проекте](#-о-проекте)
* [Структура проекта](#-структура-проекта)
* [Функциональность](#-функциональность)
* [Установка и запуск](#-установка-и-запуск)
* [Использование](#-использование)
* [Запуск через Docker](#-запуск-через-docker)
* [Технологии](#-технологии)


---

## 📖 О проекте

Проект для автоматизированного сбора, парсинга и отправки статистики из различных источников (рекламные системы, панели) в Google Sheets и Telegram.

---

## 📁 Структура проекта

```bash
GetStat/
├── 📂 sheet_ids/                  # Конфигурационные файлы для Google Sheets
│   ├── first-gsheet-id            # Идентификатор Google-таблицы
│   ├── second-gsheet-id           # Идентификатор Google-таблицы
│   ├── ✅ credentials.json        # Файл учётных данных для Google API
│   ├── third-gsheet-id            # Идентификатор основной таблицы
│   └── fourth-gsheet-id           # Идентификатор таблицы с тизерами
├── .env                           # Файл переменных окружения (дата, курс доллара)
├── ✅ bootstrap.py                # Скрипт первоначальной настройки проекта
├── ✅ Creds.py                    # Файл учетных данных рекламныз площадок и Telegram
├── ✅ docker-compose.yml          # Конфигурация Docker Compose для развёртывания
├── ✅ Dockerfile                  # Инструкция для сборки Docker-образа
├── ✅ GetStops.py                 # Скрипт для получения данных о стопах
├── ✅ GetTeasersStat.py           # Главный скрипт для получения статистики тизеров
├── ✅ PharsePopsEvadav.py         # Парсер статистики из Evadav (Pops)
├── ✅ PharseStatKadam.py          # Парсер статистики из Kadam
├── ✅ PharseStatTor.py            # Парсер статистики из Tor
├── ✅ Readme.md                   # Этот файл
├── ✅ requirements.txt            # Зависимости Python
├── ✅ SendTeasersStat.py          # Скрипт для отправки статистики в Google Sheets
├── ✅ Survey2Stat.py              # Скрипт для обработки опросов и преобразования в статистику
├── ✅ tg_bot.py                   # Модуль Telegram-бота для сбора данных с чата
└── ✅ Инструкция к запуску.txt    # Инструкция по запуску
```
---

## ✨ Функциональность

Ключевые функции вашего проекта. Используйте список для удобства чтения.

*   **Парсинг данных:** "Получение и обработка статистики из различных источников: Kadam, Evadav, Tor".
*   **Работа с Google Sheets:** "Автоматическая отправка собранных данных в указанные Google-таблицы".
*   **Мониторинг данных:** Интеграция с Telegram-ботом для сбора данных в Google-таблицы".
*   **Докеризация:** Готовность к запуску в изолированных Docker-контейнерах

---

## 🛠️ Установка и запуск

Пошаговая инструкция по установке и запуску проекта локально для разработки и тестирования.

**Предварительные требования:** Убедитесь, что у вас установлены:
* Python 3.8+
* pip (менеджер пакетов Python)
* Учётная запись Google Cloud с включённым Sheets API
* (Опционально) Docker и Docker Compose

**Инструкция по установке:**

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Beasbe/tg-bot-and-advertisers-API-to-google-docs.git
    cd tg-bot-and-advertisers-API-to-google-docs
    ```

2.  Создание виртуального окружения:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    ```
    *или*
    ```bash
    venv\Scripts\activate     # Для Windows
    ```

3.  Установка зависимостей:
    ```bash
    pip install -r requirements.txt
    ```

4. Настройка Google Sheets API:
    * Файл credentials.json должен быть помещён в папку sheet_ids/.
    * Вручную заполните файлы в папке sheet_ids/ соответствующими идентификаторами ваших Google-таблиц.
>Идентификатор можно найти в URL вашей таблицы: https://docs.google.com/spreadsheets/d/<ВАШ_ID_ТАБЛИЦЫ>/edit#gid=0


4.  Запустите скрипт:
    ```bash
    python bootstrap.py <Дата> <Курс Доллара>
    ```




---
## 🎯 Использование

### Основной workflow:
1. **Сбор данных:** Запускаются парсеры для получения статистики из различных источников
2. **Обработка:** Данные преобразуются в единый формат
3. **Отправка:** Статистика загружается в Google Sheets

### Команды для запуска:

**Запуск полного цикла сбора статистики:**
```bash
python bootstrap.py <Дата> <Курс Доллара>
```

**Запуск отдельных парсеров:**
```bash
# Для получения статистики из Kadam
python PharseStatKadam.py
```
```bash
# Для обработки Pops из Evadav
python PharsePopsEvadav.py
```
```bash
# Для сбора данных из Tor
python PharseStatTor.py
```

**Отправка данных в Google Sheets:**

```bash
python SendTeasersStat.py
```
**Запуск мониторинга стоп-слов:**

```bash
python GetStops.py
```
**Конвертация данных опросов:**

```bash
python Survey2Stat.py
```
---
## 🐳 Запуск через Docker
Альтернативный способ запуска с использованием Docker:
```bash
docker build -t my-python-app .
docker run my-python-app <Дата> <Курс Доллара>
```
* <Дата> - dd.mm.yyy
* <Курс Доллара> - число

---
## 🛠️ Технологии

Проект построен на следующих основных технологиях и библиотеках:

### **Основные языки и платформы:**
- ![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white) - Основной язык программирования
- ![Google Sheets API](https://img.shields.io/badge/Google_Sheets_API-34A853?logo=google-sheets&logoColor=white) - Для работы с Google таблицами
- ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) - Для контейнеризации приложения

### **Ключевые Python-библиотеки:**

#### **Работа с Google Sheets:**
```python
import gspread
from google.oauth2.service_account import Credentials
```
**HTTP-запросы и работа с API:**

```python
import requests
import json
```

**Работа с датами и временем:**
```python
from datetime import datetime, timedelta
import time
```

**Дополнительные утилиты:**
```python
import os
import re
import subprocess
```
