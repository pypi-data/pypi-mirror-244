# Fendi project

![logo](https://raw.githubusercontent.com/fedihamdi/WGP/main/src/images/logo.png)

Fendi is a powerful Python package designed to simplify the creation of a
Streamlit-powered chatbot infused with AI capabilities. This chatbot extracts valuable
information from user CVs and LinkedIn profiles, offering a personalized and interactive
experience.

## Overview

The Streamlit Chatbot AI Package is a Python package designed to streamline the process of creating a chatbot powered by AI. The chatbot utilizes information from user CVs and LinkedIn profiles to provide an interactive and personalized experience.

## Features

- **AI-Powered Chatbot:** Leverage advanced natural language processing (NLP) algorithms to create an intelligent and responsive chatbot.
- **CV Integration:** Extract relevant information from user CVs to enhance the chatbot's understanding and responses.
- **⚠️LinkedIn Data Integration:** Utilize data from LinkedIn profiles to personalize the chatbot's interactions.[Only linkedin PDF resume for now ]
- **Streamlit App:** Integrated with Streamlit, allowing for easy deployment and a user-friendly interface.
- **Customizable:** Easily tailor the chatbot behavior and appearance to suit specific requirements.

## Installation

Create you virtual environment using the following command (make sure that the virtual env is using py 3.9.18)
```bash
conda create -n myenv_39 python==3.9.18
```
Activate myenv_39:
```bash
conda activate myenv_39
```
Install the package using the following command:
```bash
pip install fendi
```

## Desclaimer
This project does not aim to cover best practices for Python project
development as a whole. For example, it does not provide guidance or tool
recommendations for version control, documentation, or testing.
Feel free to contact me directly, so that I can give you a walk through.

## Getting Started
**TL;DR**
> [Colab Tutorial]
> Just take a glimpse of this quick tutorial on Google Colab.
> [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/18Bw5EBs94M8c-iQob-WIS-KU8uyA9iJz#scrollTo=hqOdwn1sJZSx)

On
> Make sure that you virtual environment is activated.
1. Import Fendi in Your Python Script:
 ```py
from fendi import fedi
```
2. Define User Information:
 ```py
info = {
    "Pronoun": "his",
    "Subject": "he"}
```
Feel free to adapt this to your specific needs, adding or removing fields as required.

⚠️ The top required ones are :
``Pronoun``, ``Subject``, ``Name``, ``Full Name``, ``Intro and About`` .

3. Specify CV Path:
```py
 cv_path = r"./Profile.pdf"
```
Again the resume file should be downloaded from the Linkedin, see next section for more details.

4. Create Streamlit App:
> Invoke the create_app function provided by Fendi:
```python
 fedi.create_app(info, cv_path)
```
5. Run Your Streamlit App:
> Execute your Streamlit app script to launch the chatbot interface:
```python
streamlit run your_script.py
```
> ⚠️ ***Replace your_script.py with the name of your Python script.***   ️⚠️
6. Interact with the Chatbot:
Open your web browser and navigate to the provided Streamlit URL: http://localhost:8501/. Interact with the chatbot by
asking questions or providing input based on the user information.
7. Explore Example Usage:
Check out the `example.py` file
### Example Script
```python [exmple.py]
from fendi import fedi

def main():
    info = {
       # ... (your personal information)
    }
    cv_path = r"./Profile.pdf"
    fedi.create_app(info, cv_path)

if __name__ == '__main__':
    main()
```

:warning: you should create a directory where you will put your script. It shall be this way:
```commandline
Directory Structure:
.
├── example.py
│   (Description: Your main Python script or example file.)
└── Profile.pdf
    (Description: The Resume file you downloaded from LinkedIn.)
```

## Contributions
Contributions to Fendi are welcome!
Feel free to open issues or submit pull requests on the [GitHub repository][src].

[The source for this project is available here][src].

----

This is the README file for the project.

The PDF file should use UTF-8 encoding and can be downloaded from you Linkedin profile.

<img src="https://resumeworded.com/linkedin-review/img/sample.gif" alt="Your GIF" width="300"/>

[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md
use].

## What's New
Nothing for now. But I won't be supporting this package for long.
I use :
[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md
use].


[Portfolio]: https://fedihamdi.netlify.app/
[src]: https://github.com/fedihamdi
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
[Colab Tutorial]: https://colab.research.google.com/drive/18Bw5EBs94M8c-iQob-WIS-KU8uyA9iJz#scrollTo=hqOdwn1sJZSx
