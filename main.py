# TODO make a function to input data into chatgpt FINISHED
# TODO also make a prompt so that I can fetch data from a image generator
# TODO make a GUI
# TODO redesign the prompt
import os
import openai
import sys

openai.api_key = ""


def write_read_mem(option, *token):  # write or read token from token file
    if option:
        file = open(sys.path[0] + "/memory.mem", "w")
        file.write(token)
        file.close()
        return 0
    else:
        file = open(sys.path[0] + "/memory.mem", "r")
        token = file.read()
        file.close()
        return token


with open("OPENAI_API_KEY", "r") as f:
    openai.api_key = f.read()


def remove_newline(_response):
    res = ""
    for i in _response:
        if i == "\n":
            continue

        res = res + res.join(i)
    return res


_start_sequence = " Pekora: "
_restart_sequence = " Mike: "

prompt = write_read_mem(False)

temp_fix = False

while True:

    user_input = input("Mike: ")
    if user_input in "!BREAK":
        break
    if user_input in "!SAVE":
        prompt = prompt + response + _restart_sequence
        write_read_mem(True, prompt)
    # print(f"[DEBUG] raw user input: {user_input}")
    user_input = _restart_sequence + user_input

    try:
        prompt = prompt + response + _restart_sequence + user_input + _start_sequence
    except NameError:
        # print("[ERROR] we got a NameError")
        prompt = prompt + user_input + _start_sequence
        temp_fix = True

    # print(prompt)

    # print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=50,
        top_p=1,
        frequency_penalty=1.01,
        presence_penalty=1.03,
        stop=_restart_sequence
    )

    # print(f"[DEBUG] RAW RESPONSE: {response}")
    response = response.choices[0].text
    # print(f"[DEBUG] RAW TEXT RESPONSE:{response}")
    response = remove_newline(response)

    print("Pekora: " + response)
