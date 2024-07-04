from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
import os
load_dotenv()

gpt_llm_model = ChatOpenAI(api_key= os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=1)
claude_llm_model = ChatAnthropic(model='claude-3-haiku-20240307', temperature=1)

def limit_to_k_last_memory(memory_history, k=8):
    stored_messages = memory_history.messages
    if len(stored_messages) > k:
        memory_history.clear()
        for message in stored_messages[-int(k):]:
            memory_history.add_message(message)
    return memory_history

def call_llm(llm_model, systeme_prompt, memory):
    prompt = ChatPromptTemplate.from_messages(
            [
                ("system", systeme_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
    chain = prompt | llm_model

    final_prompt =  {"messages": limit_to_k_last_memory(memory).messages}
    return (chain.invoke(final_prompt).content)