from transformers import pipeline

from App.chain.runnable import Runnable
from App.schemas import (
    PromptBuilderInput,
    PromptBuilderOutput,
    LLMRunnerOutput,
    ResponseParserOutput
)

generator = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct"
)


class PromptBuilder(
    Runnable[PromptBuilderInput, PromptBuilderOutput]
):

    def invoke(
        self,
        input: PromptBuilderInput
    ) -> PromptBuilderOutput:

        prompt = f"""
Question: {input.question}

Facts:

Most expensive car:
{input.stats["most_expensive"]}

Answer:
"""

        return PromptBuilderOutput(
            prompt=prompt
        )


class LLMRunner(
    Runnable[PromptBuilderOutput, LLMRunnerOutput]
):

    def invoke(
        self,
        input: PromptBuilderOutput
    ) -> LLMRunnerOutput:

        result = generator(
            input.prompt,
            max_new_tokens=100,
            do_sample=False
        )

        return LLMRunnerOutput(
            raw_output=result[0]["generated_text"]
        )



class ResponseParser(
    Runnable[LLMRunnerOutput, ResponseParserOutput]
):

    def invoke(
        self,
        input: LLMRunnerOutput
    ) -> ResponseParserOutput:

        answer = input.raw_output

        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1]

        return ResponseParserOutput(
            answer=answer.strip()
        )