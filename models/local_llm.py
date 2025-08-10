# models/local_llm.py

class LocalLLM:
    def __init__(self, path):
        self.path = path
    def generate(self, prompt: str):
        # call into the local runtime
        return "(local model output)"
