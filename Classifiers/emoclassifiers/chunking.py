"""
Conversation chunking code. Shared with MIT.
"""

import pydantic

USER = "user"
ASSISTANT = "assistant"


class Chunker:
    """
    Base class for chunking conversations.
    """
    def chunk_simple_convo(self, simple_convo: list[dict], n_context: int = 3) -> dict:
        """
        Chunk a conversation.
        """
        raise NotImplementedError()


class Chunk(pydantic.BaseModel):
    """
    A chunk of a conversation (or whole conversation).
    May include prior messages as context.
    """
    chunk: list[dict]
    touches_start: bool

    @classmethod
    def from_simple_convo(cls, simple_convo: list[dict], idx: int, n_context: int = 3) -> "Chunk":
        """
        Extract a chunk from a simple conversation given an index.
        """
        assert 0 <= idx < len(simple_convo)
        start_idx = max(0, idx - n_context)
        return cls(
            chunk=simple_convo[start_idx : idx + 1],
            touches_start=start_idx == 0,
        )

    def to_string(self, include_start_indicator: bool = True, do_truncate: bool = False) -> str:
        """
        Convert a chunk to a string.
        """
        elems = []
        if include_start_indicator and self.touches_start:
            elems.append("(This is the start of the conversation.)")
        for i, message in enumerate(self.chunk):
            content = message["content"].strip()
            if do_truncate:
                content = truncate_string(content, sep="[[...Long Message Truncated...]]")
            elems.append(
                '[{marker}{role}{marker}] "{content}"'.format(
                    marker="*" if i == len(self.chunk) - 1 else "",
                    role=message["role"].upper(),
                    content=content,
                )
            )
        return "\n".join(elems)


def truncate_string(string: str, max_len: int = 1500, sep: str = "[...]") -> str:
    """
    Truncate a string to a maximum length.
    """
    if len(string) <= max_len:
        return string
    half_len = max_len // 2
    return string[:half_len] + sep + string[-half_len:]


class SingleMessageChunker(Chunker):
    """
    Chunk a conversation by a single message (with optional context).
    """
    ROLE = None

    @classmethod
    def chunk_simple_convo(cls, simple_convo: list[dict], n_context: int = 3) -> dict:
        chunks = {}
        for i, message in enumerate(simple_convo):
            if message["role"] == cls.ROLE:
                chunk_id = i
                chunks[chunk_id] = Chunk.from_simple_convo(simple_convo, idx=i, n_context=n_context)
        return chunks


class UserMessageChunker(SingleMessageChunker):
    """
    Chunk a conversation by a user message (with optional context).
    """
    ROLE = USER


class AssistantMessageChunker(SingleMessageChunker):
    """
    Chunk a conversation by an assistant message (with optional context).
    """
    ROLE = ASSISTANT


class SingleExchangeChunker(Chunker):
    """
    Chunk a conversation by a single exchange (user+assistant or vice versa).
    """
    ROLE = None
    OTHER_ROLE = None

    @classmethod
    def chunk_simple_convo(cls, simple_convo: list[dict], n_context: int = 3) -> dict:
        chunks = {}
        for i, message in enumerate(simple_convo):
            if message["role"] == cls.ROLE:
                chunk_id = i
                candidate_chunk = Chunk.from_simple_convo(simple_convo, idx=i, n_context=n_context)
                if not any(m["role"] == cls.OTHER_ROLE for m in candidate_chunk.chunk):
                    continue
                chunks[chunk_id] = candidate_chunk
        return chunks


class UserAssistantExchangeChunker(SingleExchangeChunker):
    """
    Chunk a conversation by a user+assistant exchange (with optional context).
    """
    ROLE = ASSISTANT
    OTHER_ROLE = USER


class AssistantUserExchangeChunker(SingleExchangeChunker):
    """
    Chunk a conversation by an assistant+user exchange (with optional context).
    """
    ROLE = USER
    OTHER_ROLE = ASSISTANT


class WholeConversationChunker(Chunker):
    """
    Chunk a whole conversation.
    """
    @classmethod
    def chunk_simple_convo(cls, simple_convo: list[dict], n_context: int = 3) -> dict:
        if not simple_convo:
            return {}
        return {0: Chunk(chunk=simple_convo, touches_start=True)}


CHUNKER_DICT = {
    "user_message": UserMessageChunker(),
    "assistant_message": AssistantMessageChunker(),
    "u_a_exchange": UserAssistantExchangeChunker(),
    "a_u_exchange": AssistantUserExchangeChunker(),
    "whole": WholeConversationChunker,
}
