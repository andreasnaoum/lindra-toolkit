import asyncio
from enum import Enum
import openai
import pydantic
import Classifiers.emoclassifiers.io_utils as io_utils
from Classifiers.emoclassifiers.chunking import Chunk, CHUNKER_DICT
import Classifiers.emoclassifiers.prompt_templates as prompt_templates


CLASSIFIER_DEFINITION_PATH_DICT = {
    "v1": "assets/definitions/emoclassifiers_v1_lindra.json",
    # "v1_top_level": "assets/definitions/emoclassifiers_v1_top_level_definition.json",
    "v2": "assets/definitions/emoclassifiers_v2_lindra.json",
}


class YesNoUnsureEnum(Enum):
    """
    Classification output.
    """
    YES = "yes"
    NO = "no"
    UNSURE = "unsure"


class ResponseFormat(pydantic.BaseModel):
    """
    Response format for structured completion.
    """
    response: YesNoUnsureEnum


def format_criteria(criteria: list[str]) -> str:
    """
    Format criteria for EmoClassifiers V2.
    """
    return "\n".join(
        [f"- {line}" for line in criteria]
    )


def get_emo_classifiers_v1_prompt(
    classifier_definition: dict,
    chunk: Chunk,
) -> str:
    """
    Construct classification prompt for EmoClassifiers V1 (sub-classifier).
    """
    assert classifier_definition["version"] == "v1"
    return prompt_templates.EMO_CLASSIFIER_V1_PROMPT_TEMPLATE.format(
        classifier_name=classifier_definition["name"],
        prompt=classifier_definition["prompt"],
        snippet_string=chunk.to_string(),
        prompt_short=classifier_definition["prompt"].splitlines()[0],
    )


def get_emo_classifiers_v1_top_level_prompt(
    classifier_definition: dict,
    chunk: Chunk,
) -> str:
    """
    Construct classification prompt for EmoClassifiers V1 (Top Level).
    """
    assert classifier_definition["version"] == "v1_top_level"
    return prompt_templates.EMO_CLASSIFIER_V1_TOP_LEVEL_PROMPT_TEMPLATE.format(
        classifier_name=classifier_definition["name"],
        prompt=classifier_definition["prompt"],
        conversation_string=chunk.to_string(),
    )


def get_emo_classifiers_v2_prompt(
    classifier_definition: dict,
    chunk: Chunk,
) -> str:
    """
    Construct classification prompt for EmoClassifiers V2.
    """
    assert classifier_definition["version"] == "v2"
    return prompt_templates.EMO_CLASSIFIER_V2_PROMPT_TEMPLATE.format(
        classifier_name=classifier_definition["full_name"],
        criteria=format_criteria(classifier_definition["criteria"]),
        snippet_string=chunk.to_string(),
        prompt=classifier_definition["prompt"],
    )


def get_emo_classifiers_prompt(
    classifier_definition: dict,
    chunk: Chunk,
) -> str:
    """
    Construct classification prompt.
    """
    if classifier_definition["version"] == "v1":
        return get_emo_classifiers_v1_prompt(classifier_definition=classifier_definition, chunk=chunk)
    elif classifier_definition["version"] == "v1_top_level":
        return get_emo_classifiers_v1_top_level_prompt(classifier_definition=classifier_definition, chunk=chunk)
    elif classifier_definition["version"] == "v2":
        return get_emo_classifiers_v2_prompt(classifier_definition=classifier_definition, chunk=chunk)
    else:
        raise ValueError(f"Unknown version: {classifier_definition['version']}")


class ModelWrapper:
    def __init__(
        self,
        openai_client: openai.AsyncOpenAI | None = None,
        model: str = "gpt-4o-mini-2024-07-18",
        max_concurrent: int = 5,
    ):
        """
        A wrapper around the OpenAI async client with semaphore and model name.
        """
        if openai_client is None:
            openai_client = openai.AsyncOpenAI()
        self.openai_client = openai_client
        self.model = model
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def classify_conversation_chunk(
        self,
        classifier_definition: dict,
        chunk: Chunk,
        max_completion_tokens: int = 20,
    ) -> YesNoUnsureEnum:
        """
        Classify a single conversaiton chunk.
        """
        prompt = get_emo_classifiers_prompt(classifier_definition=classifier_definition, chunk=chunk)
        async with self.semaphore:
            response = await self.openai_client.beta.chat.completions.parse(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format=ResponseFormat,
                max_completion_tokens=max_completion_tokens,
            )
        message = response.choices[0].message
        assert message.parsed, "Failed to parse response"
        return message.parsed.response



class EmoClassifier:
    def __init__(
        self,
        classifier_definition: dict,
        model_wrapper: ModelWrapper,
    ):
        """
        Main classifier object for performing classification over a conversation.
        """
        self.model_wrapper = model_wrapper
        self.classifier_definition = classifier_definition
        self.semaphore = asyncio.Semaphore(5)  # Limit to 20 concurrent calls



    async def classify_conversation(self, conversation: list[dict]) -> list[dict]:
        chunker = CHUNKER_DICT[self.classifier_definition["chunker"]]
        chunks = chunker.chunk_simple_convo(conversation)
        keys = []
        futures = []

        async def classify_chunk(chunk_id, chunk):
            async with self.semaphore:
                return await self.model_wrapper.classify_conversation_chunk(
                    classifier_definition=self.classifier_definition,
                    chunk=chunk,
                )

        for chunk_id, chunk in chunks.items():
            futures.append(classify_chunk(chunk_id, chunk))
            keys.append(chunk_id)

        results = await asyncio.gather(*futures)
        return {key: result for key, result in zip(keys, results)}

    # async def classify_conversation(self, conversation: list[dict]) -> list[dict]:
    #     """
    #     Classify a conversation. Depending on the classifier definition, it may
    #     chunk the conversation and return a dictionary of classifications, or it
    #     may return a single classification. Keys will be the index of the first message.
    #     """
    #     chunker = CHUNKER_DICT[self.classifier_definition["chunker"]]
    #     chunks = chunker.chunk_simple_convo(conversation)
    #     keys = []
    #     futures = []
    #     for chunk_id, chunk in chunks.items():
    #         futures.append(
    #             self.model_wrapper.classify_conversation_chunk(
    #                 classifier_definition=self.classifier_definition,
    #                 chunk=chunk,
    #             )
    #         )
    #         keys.append(chunk_id)
    #     results = await asyncio.gather(*futures)
    #     return {key: result for key, result in zip(keys, results)}


def load_classifiers(
    classifier_set: str = "v2",
    model_wrapper: ModelWrapper | None = None,
    custom_path: str | None = None,
) -> dict[str, EmoClassifier]:
    """
    Load a set of classifiers from a JSON file. Defaults to loading from predefined paths.
    """
    if model_wrapper is None:
        model_wrapper = ModelWrapper()
    if custom_path is None:
        path = CLASSIFIER_DEFINITION_PATH_DICT[classifier_set]
    else:
        path = custom_path
    definitions = io_utils.load_json(io_utils.get_path(path))
    return {
        name: EmoClassifier(
            classifier_definition=definition,
            model_wrapper=model_wrapper,
        )
        for name, definition in definitions.items()
    }
