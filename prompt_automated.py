import time

'''
Hugging Face Setup
'''
# Hugging Face Credientials
from dotenv import dotenv_values

secrets = dotenv_values('hf.env')
hf_email = secrets['EMAIL']
hf_pass = secrets['PASS']

# LLM Response Geenration
from hugchat import hugchat
from hugchat.login import Login

def create_chatbot(email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot

def create_new_conversation(chatbot):
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)

'''
Excel Parsing
'''
import pandas as pd

# Define the Excel file path
'''
Change to Excel file name.
'''
excel_file = 'MondayData.xlsx'

# Read the Excel file into a DataFrame with selected columns
df = pd.read_excel(excel_file, usecols=['Name', 'country', 'state', 'City', 'description', 'restaurant_categories', 'vegan', 'gluten_free', 'Additional Information', 'Enriched Description'])

# Define a class to represent the data
class Restaurant:
    def __init__(self, name, country, state, city, description, categories, vegan, gluten_free, add_info):
        self.name = name
        self.country = country
        self.state = state
        self.city = city
        self.description = description
        self.categories = categories
        self.vegan = vegan
        self.gluten_free = gluten_free
        self.add_info = add_info

def get_background(restaurant):
    name = restaurant.name
    city = restaurant.city
    state = restaurant.state
    country = restaurant.country
    description = restaurant.description
    restaurant_categories = restaurant.categories
    vegan = restaurant.vegan
    gluten = restaurant.gluten_free
    add_info = restaurant.add_info

    background = f"{name} is located in {city}, {state} {country}. It is a {description}. Some additional information, {add_info}. It covers food categories such as {restaurant_categories}. It is {vegan} that is vegan. It is {gluten} that it is gluten free."
    return background

# Initialize an empty list to store instances of the Restaurant class
restaurant_list = []

# Iterate through DataFrame rows and create instances of the Restaurant class
for index, row in df.iterrows():
    restaurant = Restaurant(
        row['Name'],
        row['country'],
        row['state'],
        row['City'],
        row['description'],
        row['restaurant_categories'],
        row['vegan'],
        row['gluten_free'],
        row['Additional Information']
    )
    restaurant_list.append(restaurant)

response = None

# Get template from text file
template_path = "template.txt"
with open(template_path, 'r', encoding='utf-8') as file:
    # Read the entire content of the file into a string
    template = file.read()

# Get Rules list form text file
rule_path = "rules.txt"
with open(rule_path, 'r', encoding='utf-8') as file:
    # Read the file line by line into a list of strings
    rules = file.readlines()

chatbot = create_chatbot(hf_email, hf_pass)
chatbot.set_system_prompt(template)             #Reinforce the Template Instructions.

start_row = int(input(f"What index row to start at?")) - 2

number_of_descriptions = input(f"How many descriptions starting at index {start_row + 2}?")

all_rules = ''
rule_number = 0
for rule in rules:
    all_rules += rules[rule_number]
    rule_number += 1

conversations_count = 0     # delete conversations after certain amount

for row in range (start_row, start_row + int(number_of_descriptions)):
    # Get Orignal Response
    description = get_background(restaurant_list[row])
    prompt = str(template + description)            
    response = chatbot.chat(prompt)
    print(response)

    # Finetune Response
    prompt = all_rules
    response = chatbot.chat(prompt)
    print('___Finetuned Response___\n')
    print(response)

    # Clean up Response
    # Check if the first line starts with 'sure'
    lines = str(response).split('\n')
    if "Sure" in lines[0]:
        lines.pop(0)

    # Rejoin the lines to form a new text
    cleaned_text = '\n'.join(lines)
    cleaned_text = cleaned_text.replace('\n', '')

    # Remove unwanted characters from output
    characters_to_remove = ['[', ']', "'", '"', '\\']

    for char in characters_to_remove:
        cleaned_text = cleaned_text.replace(char, '')

    # Write Finetuned response back to Excel
    data_to_write = [cleaned_text]

    df.loc[row, "Enriched Description"] = data_to_write

    # Save the DataFrame back to the Excel file
    df.to_excel(excel_file, index=False)
    
    # Move onto the next conversation
    print('___Next Description___\n')
    # create_new_conversation(chatbot)