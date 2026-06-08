# KK2 Oraklet

## Beskrivning

KK2 Oraklet är en applikation som analyserar fordonsdata från en CSV-fil. Användaren kan ladda upp ett dataset, få statistik om datan och ställa frågor till en AI-modell som använder den analyserade informationen för att generera svar.

Projektet använder Pandas för dataanalys och SmolLM via transformers för att generera naturliga språkbaserade svar.
funkar bäst på engelska!
---

## Funktioner

### Endpoints

#### GET /health

Kontrollerar att API:t fungerar.

Exempel på svar:

```json
{
    "status": "ok"
}
```

#### POST /data/upload

Laddar upp en CSV-fil och sparar den i minnet.

#### GET /data/stats

Returnerar sammanfattande statistik om datasetet, exempelvis:

* Genomsnittligt pris
* Genomsnittligt miltal
* Nyaste bil
* Äldsta bil
* Dyraste bil
* Billigaste bil

#### POST /ai/ask

Tar emot en fråga om datasetet och genererar ett svar med hjälp av en AI-modell.

Exempel:

```json
{
    "question": "Which car is the most expensive?"
}
```

---

## Tekniker

* Python
* FastAPI
* Pandas
* Pydantic
* Transformers
* SmolLM2-135M-Instruct
* Pytest

---

## AI-kedja

Projektet använder en Runnable-kedja bestående av tre steg:

```text
PromptBuilder
↓
LLMRunner
↓
ResponseParser
```

PromptBuilder skapar prompten, LLMRunner anropar språkmodellen och ResponseParser bearbetar modellens svar.

---

## Installation

Installera beroenden:

```bash
uv sync
```

Starta servern:

```bash
py -m uvicorn App.main:app --reload
```

Öppna Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Tester

Kör tester med:

```bash
py -m pytest
```

Projektet innehåller tester för:

* Health endpoint
* Statistikendpoint
* AI-endpoint
* Felaktig filuppladdning

---

## Författare

Azar Dani
