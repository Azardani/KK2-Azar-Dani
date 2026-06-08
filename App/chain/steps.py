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
{input.stats}

Answer using ONLY the provided facts.
Do not make assumptions.
Do not add extra information.
Write one short sentence.
dont say "in the world"

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
            max_new_tokens=30,
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