from pydantic import BaseModel


class UserCreate (BaseModel):
    name: str 

class USerRead(BaseModel):
    id: int
    name: str 


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    model: str


class PromptBuilderInput(BaseModel):
    question: str
    stats: dict
    most_expensive: dict


class PromptBuilderOutput(BaseModel):
    prompt: str


class LLMRunnerOutput(BaseModel):
    raw_output: str


class ResponseParserOutput(BaseModel):
    answer: str