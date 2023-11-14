# User-Centric Products Design with AI Copilot

The Jobs-To-Be-Done (JTBD) [[1](#1), [2](#2), [3](#3)] framework is a methodology centered around the concept that customers "hire" products or services to accomplish specific tasks.

With this project, we harness the power of OpenAI's GPT models to identify main jobs, job performers, create synthetic users, conduct interviews, and develop needs, thereby driving your product roadmap more efficiently. By automating user interviews, we reduce the time and resources spent on extensive manual interactions, optimizing data collection and product roadmap creation.

1. **Discovery of Main Jobs and Job Performers:** The system identifies and suggests a list of potential main jobs and job performers based on your vision and skillset.

2. **Synthesis of Job Performers:** The system creates dynamic representations of user archetypes, complete with an understanding of their needs, goals, and pain points.

3. **Automated Interviews:** We leverage the language generation abilities of GPT to create a dialogue system based on the JTBD framework. This system interacts with synthetic personas, efficiently extracting key insights about customer motivations and needs.

4. **Analyze Interviews:** This last step enables us to seamlessly distill the wealth of information gathered from automated interviews into actionable insights. By leveraging OpenAI's GPT models to analyze interviews, we extract detailed information such as job steps, needs, emotional jobs, and social jobs. 

This project serves as a foundation for a user-centric product design strategy, empowering you to make informed decisions about feature prioritization, user experience enhancements, and overall product development.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- `pip` package manager
- Git
- VS Code


### Clone the project

   ```bash
   git clone https://github.com/marcocello/product-design-gpt-jtbd
   ```

### Create Python virtual environment and install dependencies

```bash
cd product-design-gpt-jtbd

python3 -m venv .virtualenv
   ```

```bash 
#Activate the virtual environment for Windows
.virtualenv\Scripts\activate

#Activate the virtual environment for macOS/Linux
source .virtualenv/bin/activate
   ```

```bash
pip install -r requirements.txt
```
### Configure the Environment Variables

```bash
cp .env_template .env
```
Open the `.env` file and find the variable `OPENAI_API_KEY`. Replace the placeholder value with your proper OpenAI API key and save the file.

   ```
   OPENAI_API_KEY=<your openai key>
   ```

Note: Make sure not to share your API key publicly or commit it to version control systems.

### Run the `notebook.ipynb` file

Activate the virtual environment by following the activation steps mentioned before if you haven't already.

Open Visual Studio Code (VSCode) or any other code editor of your choice.

Locate the `notebook.ipynb` file and open it. Within the `notebook.ipynb` file, look for the "Run" button or click on the "Run Cell" option next to each code cell to execute the code.

Follow the instructions provided in the `notebook.ipynb` file to interact with the project.

That's it!
 
## Current Limitations

Current release only works fine with gpt-4-1106-preview model.

## References

<a id="1">[1]</a> J. Kalbach, The Jobs To Be Done Playbook: Align Your Markets, Organization, and Strategy Around Customer Needs. New York: Rosenfeld Media, 2020.

<a id="2">[2]</a> A. Ulwick, What Customers Want: Using Outcome-Driven Innovation to Create Breakthrough Products and Services. McGraw-Hill, 2005.

<a id="3">[3]</a> A. Ulwick, Put Jobs-To-Be-Done Theory Into Practice With Outcome-Driven Innovation, https://www.youtube.com/watch?v=2ecwXEnQ6xY, 2018.

<a id="4">[4]</a> M. Cello, Supercharging Product Design: Unleashing GPT and Jobs-to-be-Done for Limitless Innovation, https://bootcamp.uxdesign.cc/supercharging-product-design-unleashing-gpt-and-jobs-to-be-done-for-limitless-innovation-ff32fcb2c5a4, 2023


## Contribute

We're excited about collaboration and improving this project. Feel free to fork the project, submit PRs, and give your valuable feedback.

## License

This project is licensed under the terms of the MIT license.
