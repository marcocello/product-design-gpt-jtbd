# Gideon: User-Centric Products with AI Copilot

The Jobs-To-Be-Done (JTBD) framework is a methodology centered around the concept that customers "hire" products or services to get specific jobs done. With this project, we leverage the power of OpenAI's GPT-3.5 model to generate main jobs, job performers, user interviews, generate JBTD jobs, outcomes, and job stories, thus driving your product roadmap more efficiently.

This project, Gideon, aims to expedite and streamline the process of understanding customer needs and experiences using OpenAI's GPT-3.5 language model. By automating user interviews and generating job stories, we reduce the time and resources spent on extensive manual interactions, thereby optimizing data collection and product roadmap creation.

1. **Discovery of Main Jobs**: The system discover main jobs based on your vision and skillset.
   
2. **Synthesis of personas**: The system creates dynamic representations of user archetypes, complete with an understanding of their needs, goals, and pain points.
   
3. **Automated interviews**: We employ the language generation abilities of GPT-3.5 to create a dialogue system based on the JTBD framework. This system interacts with the synthetic personas, efficiently extracting key insights about customer motivations and needs.

... and more 
   

## Use the cloud version

Go to https://gideon.streamlit.app

## Run locally
This guide will walk you through the steps to set up and run the project using a Python virtual environment.

### Prerequisites

- Python 3.6 or higher
- `pip` package manager
- Git


### Clone the Project Repository

   ```bash
   git clone https://github.com/marcocello/productforge.git
   ```

### Create Python Virtual Environment

Navigate to the project directory:

```bash
cd product-design-gpt-jtbd

python3 -m venv .virtualenv

#Activate the virtual environment for Windows
.virtualenv\Scripts\activate

#Activate the virtual environment for macOS/Linux
source .virtualenv/bin/activate
   ```

With the virtual environment activated, use `pip` to install the project dependencies from the `requirements.txt` file. Run the following command:

```bash
pip install -r requirements.txt
```

This will install all the required packages and their dependencies into the virtual environment.

### Run Streamlit locally

```bash
streamlit run streamlit.py
   ```

<!-- 
### Configure the Environment Variables

```bash
cp .env_template .env
```
Open the `.env` file and find the variable `OPENAI_API_KEY`. Replace the placeholder value with your proper OpenAI API key and save the file.

   ```
   OPENAI_API_KEY=<your openai key>
   ```

Note: Make sure not to share your API key publicly or commit it to version control systems.

### Run the `main.ipynb` file

Activate the virtual environment by following the activation steps mentioned before if you haven't already.

Open Visual Studio Code (VSCode) or any other code editor of your choice.

Locate the `main.ipynb` file and open it. Within the `main.ipynb` file, look for the "Run" button or click on the "Run Cell" option next to each code cell to execute the code.

Follow the instructions provided in the `main.ipynb` file to interact with the project.

That's it! 

## Current Limitations

The current release (0.1) uses only GPT without any custom knowledge base and it generates up to the outcomes. Furthermore, the prompts used for generating jobs map and outcomes could benefit from additional refinement. -->

## Contribute

We're excited about collaboration and improving this project. Feel free to fork the project, submit PRs, and give your valuable feedback.

## License

This project is licensed under the terms of the MIT license.
