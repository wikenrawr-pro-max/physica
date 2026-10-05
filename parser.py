import os
import json
from dotenv import load_dotenv
from schemas import BeamAnalysisRequest

load_dotenv()

def parse_user_prompt(prompt: str) -> BeamAnalysisRequest:
    """Parses natural language prompt into a validated BeamAnalysisRequest."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    # Check if API key is missing or set to placeholder
    if not api_key or "your_anthropic_api_key_here" in api_key:
        print("⚠️ No valid Anthropic key found. Running in MOCK MODE...")
        return BeamAnalysisRequest(
            length=10.0,
            num_elements=2,
            supports=[
                {"node_id": 1, "type": "hinge"},
                {"node_id": 3, "type": "roller"}
            ],
            point_loads=[
                {"node_id": 2, "Fy": -50.0, "Fx": 0.0}
            ]
        )

    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        SYSTEM_PROMPT = """You are Physica's structural parsing assistant. Extract 2D beam parameters from natural language descriptions and convert them strictly into a JSON object matching this structural schema:

Schema guide:
- length (float): Total beam length in meters.
- num_elements (int): Number of sub-elements (default 2).
- supports (list): Objects containing 'node_id' (1-indexed) and 'type' ("hinge", "roller", or "fixed").
- point_loads (list): Objects containing 'node_id', 'Fy' (vertical force in kN; negative for downward), and 'Fx'.

Return strictly raw JSON without markdown code blocks."""

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Parse this beam structure: {prompt}"}]
        )
        
        raw_text = response.content[0].text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()
            
        data = json.loads(raw_text)
        return BeamAnalysisRequest(**data)

    except Exception as e:
        print(f"⚠️ API Call Failed ({e}). Falling back to MOCK MODE...")
        return BeamAnalysisRequest(
            length=10.0,
            num_elements=2,
            supports=[
                {"node_id": 1, "type": "hinge"},
                {"node_id": 3, "type": "roller"}
            ],
            point_loads=[
                {"node_id": 2, "Fy": -50.0, "Fx": 0.0}
            ]
        )

if __name__ == "__main__":
    prompt = "A 10 meter long beam split into 2 elements with a hinge at node 1, a roller at node 3, and a 50 kN downward load on node 2."
    print(f"Parsing prompt:\n\"{prompt}\"\n")
    
    validated_request = parse_user_prompt(prompt)
    print("✅ Parsed request successfully:")
    print(validated_request.model_dump_json(indent=2))
