import streamlit as st
import ollama


if 'messages' not in st.session_state:
	st.session_state.messages = []

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

if prompt := st.chat_input("What can I help you with?"):
	st.session_state.messages.append({"role": "user", "content": prompt})

	with st.chat_message("user"):
		st.write(prompt)

	with st.chat_message("assistant"):
		response = ollama.chat(model='gemma2',
			messages=[
				{"role": m["role"], "content": m["content"]}
					for m in st.session_state.messages
			],
			stream=True)

		response_content = ''
		def catch_response(response):
			global response_content
			for chunk in response:
				response_content += chunk['message']['content']
				yield chunk['message']['content']

		stream = catch_response(response)
		st.write_stream(stream)
		
		st.session_state.messages.append({"role": "assistant", "content": response_content})
