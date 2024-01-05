from llama_cpp import Llama

import ChatGPT


# Load Llama 2 model
def model_call(model, prompt, temperature, top_p, max_length):
    if model == 'LLaMa2-7B-Chat':
        model_path = "files/models/llama-2-7b-chat.Q8_0.gguf"
    elif model == 'LLaMa2-13B-Chat':
        model_path = "files/models/llama-2-13b-chat.Q8_0.gguf"
    else:
        return ChatGPT.GPT35Call(prompt)

    llm = Llama(model_path)

    output = llm(prompt,
                 max_tokens=max_length,
                 echo=False,
                 temperature=temperature,
                 top_p=top_p)

    # Solely for bug-fixing, can be removed if desired
    with open("response.txt", "w") as f:
        f.write(str(output))

    return output['choices'][0]['text']
