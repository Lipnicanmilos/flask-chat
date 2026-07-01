# Flask Code Board

Jednoduchá appka na zdieľanie príspevkov s kódom — registrácia/prihlásenie, tvorba príspevkov (text + code snippet), komentáre pod príspevkami a úprava vlastných príspevkov.

> Poznámka: pôvodný názov repozitára ("flask-chat") je zavádzajúci — appka neobsahuje real-time chat, ale skôr jednoduché fórum na zdieľanie kódu a diskusiu pod príspevkami.

## Funkcie

- Registrácia a prihlásenie používateľov (heslá hashované cez Werkzeug)
- Vytváranie príspevkov s textom aj úryvkom kódu
- Komentáre pod príspevkami
- Úprava vlastných príspevkov
- Stránkovanie zoznamu príspevkov

## Technológie

- Python, Flask, Flask-SQLAlchemy
- SQLite

## Lokálne spustenie

1. Vytvor virtuálne prostredie a nainštaluj závislosti:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Skopíruj `.env.example` na `.env`:
   ```bash
   cp .env.example .env
   ```

3. Spusti aplikáciu:
   ```bash
   python app.py
   ```
   Aplikácia beží na `http://localhost:5000`.

## Poznámka

Cvičný/portfóliový projekt. Databáza (`database.db`) sa vytvorí automaticky pri prvom spustení a nie je súčasťou repozitára.
