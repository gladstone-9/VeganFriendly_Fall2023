'''
Hugging Face Setup
'''
# For Hugging Face Credientials
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
excel_file = 'ChosenColumns.xlsx'

# Read the Excel file into a DataFrame with selected columns
df = pd.read_excel(excel_file, usecols=['Name', 'country', 'state', 'City', 'description', 'restaurant_categories', 'vegan', 'gluten_free'])

# Define a class to represent the data
class Restaurant:
    def __init__(self, name, country, state, city, description, categories, vegan, gluten_free):
        self.name = name
        self.country = country
        self.state = state
        self.city = city
        self.description = description
        self.categories = categories
        self.vegan = vegan
        self.gluten_free = gluten_free

def get_background(restaurant):
    name = restaurant.name
    city = restaurant.city
    state = restaurant.state
    country = restaurant.country
    description = restaurant.description
    restaurant_categories = restaurant.categories
    vegan = restaurant.vegan
    gluten = restaurant.gluten_free

    background = f"{name} is located in {city}, {state} {country}. It is a {description} It covers food categories such as {restaurant_categories}. It is {vegan} that is vegan. It is {gluten} that it is gluten free."
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
        row['gluten_free']
    )
    restaurant_list.append(restaurant)

# Get template from text file
template_path = "template.txt"
with open(template_path, 'r', encoding='utf-8') as file:
    # Read the entire content of the file into a string
    template = file.read()

# Get Rules list form text file
rule_path = "rules.txt"
with open(rule_path, 'r', encoding='utf-8') as file:
    # Read the file line by line into a list of strings
    rules = file.readlines()        #A list of strings

chatbot = create_chatbot(hf_email, hf_pass)
chatbot.set_system_prompt(template)             #Reinforce the Template Instructions.

row = 0             #Change this to get the next description in the excel sheet.
additional_information = input(f"Enter any additional info related to {restaurant_list[row].name}:\n")
description = get_background(restaurant_list[row]) + additional_information      #Brief background from Monday Data
prompt = template + description                                 
response = chatbot.chat(prompt)
print(response)

user_says_stop = False
user_wants_to_finetune = False

while user_says_stop == False:
    user_input = input("Do you want to finetune the response (y)?")
    if user_input == 'y':
        user_wants_to_finetune = True
    
    while user_wants_to_finetune == True:
        #Choose rule to finetune response or create own rule
        rule_number = 0
        for rule in rules:
            print(f"Rule {rule_number}: {rule}")
            rule_number += 1
        print(f"Customized Rule (c)")

        user_input = input("Which rule do you want to use?")

        if user_input == 'c':
            user_input = input("Enter customized rule:\n")
            prompt = user_input
        else:
            prompt = rules[int(user_input)]

        response = chatbot.chat(prompt)

        print('___Finetuned Response___\n')
        print(response)
        user_input = input("Do you want to continue finetuning (n)?")
        if user_input == 'n':
            user_wants_to_finetune = False
    
    user_input = input("Do you want the next description (n)?")
    if user_input == 'n':
        break
    print('___Next Description___\n')
    
    #Move onto the next conversation
    create_new_conversation(chatbot)                        #Creates a new conversation.

    row += 1

    additional_information = input(f"Enter any additional info related to {restaurant_list[row].name}:\n")

    description = get_background(restaurant_list[row]) + additional_information      #Brief background from Monday Data
    prompt = template + description                                 
    response = chatbot.chat(prompt)
    print(response)