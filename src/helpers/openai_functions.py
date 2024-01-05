import openai
import tiktoken

from .prompts import chunking_prompt

def query_chatGPT(
    prompt=None,
    text_data=None,
    openai_api_key = None,
    chat_model="gpt-3.5-turbo",
    model_token_limit=8192,
    max_tokens=2500,
):
    """
    Generic function that can take a prompt to direct ChatGPT to process a query in a particular way. The function also sends additional text data to ChatGPT.
    The text data is chunked into maximum number of tokens and send piecewise to ChatGPT. The overall contextual memory of all the chunks is mantianed by using
    ChatGPT's conversational Chat model and not a simple 'create' query.

    Input:
        prompt: -string. Main prompt on which ChatGPT acts and generates response according to it.
        text_data: -string. Complete text of a single text file.
        openai_api_key: -string. API key from ChatGPT to enable using ChatGPT.

        chat_model: -string. Name of the defined Chat Models from OpenAI.
        model_token_limit: -int. The overall token limit from ChatGPT for the 3.5 turbo model.
        max_tokens: -int. Number of tokens in an individual chunk of text that will be sent to ChatGPT.

    Return: String. The response from ChatGPT as per the given prompt. The response can be a summary or can be action item table based on the 'prompt' that was used in input.
    """

    # Check if the necessary arguments are provided
    if not prompt:
        return "Error: Prompt is missing. Please provide some prompt to generate responses from."
    if not text_data:
        return "Error: Text data is missing. Please provide some text data."
    if openai_api_key is None:
        return "Error: OpenAI API key not found. Please add the key in environment variables."
    openai.api_key = openai_api_key

    # Initialize the tokenizer
    tokenizer = tiktoken.encoding_for_model(chat_model)

    # Encode the text_data into token integers
    token_integers = tokenizer.encode(text_data)

    # Split the token integers into chunks based on max_tokens
    chunk_size = max_tokens - len(tokenizer.encode(prompt))
    chunks = [
        token_integers[i : i + chunk_size]
        for i in range(0, len(token_integers), chunk_size)
    ]

    # Decode token chunks back to strings
    chunks = [tokenizer.decode(chunk) for chunk in chunks]

    messages = [
        {"role": "user", "content": prompt},
        {
            "role": "user",
            "content": chunking_prompt,
        },
    ]
    for chunk in chunks:
        messages.append({"role": "user", "content": chunk})

        # Check if total tokens exceed the model's limit and remove oldest chunks if necessary
        while (
            sum(len(tokenizer.encode(msg["content"])) for msg in messages)
            > model_token_limit
        ):
            messages.pop(1)  # Remove the oldest chunk... Not the latest (newest) chunk.

        response = openai.ChatCompletion.create(model=chat_model, messages=messages)
        
    # Add the final "ALL PARTS SENT" message
    messages.append({"role": "user", "content": "ALL PARTS SENT"})
    response = openai.ChatCompletion.create(model=chat_model, messages=messages)
    final_response = response.choices[0].message["content"].strip()
    
    return final_response