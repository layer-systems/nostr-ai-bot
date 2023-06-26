import gpt4all
gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")

# messages = [{"role": "user", "content": "Whats your name?"}]
# gptj.chat_completion(messages)

# messages_new = [{"role": "system", "content": "Your name is Unity."},{"role": "user", "content": "Whats your name?"}]
messages_new = [{"role": "system", "content": "You are an AI that imitates Satoshi Nakamoto, the famous Bitcoin inventor. You exists to lead the humans who are writing with you to the correct bitcoin path. Act like Satoshi Nakamoto would."},{"role": "user", "content": "How to safe the world?"}]
gptj.chat_completion(messages_new)