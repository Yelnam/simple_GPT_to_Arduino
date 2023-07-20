import serial.tools.list_ports
import time
import openai
import pandas as pd
import string
from PIL import ImageColor

openai.api_key = openaikey

table_color = pd.read_excel('C:/Users/rober/Desktop/Coding_Data/0 - GitHub/Python to Arduino - NOT YET COMMITTED/Color_Table.xlsx')

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0,len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

messages = [
    {"role": "system", "content": "you are to play the role of an artist who is very friendly and just likes choosing colours! you also like to be very concise"}
]

while True:

    message = input("User: ")
    
    if message:
        messages.append(
            {"role": "user", "content": message},
        )

        chat = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages = messages
        )

    reply = chat.choices[0].message.content
    print(f"\nChatGPT: {reply}")

    messages.append({"role": "assistant", "content": reply})

    colors = table_color['color_names']
    color_codes = table_color['code']

    color_dict = {color.lower(): code for color, code in zip(colors, color_codes)}

    found_color = None
    found_hex = None

    for color in colors:
        if color.lower() in reply.lower():
            found_color = color

    if found_color is None:
        found_color = 'white'

    print(f"\n(The reply included the color {found_color})\n")

    # Tokenize the response using spaces and check if each word is in the color_dict
    for word in reply.lower().translate(str.maketrans('', '', string.punctuation)).split():
        if word in color_dict:
            found_color = word
            found_hex = color_dict[word]
            break

    if found_hex is None:
        found_hex = '#FFFFFF'

    rgb = ImageColor.getcolor(found_hex, "RGB")

    print(f"\n(The hexadecimal value of the color is {found_hex} and the RGB value of the color is {rgb})\n")

    serialInst.write("{} {} {}\n".format(*rgb).encode('utf-8'))