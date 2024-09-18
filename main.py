from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx
from pydantic import BaseModel
from typing import List

# Initialize the FastAPI app
app = FastAPI()

# Define the request body structure
class Edge(BaseModel):
    source: str
    target: str

class Node(BaseModel):
    id: str
    type: str  # Assuming you have types like 'input', 'output', etc.

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

# Add CORS middleware to allow requests from localhost:3000 (React app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only this origin (your React app)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define a simple GET route to test the server is working
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/pipelines/parse")
async def parse_pipeline(pipeline: Pipeline):
    G = nx.DiGraph()

    # Add nodes to the graph using only their IDs
    node_ids = [node.id for node in pipeline.nodes]
    G.add_nodes_from(node_ids)

    # Add edges to the graph
    edge_list = [(edge.source, edge.target) for edge in pipeline.edges]
    G.add_edges_from(edge_list)

    # Example of using NetworkX's built-in algorithms
    is_dag = nx.is_directed_acyclic_graph(G)

    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "is_dag": is_dag
    }
