from django.shortcuts import render
from linkedin_api import linkedin
from linkedin_api import Linkedin
from .forms import ReviewForm
from django.http import HttpResponseRedirect
from pprint import pprint
import xml.etree.ElementTree as ET
import json
import aiml

# Create your views here.

def index(request):
    return render(request,"index.html")

def login(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            persons_username = form.cleaned_data['persons_username']

            api = Linkedin(user_name,password)
            data = api.get_profile(persons_username)
            # Create the root element for XML data
            root = ET.Element("data")

            # Create and append sub-elements for each field in the data
            for key, value in data.items():
                sub_element = ET.SubElement(root, key)
                sub_element.text = str(value)

            # Create an ElementTree from the root
            tree = ET.ElementTree(root)

            # Create AIML categories from XML elements
            aiml_categories = []
            for child in root:
                if child.tag == "summary":
                    pattern = "WHAT IS YOUR SUMMARY"
                    response = child.text.strip()
                    aiml_categories.append(f"""
                    <category>
                        <pattern>{pattern}</pattern>
                        <template>{response}</template>
                    </category>
                    """)
                else:
                    pattern = f"WHAT IS YOUR {child.tag.upper()}"
                    response = child.text.strip()
                    aiml_categories.append(f"""
                    <category>
                        <pattern>{pattern}</pattern>
                        <template>{response}</template>
                    </category>
                    """)

            # Create AIML document
            aiml_document = f"""<?xml version="1.0" ?>
            <aiml>
                {"".join(aiml_categories)}
            </aiml>
            """
            pprint(aiml_document)
            # Save AIML document to an output file
            with open("output_of_aiml.xml", "w") as aiml_file:
                aiml_file.write(aiml_document)

            # Create a new AIML kernel
            kernel = aiml.Kernel()

            # Load standard AIML startup files
            kernel.learn("std-startup.xml")

            # Load additional AIML files (if needed)
            kernel.respond("load aiml b")

            # Load the newly generated AIML file
            kernel.respond("load aiml output_of_aiml.xml")

            # Interact with the chatbot
            while True:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    print("Bot: Goodbye!")
                    break
                response = kernel.respond(user_input)
                print("Bot:", response)

            print("Conversion completed. AIML data saved to 'output_aiml.xml'")

            return render(request, 'index.html', {'profile_data': aiml_document})
    else:
        form=ReviewForm()

    return render(request, "login.html",{
        "form":form
    })

def linkedin(request):
    return render(request, 'linkedin.html')
