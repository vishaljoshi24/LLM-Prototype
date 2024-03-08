import llm
from openai.error import RateLimitError


# Code used to send a prompt to ChatGPT. Requires a model key, likely to be unused for the prototype.
def gpt35call(prompt):
    model = llm.get_model("gpt-3.5-turbo")
    model.key = 'MODEL KEY HERE'
    try:
        gpt_response = model.prompt(prompt)
        response = gpt_response.text()
    except RateLimitError:
        response = "OpenAI API Rate Limit Error"
    return response
