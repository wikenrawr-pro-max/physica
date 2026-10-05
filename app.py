import streamlit as st
from parser import parse_user_prompt
from solver import solve_beam
import os

st.set_page_config(page_title="Physica - AI Structural FEA", page_icon="🏗️", layout="centered")

st.title("🏗️ Physica")
st.subheader("Natural Language to Structural FEA Diagram")

# Text prompt box
prompt = st.text_area(
    "Enter your beam description:",
    value="A 10 meter long beam split into 2 elements with a hinge at node 1, a roller at node 3, and a 50 kN downward load on node 2.",
    height=100
)

if st.button("Generate FEA Diagram", type="primary"):
    with st.spinner("Parsing structure and calculating physics..."):
        try:
            # Step 1: Parse request using Day 3 logic
            request_schema = parse_user_prompt(prompt)
            
            # Step 2: Calculate FEA and generate plot image
            output_path = "web_analysis_output.png"
            solve_beam(request_schema, output_image_path=output_path)
            
            st.success("Analysis Complete!")
            
            # Step 3: Render image in browser
            st.image(output_path, caption="Generated FEA Diagram", use_container_width=True)
            
            # Show extracted data structure
            with st.expander("🔍 View Parsed Pydantic Schema"):
                st.json(request_schema.model_dump())
                
        except Exception as e:
            st.error(f"Error processing request: {e}")
