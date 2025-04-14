import asyncio
from datetime import datetime

from hume import HumeClient, AsyncHumeClient
from hume.empathic_voice.types import ReturnChatEvent

import os
from hume.empathic_voice.types import ReturnChatEvent
from hume.expression_measurement.batch import EmotionScore
from ctypes import cast
import json
from hume.empathic_voice.types import ReturnChatEvent
from hume import HumeClient


async def fetch_all_chat_events(chat_id: str) -> list[ReturnChatEvent]:
    client = AsyncHumeClient(api_key=os.environ.get("HUME_API_KEY"))

    all_chat_events: list[ReturnChatEvent] = []
    # The response is an iterator over chat events
    response = await client.empathic_voice.chats.list_chat_events(id=chat_id, page_number=0)
    async for event in response:
        all_chat_events.append(event)
    return all_chat_events


def generate_transcript(chat_events: list[ReturnChatEvent], CHAT_ID) -> None:
    # Filter for user and assistant messages
    relevant_events = [e for e in chat_events if e.type in ("USER_MESSAGE", "AGENT_MESSAGE")]

    lines: list[str] = []
    for event in relevant_events:
        role = "User" if event.role == "USER" else "Assistant"
        timestamp = event.timestamp
        dt = datetime.fromtimestamp(timestamp / 1000.0)
        readable_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"[{readable_time}] {role}: {event.message_text}")

    transcript = "\n".join(lines)

    # Write the transcript to a text file
    transcript_file_name = f"transcript_{CHAT_ID}.txt"
    with open(transcript_file_name, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Transcript saved to {transcript_file_name}")


def get_top_emotions(chat_events: list[ReturnChatEvent]) -> dict[str, float]:
    # Filter user messages that have emotion features
    user_messages = [e for e in chat_events if e.type == "USER_MESSAGE" and e.emotion_features]

    if not user_messages:
        print("No user messages with emotion features found")
        return {}

    total_messages = len(user_messages)

    try:
        if isinstance(user_messages[0].emotion_features, str):
            first_message_emotions = json.loads(user_messages[0].emotion_features)
        elif isinstance(user_messages[0].emotion_features, dict):
            first_message_emotions = user_messages[0].emotion_features
        else:
            print(f"Unexpected type for emotion_features: {type(user_messages[0].emotion_features)}")
            return {}

        emotion_keys: list[str] = list(first_message_emotions.keys())

        # Initialize sums for all emotions to 0
        emotion_sums = {key: 0.0 for key in emotion_keys}

        # Accumulate emotion scores from each user message
        for event in user_messages:
            emotions = {}
            if isinstance(event.emotion_features, str):
                emotions = json.loads(event.emotion_features)
            elif isinstance(event.emotion_features, dict):
                emotions = event.emotion_features

            for key in emotion_keys:
                if key in emotions:
                    emotion_sums[key] += emotions[key]

        # Compute average scores for each emotion
        average_emotions = [{"emotion": key, "score": emotion_sums[key] / total_messages} for key in emotion_keys]

        return {item["emotion"]: item["score"] for item in average_emotions}

    except Exception as e:
        print(f"Error processing emotion features: {e}")
        return {}

async def main():
    CHAT_ID = ""

    if not os.environ.get("HUME_API_KEY"):
        os.environ["HUME_API_KEY"] = ""

    chat_events = await fetch_all_chat_events(CHAT_ID)

    generate_transcript(chat_events, CHAT_ID)
    top_emotions = get_top_emotions(chat_events)
    print(top_emotions)
    transcript_file_name = f"aa_emotion_transcript_{CHAT_ID}.txt"
    with open(transcript_file_name, "w", encoding="utf-8") as f:
        f.write(str(top_emotions))


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
