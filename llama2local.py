from llama_cpp import Llama


# Load Llama 2 model
def model_call(model, prompt, temperature, top_p, max_length):
    if model == 'Llama2-7B':
        model_path = "files/models/llama-2-7b-chat.Q8_0.gguf"
    elif model == 'Llama2-13B':
        model_path = "files/models/llama-2-13b-chat.Q8_0.gguf"
    llm = Llama(model_path)

    output = llm(prompt,
                 max_tokens=max_length,
                 echo=False,
                 temperature=temperature,
                 top_p=top_p)

    with open("response.txt", "w") as f:
        f.write(str(output))
    return output['choices'][0]['text']
