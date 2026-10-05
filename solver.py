from anastruct import SystemElements
import matplotlib.pyplot as plt

def test_physics_engine():
    # Initialize a 2D structural system
    ss = SystemElements()
    
    # Define a 12-meter beam (two 6-meter elements connected at x=6)
    ss.add_element(location=[[0, 0], [6, 0]])
    ss.add_element(location=[[6, 0], [12, 0]])
    
    # Add supports: Hinge at left end (x=0), Roller at right end (x=12)
    ss.add_support_hinged(node_id=1)
    ss.add_support_roll(node_id=3, direction=2)
    
    # Apply a 40 kN downward point load at center node (x=6)
    ss.point_load(node_id=2, Fy=-40.0)
    
    # Calculate global stiffness matrix and solve
    ss.solve()
    
    print("✅ Anastruct FEA solver executed successfully!")
    
    # Save visualization to image
    ss.show_structure(show=False)
    plt.title("Physica Day 1 Test - 12m Beam with 40kN Load")
    plt.savefig("test_output.png")
    print("✅ Diagram rendered and saved as 'test_output.png'")

if __name__ == "__main__":
    test_physics_engine()
