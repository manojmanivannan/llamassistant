import streamlit as st
from tools.chatGeneration import call_ai

with st.sidebar:
    st.write("Model Parameters")
    model_endpoint = st.text_input("Model endpoint", "http://localhost:11434", key="chatbot_model_endpoint")
    model_name = st.text_input("Model name", "llama3:8b-instruct-q8_0", key="chatbot_model_name")


def get_chat_response(prompt):
    print(f"Prompt: {prompt}")
    with st.spinner("Thinking..."):
        response = call_ai(prompt,model_endpoint, model_name)
    # print(response)
    # print('reformatting')
    if isinstance(response,list) and len(response)==1:
        return repr(response[0][0])
    elif isinstance(response,list) and len(response) >1:
        return '\n'.join([''.join(repr(s[0])) for s in response])

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by llama3")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = get_chat_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)