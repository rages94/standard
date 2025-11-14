from ollama import AsyncClient


class LLMGenerate:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def __call__(self, model_name: str, prompt: str) -> str:
        return (await self.client.generate(model=model_name, prompt=prompt)).response
