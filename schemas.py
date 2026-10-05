from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

class SupportSchema(BaseModel):
    node_id: int = Field(..., description="The node ID where the support is located (1-indexed)")
    type: Literal["hinge", "roller", "fixed"] = Field(..., description="Type of structural support")

class PointLoadSchema(BaseModel):
    node_id: int = Field(..., description="Node ID where the point load is applied")
    Fy: float = Field(..., description="Vertical force component in kN (negative for downward)")
    Fx: float = Field(default=0.0, description="Horizontal force component in kN")

class BeamAnalysisRequest(BaseModel):
    length: float = Field(..., gt=0, description="Total length of the beam in meters")
    num_elements: int = Field(default=2, ge=1, le=20, description="Number of elements to divide the beam into")
    supports: List[SupportSchema] = Field(..., min_length=1, description="List of supports applied to the structure")
    point_loads: List[PointLoadSchema] = Field(default_factory=list, description="List of point loads applied to the structure")

    @field_validator("length")
    def validate_length(cls, v):
        if v > 100:
            raise ValueError("Beam length cannot exceed 100 meters for standard 2D analysis.")
        return v

if __name__ == "__main__":
    print("Testing Pydantic schema validation...")
    
    valid_data = {
        "length": 12.0,
        "num_elements": 2,
        "supports": [
            {"node_id": 1, "type": "hinge"},
            {"node_id": 3, "type": "roller"}
        ],
        "point_loads": [
            {"node_id": 2, "Fy": -40.0, "Fx": 0.0}
        ]
    }
    
    validated = BeamAnalysisRequest(**valid_data)
    print("✅ Valid payload successfully parsed!")
    print(f"Structure dump: {validated.model_dump_json(indent=2)}")

    print("\nTesting validation error catching...")
    invalid_data = {
        "length": -5.0,
        "supports": [{"node_id": 1, "type": "pin"}]
    }
    try:
        BeamAnalysisRequest(**invalid_data)
    except Exception as e:
        print("✅ Correctly rejected invalid data with Pydantic error:")
        print(e)
