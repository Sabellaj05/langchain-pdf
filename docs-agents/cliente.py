from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/agent/")

remote_chain.invoke({
    "input": "Explain to me how to play Mahjong Riichi in 4 sentences",
    "chat_history": []  # Providing an empty list as this is the first call
})


