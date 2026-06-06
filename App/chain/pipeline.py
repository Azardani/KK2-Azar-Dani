from App.chain.steps import (
    PromptBuilder,
    LLMRunner,
    ResponseParser
)

oracle_chain = (
    PromptBuilder()
    | LLMRunner()
    | ResponseParser()
)