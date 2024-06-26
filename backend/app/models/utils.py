from enum import Enum

class AgentType(str, Enum):
    CONVERSATIONAL = "Conversational"
    ANALYTICAL = "Analytical"
    GENERATIVE = "Generative"
    RETRIEVAL_BASED = "Retrieval-based"

class AgentStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class LLMChoice(str, Enum):
    GPT_35 = "GPT-3.5"
    GPT_4 = "GPT-4"
    CLAUDE = "Claude"
    ANTHROPIC_100K = "Anthropic-100k"
    CHINCHILLA = "Chinchilla"
    PALM = "PaLM"
    JURASSIC_2 = "Jurassic-2"
    BEDROCK = "Bedrock"
    COHERE = "Cohere"
    LLAMA = "Llama"
    ALPACA = "Alpaca"
    VICUNA = "Vicuna"
    FALCON = "Falcon"
    MPT = "MPT"
    DOLLY = "Dolly"
    STABLELM = "StableLM"
    REDPAJAMA_INCITE = "RedPajama-INCITE"
    OPENASSISTANT = "OpenAssistant"
    