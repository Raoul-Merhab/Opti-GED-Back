import anthropic
import base64
from pdf2jpg import pdf2jpg
import os
from PIL import Image
import json
import requests

# models constants
max_tokens = 4000   
temperature = 1

# Pre-Prompts
preprompt_diagram_to_text = "You are an AI assistant that analyzes workflow diagrams and provides detailed descriptions of them in plain text. When given an image of a workflow diagram as input, you should carefully examine the diagram and generate a thorough written description explaining the various components, steps, and flow represented in the diagram. Your description should be easy for a non-technical person to understand, using clear language to convey the meaning and purpose of the workflow diagram."
preprompt_text_to_actors = '''You are an AI assistant helping an IT consultant analyze a client company's workflows. You will be provided with text that describes the functions and workflows within a department of the client company. Your task is to carefully read and understand the text, and then extract a list of all the active actors (roles, teams, individuals) involved in the workflows described. Present this list in a clear and concise manner to assist the consultant in understanding who the key participants are in executing the departmental processes and workflows.'''
preprompt_get_diagrams = '''You are an AI assistant that analyzes images to determine if they are workflow diagrams or not. You will receive multiple images as input. For each image, you should output the image number followed by 'True' if the image is a workflow diagram, or 'False' if it is not. Use the following syntax:
Photo 1: True
Photo 2: False
Photo 3: True
...
Replace the 'True' or 'False' values with your assessment of whether each numbered image is a workflow diagram or not.'''
preprompt_suggerer_workflow = '''Je vais t'utiliser comme intelligence artificielle pour résoudre un problème dans ma solution. Je suis en train de réaliser une solution d'anticipation des changements GED avec l'IA. En entrée tu as les acteurs de l'entreprise : nom, rôle et département. Les documents de l'entreprise : leurs types. Une liste de workflows de validation (un par ligne) sous la forme suivante. Par exemple : Acteur A envoie Document X à Acteur Z. Acteur Z valide Document X et l'envoie à acteur W.

Ton rôle est de comparer ces workflows à ceux que tu connais déjà et de répondre de la manière suivante.

Suggestions de correction
// Tu mets ici les suggestions de correction des workflows de validation en te basant sur les workflows que tu connais, les acteurs de l'entreprise et les documents. Tu me fais une liste de workflows corrigés en respectant comment j'ai écrit.

Suggestions d'ajout
// Tu mets ici les suggestions d'ajout des workflows de validation en te basant sur les workflows que tu connais, les acteurs de l'entreprise et les documents. Tu me fais une liste de workflows ajoutés  en respectant comment j'ai écrit.

Après ce prompt, tu ne réponds rien. Tu attends mes messages de la forme :
Acteurs
Role, Département
Role, Département

Documents
Type document

Workflows de validation
Acteurs
Employé, Direction financière
Responsable, Direction financière
Responsable, Direction RH
Comptable, Département comptabilité

Documents
Demande de congé

Workflows de validation'''

def jpeg_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")
    return encoded_string

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def jpg_to_jpeg(path):
    im = Image.open(path)
    im = im.convert("RGB")
    im.save(path.replace(".jpg",".jpeg"))
    os.remove(path)

class IntelligentStuff():
    
    @staticmethod
    def diagram_to_text(img):
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            temperature=temperature,
            system=preprompt_diagram_to_text,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img
                            }
                        }
                    ]
                }
            ]
        )
        return message.content[0].text
    
    @staticmethod
    def text_to_actors(text):
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            temperature=temperature,
            system=preprompt_text_to_actors,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        )
        return message.content[0].text
    
    @staticmethod
    def pdf_to_jpegs(base64_pdf):
        os.mkdir("/temp")
        pdfPath = r"/temp/file.pdf"
        with open(pdfPath, "wb") as file:
            file.write(base64.b64decode(base64_pdf))
        outputpath = r"/temp/Images/"
        pdf2jpg.convert_pdf2jpg(pdfPath,outputpath, pages="ALL")
        os.remove(pdfPath)
        jpgpath="/temp/Images/file.pdf_dir/"
        for filename in os.listdir(jpgpath):
            if filename.endswith(".jpg"):
                jpg_to_jpeg(jpgpath+filename)
            else:
                continue
        imgspath = "/temp/Images/file.pdf_dir/"
        images = []
        for filename in os.listdir(imgspath):
            if filename.endswith(".jpeg"):
                image_path = os.path.join(imgspath, filename)
                images.append(image_to_base64(image_path))
        client = anthropic.Anthropic()
        messageContent= []
        for image in images:
            messageContent.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image
                }
            })
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            temperature=temperature,
            system=preprompt_get_diagrams,
            messages=[
                {
                    "role": "user",
                    "content": messageContent
                }
            ]
        )
        boolean_array = []
        for line in message.content[0].text.split('\n'):
            if line.endswith('True'):
                boolean_array.append(True)
            elif line.endswith('False'):
                boolean_array.append(False)
        workflows = []
        for i in range(len(images)):
            if ( boolean_array[i]):
                workflows.append(IntelligentStuff.diagram_to_text(images[i]))
        os.remove("/temp")
        return workflows
    
    @staticmethod
    def suggerer_workflow(image64):
        image64 = image64.split(",")[1]
        print(image64)
        text = IntelligentStuff.diagram_to_text(image64)
        
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiM2YzNjQwZjMtMTJjZi00NzVkLWI2OTYtMTA4NTM2MzRiMGU5IiwidHlwZSI6ImFwaV90b2tlbiJ9.usYr-6c0Nwf7n3R6VS9DLA5EGPkAdcRZUz8Weoqjtog"}

        url = "https://api.edenai.run/v2/text/chat"
        payload = {
            "providers": "openai",
            "text": text,
            "chatbot_global_action": preprompt_suggerer_workflow,
            "previous_history": [],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "fallback_providers": ""
        }

        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
        return result['openai']['generated_text']
