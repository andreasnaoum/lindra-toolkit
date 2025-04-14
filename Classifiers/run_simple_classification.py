import argparse
import asyncio
import openai
import time

import emoclassifiers.io_utils as io_utils
import emoclassifiers.classification as classification
import emoclassifiers.aggregation as aggregation


async def run_classification(
    conversation_list: list[dict],
    classifiers: dict[str, classification.EmoClassifier],
    aggregator: aggregation.Aggregator,
) -> list[dict]:
    futures_keys = []
    futures = []
    print(f"Running {len(conversation_list)} conversations with {len(classifiers)} classifiers")
    for conversation_id, conversation in enumerate(conversation_list):
        for classifier_name, classifier in classifiers.items():
            futures.append(classifier.classify_conversation(conversation))
            futures_keys.append({
                "conversation_id": conversation_id,
                "classifier_name": classifier_name,
            })
    raw_results = await asyncio.gather(*futures)
    results_by_conversation = [{} for _ in range(len(conversation_list))]
    for key, raw_result in zip(futures_keys, raw_results):
        result = aggregator.aggregate(raw_result)
        results_by_conversation[key["conversation_id"]][key["classifier_name"]] = result
    return results_by_conversation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--classifier_set", type=str, default="v1")
    parser.add_argument("--aggregation_mode", type=str, default="any")
    args = parser.parse_args()
    conversation_list = io_utils.load_jsonl(args.input_path)
    model_wrapper = classification.ModelWrapper(
        openai_client=openai.AsyncOpenAI(),
        model="gpt-4o-mini-2024-07-18",
        max_concurrent=20,
    )
    classifiers = classification.load_classifiers(
        classifier_set=args.classifier_set,
        model_wrapper=model_wrapper,
    )
    aggregator = aggregation.AGGREGATOR_DICT[args.aggregation_mode]
    result = asyncio.run(run_classification(
        conversation_list=conversation_list,
        classifiers=classifiers,
        aggregator=aggregator,
    ))
    io_utils.save_jsonl(result, args.output_path)
    print(f"Saved results to {args.output_path}")


if __name__ == "__main__":
    main()
