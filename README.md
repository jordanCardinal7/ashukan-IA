# Project Title: Forest Management Analysis Tool

## Description

This project involves a Python-based data processing and analysis tool designed for synthesizing ideas about governance in Indigenous contexts and suggesting improvements for forest management in Quebec. The tool leverages OpenAI's GPT-4 model to analyze, synthesize, and offer insights on collected data.

## Workflow

The project workflow is divided into several stages:

1. **Data Preprocessing**: Raw data is processed and outputted into a structured JSON format.
2. **Data Analysis and Synthesis**: The preprocessed data is passed through GPT-4 to generate organized lists of ideas and themes.
3. **Synthesis Paragraphs Generation**: Short synthesis paragraphs are created for each set of ideas/themes.
4. **Final Output Generation**: A general synthesis is created, along with AI's perspective on the synthesized data.
5. **Report Generation**: A general report comprehensively displaying all data.


## Usage

The tool is run via a command-line interface with different modes corresponding to each stage of the workflow:

- Mode 0: Data preprocessing (`run.py 0`)
- Mode 1: Data analysis and synthesis (`run.py 1`)
- Mode 2: Synthesis paragraphs generation (`run.py 2`)
- Mode 3: Final output generation (`run.py 3`)
- Mode 4: Compiling all data into a single comprehensive report (`run.py 4`)

## Directory Structure

- `data/`
  - `raw/`: Contains the raw data files.
  - `interim/`: Stores the preprocessed data.
  - `processed/`
    - `step_1/`: Output from the first analysis stage.
    - `step_2/`: Synthesis paragraphs.
    - `final/`: Final synthesized output and AI analysis.
- `scripts/`: Contains Python scripts for API interaction and other utilities.

## Requirements

- Python 3.x
- OpenAI Python library
- Other dependencies as listed in `requirements.txt`

## Setup and Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
4. Run the tool as needed per the usage instructions.

## Contributing

Contributions to the project are welcome. Please follow the standard fork, branch, and pull request workflow.

## License

[License details]

---

Feel free to modify and expand upon this template to better suit the specifics and nuances of your project!