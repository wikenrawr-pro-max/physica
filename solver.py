import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from anastruct import SystemElements
from schemas import BeamAnalysisRequest, SupportSchema, PointLoadSchema

def solve_beam(request: BeamAnalysisRequest, output_image_path: str = "test_output.png") -> dict:
    """
    Solves a 2D beam using a validated BeamAnalysisRequest object.
    Returns analysis summary dictionary and saves the moment diagram.
    """
    ss = SystemElements()
    element_length = request.length / request.num_elements

    # Build beam topology
    for i in range(request.num_elements):
        ss.add_element(location=[[i * element_length, 0], [(i + 1) * element_length, 0]])

    # Apply supports
    for sup in request.supports:
        if sup.type == "hinge":
            ss.add_support_hinged(node_id=sup.node_id)
        elif sup.type == "roller":
            ss.add_support_roll(node_id=sup.node_id)
        elif sup.type == "fixed":
            ss.add_support_fixed(node_id=sup.node_id)

    # Apply point loads
    for load in request.point_loads:
        ss.point_load(node_id=load.node_id, Fy=load.Fy, Fx=load.Fx)

    # Calculate FEA forces
    ss.solve()

    # Render bending moment diagram
    fig = ss.show_bending_moment(show=False)
    plt.title(f"Bending Moment Diagram ({request.length}m Beam)")
    plt.savefig(output_image_path, bbox_inches='tight')
    plt.close('all')

    return {
        "status": "success",
        "length": request.length,
        "elements": request.num_elements,
        "diagram_path": output_image_path
    }

if __name__ == "__main__":
    print("Testing solver.py integration with Pydantic...")

    # Build validated request
    req = BeamAnalysisRequest(
        length=10.0,
        num_elements=2,
        supports=[
            SupportSchema(node_id=1, type="hinge"),
            SupportSchema(node_id=3, type="roller")
        ],
        point_loads=[
            PointLoadSchema(node_id=2, Fy=-50.0, Fx=0.0)
        ]
    )

    result = solve_beam(req)
    print("✅ Solver successfully integrated with Pydantic schema!")
    print(f"Result summary: {result}")
