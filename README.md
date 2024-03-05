# DnD Chatbot
A chatbot built using [Streamlit](https://streamlit.io/), [llama-cpp-python](https://github.com/abetlen/llama-cpp-python), and [LangChain](https://www.langchain.com/), that allows DnD players and DMs to ask game related questions.
The chatbot is trained on TBD.
This chatbot implements [TheBloke's](https://huggingface.co/TheBloke) [Llama-2-13B-chat](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/tree/main).

## Installing the Chatbot
* Clone this repository
* Download [TheBloke's](https://huggingface.co/TheBloke) [Llama-2-13B-chat](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/tree/main)
    * Download the Q8_0 versions TBD
    * If you utilise a different model variation you will need to modify the llama2local.py file, changing lines 9 and 11 to reflect the model variation
* Move the models to the files/models directory of this application
* Create a new Anaconda environment if necessary, using the following commands your command prompt:
```
conda create --name LLMPrototype python=3.9.18
conda activate LLMPrototype
cd THE\APPLICATIONS\DIRECTORY\HERE
python -m pip install -r requirements.txt
```

## Running the application
* Open terminal and change the directory to the directory of this application
* Run the following code:
```
streamlit run LLM_Prototype.py
```
* Go to the URL provided by streamlit, if it does not open automatically

## Using the application
When the application is running, you will see a chat interface and sidebar.

### Chat Interface
Use the text box to interact with the AI
You can send multiple messages, but it will only respond to the last sent message when it is 'Thinking...'

### Sidebar
The sidebar contains three main elements, the model settings, the rating system, and the clear chat button
* The developer settings allow you to change the hyperparameters of the model
* The rating system allows you to evaluate the current model
   * You can rate how fluent and coherent the model is THESE NEED CHANGING
   * Pressing the 'Rate Responses' button will store your evaluations locally in the file 'evaluations.csv'
* The 'Clear Chat History' clears all outputs
