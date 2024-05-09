import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()


openai.api_key = "YOUR-API-KEY"

def validate_difficulty(assignment):
  print("start validating")
  chat = ChatOpenAI(openai_api_key = "YOUR-API-KEY", model="gpt-3.5-turbo-1106", temperature=0.2)
  prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a very powerful assistant that can determine the difficulty level of the provided assignment. Determine the difficulty level of the provided assignment.",
        ),
        ("user", "{input}"),
    ]
  )
  chain = prompt | chat | output_parser
  st.write(chain.invoke({"input": assignment}))

def generate_assignment(instructions, homework_type):
  response = openai.chat.completions.create(
          model="gpt-4-0125-preview",
          messages=[
              {"role": "system", "content": "You are a helpful homework generator."},
              {"role": "user", "content": "Generate homework assignment for:" 
                + homework_type 
                + "based on the following instructions:" 
                + instructions}            
              ],
          temperature=0.7,
          max_tokens=500,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

  generated_assignment = response.choices[0].message.content.strip()
  print("finish generate")
  validate_difficulty(generated_assignment)
  return generated_assignment

def refine_assignment(refined_prompt):
  response = openai.chat.completions.create(
          model="gpt-4-0125-preview",
          messages=[
              {"role": "system", "content": "You are a helpful generator that can refine homework based on the provided needs."},
              {"role": "user", "content": "Refine the provided homework assignment:" 
                + st.session_state.generated_assignment
                + "based on the following instructions:" 
                + refined_prompt}            
              ],
          temperature=0.7,
          max_tokens=500,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

  refined_assignment = response.choices[0].message.content.strip()
  validate_difficulty(refined_assignment)
  return refined_assignment

st.title('Homework Assignment Generator')

# Initialize or update session state variables
if 'generated_assignment' not in st.session_state:
    st.session_state.generated_assignment = None
if 'refinement_requested' not in st.session_state:
    st.session_state.refinement_requested = False

# Input for assignment instructions
instructions = st.text_area("Enter the assignment instructions:")

# Selection box for the type of homework
homework_type = st.selectbox("Select the type of homework:", ['Math', 'Science', 'History', 'English'])

# # Button to generate the assignment
if st.button('Generate Assignment'):
    st.session_state.generated_assignment = generate_assignment(instructions, homework_type)
    st.session_state.refinements = []  # Initialize refinements list

# Display the generated assignment
if 'generated_assignment' in st.session_state and st.session_state.generated_assignment:
    st.subheader('Generated Homework Assignment')
    st.markdown(st.session_state.generated_assignment)

    # Display all refinements
    for refinement in st.session_state.get('refinements', []):
        st.markdown(f"**Refinement:** {refinement}")

    # Refinement section
    if st.button('Refine Assignment'):
        st.session_state.refinement_requested = True

    if 'refinement_requested' in st.session_state and st.session_state.refinement_requested:
        additional_details = st.text_area("Refinement instructions:", key='refine_additional_details')
        
        if st.button('Submit Refinement'):
            # Get the latest assignment (either the original or the last refinement)
            latest_assignment = st.session_state.refinements[-1] if st.session_state.refinements else st.session_state.generated_assignment
            
            # Call API for refinement
            refined_assignment = refine_assignment(additional_details)
            
            # Add the new refinement to the list
            st.session_state.refinements.append(refined_assignment)
            
            # Optionally, to let the user finalize or continue refining:
            if st.button('Finalize Assignment'):
                st.session_state.refinement_requested = False  # End refinement process
                st.subheader('Final Homework Assignment')
                st.markdown(refined_assignment)
            else:
                st.subheader('Current Refinement')
                st.markdown(refined_assignment)
