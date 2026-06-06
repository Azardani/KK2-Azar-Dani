import pandas as pd
from fastapi import FastAPI, UploadFile, File
from App.chain.pipeline import oracle_chain
from App.schemas import PromptBuilderInput
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

    data.current_df = pd.read_csv(file.file, sep=";")

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

    try:
        return data.get_summary(
            data.current_df
        )

    except Exception as e:
        return {
            "error": str(e)
        }

@app.post("/ai/ask")
def ask_ai(request: QuestionRequest):

    if data.current_df is None:
        return {"error": "No dataset uploaded"}

    summary = data.get_summary(
        data.current_df
    )

    chain_input = PromptBuilderInput(
        question=request.question,
        stats=summary,
        most_expensive=summary["most_expensive"]
    )

    result = oracle_chain.invoke(chain_input)

    return QuestionResponse(
        question=request.question,
        answer=result.answer,
        model="SmolLM2-135M-Instruct"
    )
    
