from parser import parse_user_prompt
from solver import solve_beam

def run_pipeline(prompt: str):
    print(f"--- Running Physica End-to-End Pipeline ---")
    print(f"User Input: \"{prompt}\"\n")
    
    # Step 1: Parse prompt into Pydantic model
    request_schema = parse_user_prompt(prompt)
    print("1. Schema Parsed & Validated:")
    print(request_schema.model_dump_json(indent=2))
    
    # Step 2: Pass validated schema into FEA solver
    print("\n2. Solving Structural Physics & Generating Diagram...")
    result = solve_beam(request_schema, output_image_path="final_beam_analysis.png")
    
    print("\n✅ Pipeline Execution Complete!")
    print(f"Result summary: {result}")

if __name__ == "__main__":
    user_prompt = "A 10 meter long beam split into 2 elements with a hinge at node 1, a roller at node 3, and a 50 kN downward load on node 2."
    run_pipeline(user_prompt)
