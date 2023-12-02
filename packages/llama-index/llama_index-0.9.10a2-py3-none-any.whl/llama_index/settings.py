from typing import Optional, Callable

from llama_index.bridge.pydantic import BaseModel, PrivateAttr
from llama_index.embeddings import BaseEmbedding
from llama_index.embeddings.utils import resolve_embed_model
from llama_index.llms import LLM
from llama_index.llms.utils import resolve_llm


class Settings(BaseModel):
    """Settings for the Llama Index, lazily initialized."""

    _llm: Optional[LLM] = PrivateAttr(None)
    _embed_model: Optional[LLM] = PrivateAttr(None)

    @property
    def llm(self) -> LLM:
        """Get the LLM."""
        if self._llm is None:
            self._llm = resolve_llm("default")
        return self._llm

    @property.setter
    def llm(self, llm: LLM) -> None:
        """Set the LLM."""
        self._llm = llm

    @property
    def embed_model(self) -> BaseEmbedding:
        """Get the embedding model."""
        if self._embed_model is None:
            self._embed_model = resolve_embed_model("default")
        return self._embed_model

    @property.setter
    def embed_model(self, embed_model: BaseEmbedding) -> None:
        """Set the embedding model."""
        self._embed_model = embed_model
