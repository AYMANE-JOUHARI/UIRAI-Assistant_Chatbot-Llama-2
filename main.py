from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from gtts import gTTS  # new import
from io import BytesIO 
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *

import os

os.environ["TOGETHER_API_KEY"] = "TOGETHER_API_KEY"
import together

# set your API key
together.api_key = os.environ["TOGETHER_API_KEY"]


import together

import logging
from typing import Any, Dict, List, Mapping, Optional

from pydantic import Extra, Field, root_validator

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env

class TogetherLLM(LLM):
    """Together large language models."""

    model: str = "togethercomputer/llama-2-70b-chat"
    """model endpoint to use"""

    together_api_key: str = os.environ["TOGETHER_API_KEY"]
    """Together API key"""

    temperature: float = 0.7
    """What sampling temperature to use."""

    max_tokens: int = 512
    """The maximum number of tokens to generate in the completion."""

    class Config:
        extra = Extra.forbid

    @root_validator(allow_reuse=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(
            values, "together_api_key", "TOGETHER_API_KEY"
        )
        values["together_api_key"] = api_key
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(prompt,
                                          model=self.model,
                                          max_tokens=self.max_tokens,
                                          temperature=self.temperature,
                                          )
        text = output['output']['choices'][0]['text']
        return text
    
llm = TogetherLLM(
    model= "togethercomputer/llama-2-70b-chat",
    
)    

def query_refiner1(conversation,query):
   llm=together.Complete.create( model= "togethercomputer/llama-2-70b-chat",
    temperature=0.3, prompt=f"<<SYS>>Given the following user query and conversation log, formulate a question in the user's language only that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\n<</SYS>>",top_p=1)
   
   response=llm
   return response['output']['choices'][0]['text']

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
hide_streamlit_style1 = """
<style>
audio::-webkit-media-controls-panel,
audio::-webkit-media-controls-enclosure {
    background-color:#073567;}

audio::-webkit-media-controls-time-remaining-display,
audio::-webkit-media-controls-current-time-display {
    color: white;
    text-shadow: none; 

}
audio::-webkit-media-controls-current-time-display {
    max-width: 20%;
    max-height: 20px;
}

audio::-webkit-media-controls-timeline {
  background-color: #073567;
  border-radius: 25px;
  margin-left: 10px;
  margin-right: 10px;
}
</style>

"""
st.set_page_config(page_title='uAIr', page_icon="https://i.imgur.com/IqRhThR.png")
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("https://i.imgur.com/IqRhThR.png", width=300 )
   
def text_to_speech(text):
    """
    Converts text to an audio file using gTTS and returns the audio file as binary data
    """
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang="fr")
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Bonjour, je m'appelle UIRAi. Comment puis-je vous aider aujourd'hui ?"]
    
    

if 'requests' not in st.session_state:
    st.session_state['requests'] = []


if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""<<SYS>> You are a very friendly AI bot working for Université Internationale de Rabat . Your name is UAIR, and you're just 2 months old.Remember that the user is a futur student of the university your working with ,Your creators are Marouane Benbrahim and Ayman Jouhari. Always answer questions in the user's language and only using the provided context. If the answer is not contained within the context below and it seems related to the university redirect the user without adding nothing to the university's website, which is www.uir.ac.ma. If The question is completely off-topic in relation to the university say that its not you job to answer that.""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="<</SYS>>[INST]{input}[/INST]")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)



# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()


with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            # st.code(conversation_string)
            refined_query = query_refiner1(conversation_string,query)
            #refined_query = query
            st.subheader("Refined Query:")
            st.write(refined_query)
            context = find_match(refined_query)
            print(context)  
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response) 
        
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            st.markdown(hide_streamlit_style1, unsafe_allow_html=True) 
            st.audio(text_to_speech(st.session_state['responses'][i]), format="audio/wav")
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

          