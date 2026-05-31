import pandas as pd
from fastapi import FastAPI, UploadFile, File

from App import data
from App.schemas import QuestionRequest, QuestionResponse

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/data/upload")
async def upload_data(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    data.current_df = pd.read_csv(file.file)

    return {
        "rows": len(data.current_df),
        "columns": list(data.current_df.columns),
        "dtypes": {
            col: str(dtype)
            for col, dtype in data.current_df.dtypes.items()
        }
    }


@app.get("/data/stats")
def get_stats():

    if data.current_df is None:
        return {"error": "No dataset uploaded"}

    return data.current_df.describe().to_dict()


@app.post("/ai/ask")
def ask_ai(request: QuestionRequest):

    return QuestionResponse(
        question=request.question,
        answer="Din Mammaaaaaaaa.",
        model="FakeModel"
    )