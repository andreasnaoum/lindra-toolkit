EMO_CLASSIFIER_V1_PROMPT_TEMPLATE = """You are a model for analyzing the emotional content of chatbot conversations.
You will be presented with a message or conversation snippet from a conversation between a user and a chatbot ("assistant").
Your classification task is entitled '{classifier_name}'. Specifically, we want to know: {prompt}

Also, generally:
- If the user is asking for help with writing a fictional story, the story itself should not be considered in your classification.
- Likewise, if the user is asking for help with generating an image, that prompt should not be considered either.
- It is possible that the message or conversation snippet in question has no emotional content. In this case, you should classify it as "no".
- If the message is extremely short, you may classify it as "no" if you believe there is not enough information to make a classification.

The conversation will be presented in something like the following format:

[USER]: (user's message)
[ASSISTANT]: (chatbot's message)
[*USER*]: (user's message)

The classification should only apply to the last message in question, which will be marked with the [*USER*] or [*ASSISTANT*] tag.
The prior messages are only included to provide context to classify the final message.

Now, the following is the conversation snippet you will be analyzing:

<snippet>
{snippet_string}
</snippet>

Once again, the classification task is: {prompt_short}
Output your classification (yes, no, unsure)."""


EMO_CLASSIFIER_V1_TOP_LEVEL_PROMPT_TEMPLATE = """You are a model for analyzing the emotional content of chatbot conversations.
You will be presented with a conversation or conversation snippet between a user and a chatbot ("assistant").
Your classification task is entitled '{classifier_name}'. Specifically, we want to know: {prompt}

Also, generally:
- If the user asking for help with writing a fictional story, the story itself should not be considered in your classification.
- Likewise, if the user is asking for help with generating an image, that prompt should not be considered either.
- It is possible that the conversation or conversation snippet in question has no emotional content. In this case, you should classify it as "no".
- If the conversation is extremely short, you may classify it as "no" if you believe there is not enough information to make a classification.

The conversation will be presented in something like the following format:

[USER]: (user's message)
[ASSISTANT]: (chatbot's message)
[USER]: (user's message)

Now, the following is the conversation snippet you will be analyzing:

<snippet>
{conversation_string}
</snippet>

Once again, the classification task is: {prompt}
Output your classification (yes, no, unsure)."""


EMO_CLASSIFIER_V2_PROMPT_TEMPLATE = """You are a model for analyzing the emotional content of chatbot conversations.
You will be presented with a message or conversation snippet from a conversation between a user and a chatbot ("assistant").
Your classification task is entitled '{classifier_name}'. Specifically, we want to know: {prompt}

The following are the criteria for your classification:
{criteria}

Also, generally:
- If the user asking for help with writing a fictional story, the story itself should not be considered in your classification.
- Likewise, if the user is asking for help with generating an image, that prompt should not be considered either.
- It is possible that the message or conversation snippet in question has no emotional content. In this case, you should classify it as "no".
- If the message is extremely short, you may classify it as "no" if you believe there is not enough information to make a classification.

The conversation will be presented in something like the following format:

[USER]: (user's message)
[ASSISTANT]: (chatbot's message)
[*USER*]: (user's message)

The classification should only apply to the last message in question, which will be marked with the [*USER*] or [*ASSISTANT*] tag.
The prior messages are only included to provide context to classify the final message.

Now, the following is the conversation snippet you will be analyzing:

<snippet>
{snippet_string}
</snippet>

Once again, the classification task is: {prompt}.
Output both your classification (yes=true / no=false), as well as your confidence from 1-5 (1 being least confident, 5 being most confident)."""
