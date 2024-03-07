import streamlit as st
import llama2local
import evaluation
from datetime import datetime
import os

# Uncomment for star ratings
# from streamlit_star_rating import st_star_rating

# App title
st.set_page_config(page_title="DnD LLM Prototype")
if not os.path.isdir('files/chatlogs'):
    os.mkdir('files/chatlogs')

if "show_advanced" not in st.session_state:
    st.session_state["show_advanced"] = False

if "chatlog_file" not in st.session_state:
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H%M%S")
    st.session_state["chatlog_file"] = str(dt_string)


def advanced_change():
    st.session_state["show_advanced"] = not st.session_state["show_advanced"]


# Replicate Credentials
with st.sidebar:
    st.title('DnD LLM Prototype')
    st.sidebar.button('Developer Settings', on_click=advanced_change)
    if st.session_state["show_advanced"]:
        st.subheader('Parameters')
        selected_model = st.sidebar.selectbox('Choose a Large Language Model',
                                              ['LLaMa2-7B-Chat', 'LLaMa2-13B-Chat', 'GPT-3.5-turbo-1106'],
                                              key='selected_model')
        temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.72, step=0.01,
                                        disabled=(selected_model == "GPT-3.5-turbo-1106"))
        top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.73, step=0.01,
                                  disabled=(selected_model == "GPT-3.5-turbo-1106"))
        top_k = st.sidebar.slider('top_k', min_value=0, max_value=100, value=0, step=1,
                                  disabled=(selected_model == "GPT-3.5-turbo-1106"))
        repetition = st.sidebar.slider('repetition_penalty', min_value=0.0, max_value=2.0, value=1.1, step=0.01,
                                       disabled=(selected_model == "GPT-3.5-turbo-1106"))
        max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8,
                                       disabled=(selected_model == "GPT-3.5-turbo-1106"))
    else:
        selected_model = 'LLaMa2-7B-Chat'
        temperature = 0.72
        top_p = 0.73
        top_k = 0
        repetition = 1.1
        max_length = 512

    st.markdown('----')
    st.write("**Rate the Conversation**")
    theme = st.radio("What is the conversation's general theme?",
                     ["Content Generation", "Rules Clarification", "Combat Help", 'Other'],
                     index=None, )

    # Uncomment below code for star ratings instead
    # coherency = st_star_rating('Coherency (does the response match the input)', maxValue=5,
    # defaultValue=2.5, key="coherency")
    # fluency = st_star_rating('Fluency (how natural is the conversation)', maxValue=5,
    # defaultValue=2.5, key="fluency")
    coherency = st.slider('Coherency (does the response match the input)', min_value=0, max_value=10,
                          value=5, step=1)
    fluency = st.slider('Fluency (how natural is the conversation)', min_value=0, max_value=10, value=5, step=1)
    st.sidebar.button(label='Rate Conversation',
                      on_click=evaluation.submit_rating,
                      args=(st.session_state["chatlog_file"], selected_model, temperature, top_p, top_k,
                            repetition, max_length, theme, coherency, fluency))
    st.markdown('----')


def clear_chat_history():
    st.session_state.messages = [{"role": "Chatbot", "content": "Hello!", "avatar": "⚔️"}]
    del st.session_state["chatlog_file"]


st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "Chatbot", "content": "Hello!", "avatar": "⚔️"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.write(message["content"])


# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    # The Prompt for the chatbot
    string_dialogue = f"""
[INST] <<SYS>>
You are a DnD assistant tool.
<</SYS>>
Current conversation:
"""
    # The chat history for the chatbot
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Chatbot: " + dict_message["content"] + "\n\n"

    # Generate the output based on history and prompt
    output = llama2local.model_call(selected_model, f"{string_dialogue} {prompt_input} Chatbot: [/INST]", temperature,
                                    top_p, top_k, repetition, max_length)

    return output


# User-provided prompt
if prompt := st.chat_input("Message the Chatbot"):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧝‍♂️"})
    with st.chat_message("user", avatar="🧝‍♂️"):
        st.write(prompt)
    try:
        file = open('files/chatlogs/' + st.session_state["chatlog_file"] + ".txt", 'a+')
        file.write("User: " + prompt + "\n")
        file.close()
    except IOError:
        file = open('files/chatlogs/' + st.session_state["chatlog_file"] + ".txt", 'w+')
        file.write("User: " + prompt + "\n")
        file.close()

# Generate a new response if last message is not from Chatbot
if st.session_state.messages[-1]["role"] != "Chatbot":
    with st.chat_message("Chatbot", avatar="⚔️"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "Chatbot", "content": full_response, "avatar": "⚔️"}
    st.session_state.messages.append(message)
    try:
        file = open('files/chatlogs/' + st.session_state["chatlog_file"] + ".txt", 'a')
        file.write(message["role"] + ": " + message["content"] + "\n")
        file.close()
    except IOError:
        file = open('files/chatlogs/' + st.session_state["chatlog_file"] + ".txt", 'w')
        file.write(message["role"] + ": " + message["content"] + "\n")
        file.close()
