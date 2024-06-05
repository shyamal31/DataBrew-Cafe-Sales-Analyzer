import streamlit as st
import random
import time
import model_test

# message = st.chat_message("assistant")
# message.write("hello how can I help you?")

# prompt = st.chat_input("Say something here")
# if prompt:
#     st.write(f'User has sent the following prompt: {prompt}')



st.title("MarketingGPT")

#streamed response emulator
# def response_generator():
#     response = random.choice(
#         [
#             "Hello there! How can I help you?",
#             "Hi, human ! Is there anything that I can help you with?",
#             "Do you need help?"
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.1)

#Custom streamed response

def response_generator(prompt):
    llm = model_test.cntopenai()
    db = model_test.cntdb()

    model = model_test.own_data(db, llm)

    response1, response2 = model.prtext_query(prompt)
    for word in response1.content.split():
        yield word + " "
        time.sleep(0.2)
    st.write("The above response was made by using following SQL query: ")
    # for word in response2.split():
    #     yield word + " "
    #     time.sleep(0.5)
    st.code(body = response2, language="SQL")

#initialize chat history


if "messages" not in st.session_state:
    st.session_state.messages = []

#display chat messages from histroy
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

if prompt := st.chat_input("Type Here"): #:= assisgns as the left side value and check for potential null
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({'role':'user', 'content':prompt})

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
        
    st.session_state.messages.append({'role':'user', 'content':response})


