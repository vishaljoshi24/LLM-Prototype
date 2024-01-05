import streamlit as st
import random
import PersonaList
import llama2local

# App title
st.set_page_config(page_title="Persona Chatbot")

# Persona Gen
if "rn" not in st.session_state:
    st.session_state["rn"] = random.randint(0, len(PersonaList.personas))

if "persona" not in st.session_state:
    st.session_state["persona"] = PersonaList.personas[st.session_state["rn"]]

# Replicate Credentials
with st.sidebar:
    st.title('Persona Chatbot')

    # Refactored from https://github.com/a16z-infra/llama2-chatbot
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')

    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "Persona", "content": "Hello!", "avatar": "🤖"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "Persona", "content": "Hello!", "avatar": "🤖"}]


st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


def rate_persona():
    pass


st.sidebar.button('Rate this persona', on_click=rate_persona)


# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = f"""
[INST] <<SYS>>
Your persona '{st.session_state["persona"]}'.
<</SYS>>
Current conversation:
"""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Persona: " + dict_message["content"] + "\n\n"
    output = llama2local.model_call(selected_model, f"{string_dialogue} {prompt_input} Persona: [/INST]", temperature,
                                    top_p, max_length)
    return output


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from Persona
if st.session_state.messages[-1]["role"] != "Persona":
    with st.chat_message("Persona", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "Persona", "content": full_response}
    st.session_state.messages.append(message)
