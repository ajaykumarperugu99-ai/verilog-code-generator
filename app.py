import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Streamlit Page Setup
st.set_page_config(page_title="Verilog RTL Generator", page_icon="⚡", layout="wide")

st.title("⚡ Verilog RTL & Testbench Generator")
st.write("Enter a digital logic design task (e.g., `Full Adder`, `4-bit Counter`, `D Flip-Flop`) to generate Verilog RTL code and its Testbench.")

# Sidebar for API Key configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

# Fallback to environment variable if sidebar is empty
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY", "")

if not api_key:
    st.warning("⚠️ Please enter your Gemini API Key in the sidebar or set `GEMINI_API_KEY` environment variable.")

# User Input Box
task_input = st.text_input("Digital Hardware Task:", placeholder="e.g., Full Adder")

if st.button("Generate Code"):
    if not api_key:
        st.error("API Key is missing! Please provide a valid Gemini API Key.")
    elif not task_input.strip():
        st.error("Please enter a task description or component name.")
    else:
        with st.spinner("Generating Verilog RTL code and Testbench..."):
            try:
                # Initialize Model
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=api_key
                )
                
                prompt = f"""
                You are an expert Verilog RTL and verification engineer.
                Generate synthesizable Verilog code and a complete testbench for the following hardware design task:
                "{task_input}"

                Format the output into two clear sections:
                1. Synthesizable Verilog Module
                2. Verilog Testbench
                """
                
                response = llm.invoke([HumanMessage(content=prompt)])
                
                # Display Results
                st.success("Code generated successfully!")
                st.markdown(response.content)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
