# Homework Assignment Generator

## Overview
The Homework Assignment Generator is a Streamlit application that leverages the OpenAI API to generate and refine homework assignments based on user inputs. It supports various subjects such as Math, Science, History, and English. The application also offers functionality to assess the difficulty of generated assignments and refine them based on additional instructions.

## Features
- Generate homework assignments for different subjects using OpenAI API.
- Assess the difficulty level of assignments using LangChain.
- Refine assignments based on user feedback using OpenAI API.

### Installation Steps
1. Clone this repository or download the application files.
2. Navigate to the application directory.
3. Set your OpenAI API key at line 10 and line 14 of homework_generator.py.
4. Run the Streamlit application: streamlit run homework_generator.py

## Usage
1. **Enter Assignment Instructions**: Start by typing the instructions for the assignment in the text area provided.
2. **Select Homework Type**: Choose the type of homework you're creating an assignment for (e.g., Math, Science, History, English).
3. **Generate Assignment**: Click the "Generate Assignment" button to receive your initial homework assignment based on the instructions and type you provided.
4. **Review and Refine**: If the generated assignment needs refinement, use the refinement feature to specify additional details or corrections. The application will then generate a refined version of the assignment.
5. **Finalize Assignment**: Review the final version of the assignment. If further refinements are needed, you can repeat the refinement process.