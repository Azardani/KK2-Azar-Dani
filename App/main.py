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

    data.current_df = pd.read_csv(
        file.file,
        sep=";"
    )

    data.current_df["Price"] = pd.to_numeric(
        data.current_df["Price"],
        errors="coerce"
    )

    data.current_df["Mileage"] = pd.to_numeric(
        data.current_df["Mileage"],
        errors="coerce"
    )

    data.current_df["Year"] = pd.to_numeric(
        data.current_df["Year"],
        errors="coerce"
    )

    data.current_df = data.current_df.dropna(
        subset=["Price", "Mileage", "Year"]
    )

    return {
        "rows": len(data.current_df),
        "columns": list(data.current_df.columns)
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

    question = request.question.lower()

    if "expensive" in question:
        fact = summary["most_expensive"]

    elif "mileage" in question:
        fact = summary["most_miles"]

    elif "cheapest" in question:
        fact = summary["cheapest"]
    
    elif "least miles" in question or "low" in question:
        fact = summary["least_miles"]

    elif "oldest" in question or "old" in question:
        fact = summary["oldest"]

    elif "newest" in question or "new" in question:
        fact = summary["newest"]

    else:
        fact = summary

    chain_input = PromptBuilderInput(
        question=request.question,
        stats=fact
    )

    result = oracle_chain.invoke(chain_input)

    return QuestionResponse(
        question=request.question,
        answer=result.answer,
        model="SmolLM2-135M-Instruct"
    )