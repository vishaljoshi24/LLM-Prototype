from llama_cpp import Llama
#import ChatGPT


# Load Llama 2 model
def model_call(model, prompt, temperature, top_p, top_k, repetition, max_length):
    if model == 'LLaMa2-7B-Chat':
        # Change the gguf if different quantisation used
        model_path = "files/models/llama-2-7b-chat.Q8_0.gguf"
    elif model == 'LLaMa2-13B-Chat':
        # Change the gguf if different quantisation used
        model_path = "files/models/llama-2-13b-chat.Q8_0.gguf"
    # Uncomment below lines for ChatGPT implementation
    # else:
        # return ChatGPT.GPT35Call(prompt)

    # Needs updating for LangChain
    llm = Llama(model_path)

    output = llm(prompt,
                 echo=False,
                 temperature=temperature,
                 top_p=top_p,
                 top_k=top_k,
                 repeat_penalty=repetition,
                 max_tokens=max_length)

    # Solely for bug-fixing, can be removed if desired
    with open("response.txt", "w") as f:
        f.write(str(output))

    # Update for langchain
    return output['choices'][0]['text']
