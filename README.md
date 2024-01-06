# Persona Chat
A chatbot built using [Streamlit](https://streamlit.io/), [llama-cpp-python](https://github.com/abetlen/llama-cpp-python), and [LLM](https://llm.datasette.io/en/stable/), that creates personas for users to interact with.
This chatbot implements [TheBloke's](https://huggingface.co/TheBloke) [Llama-2-7B-chat](https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF/tree/main) and [Llama-2-13B-chat](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/tree/main), as well as OpenAI's [Gpt-3.5-turbo-1106](https://chat.openai.com/).
The personas implemented are from the [PersonaChat dataset](https://www.kaggle.com/datasets/atharvjairath/personachat).
The UI was refactored from [a16z's implementation](https://github.com/a16z-infra/llama2-chatbot) of their [LLaMA2 Chatbot](https://www.llama2.ai/).

## Installing the Chatbot
* Clone this repository
* Download [TheBloke's](https://huggingface.co/TheBloke) [Llama-2-7B-chat](https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF/tree/main) and [Llama-2-13B-chat](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/tree/main)
    * Download the Q8_0 versions
    * If you utilise a different model variation you will need to modify the llama2local.py file, changing lines 9 and 11 to reflect the model variation
* Move the models to the files/models directory of this application
* Create a new Anaconda environment if necessary, using the following commands your command prompt:
```
conda create --name PersonaChat python=3.9.18
conda activate PersonaChat
cd THE\APPLICATIONS\DIRECTORY\HERE
python -m pip install -r requirements.txt
```

## Running the application
* Open terminal and change the directory to the directory of this application
* Run the following code:
```
streamlit run Persona_Chat.py
```
* Go to the URL provided by streamlit, if it does not open automatically

## Using the application
When the application is running, you will see a chat interface and sidebar.

### Chat Interface
Use the text box to interact with the AI
You can send multiple messages, but it will only respond to the last sent message when it is 'Thinking...'

### Sidebar
The sidebar contains three main elements, the model settings, the rating system, and the clear chat button
* The model settings allows you to change the selected model, change the hyperparameters of the model, and toggle further hyperparameters
    * The model dropdown list allows you to choose which model to use, the chat history is not affected and will be read by the new model
    * The basic settings allow you to change the temperature and top_p of the model
    * Toggling the advanced settings also allows you to change the top_k, repetition penalty, and max token length of the model
* The rating system allows you to evaluate the current model
   * You can select which persona you feel the model is representing, one of the options is the model's current persona
   * You can rate how fluent and coherent the model is
   * Pressing the 'Rate Persona' button will store your evaluations locally in the file 'evaluations.csv'
* The 'Clear Chat History and Change Persona' button performs the said task, by clearing all outputs and randomly selecting a new persona