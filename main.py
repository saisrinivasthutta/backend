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
    type: str  

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Define a simple GET route to test the server is working
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

#API End Point for Getting the Results
@app.post("/pipelines/parse")
async def parse_pipeline(pipeline: Pipeline):
    G = nx.DiGraph()

    # Add nodes to the graph using only their IDs
    node_ids = [node.id for node in pipeline.nodes]
    G.add_nodes_from(node_ids)

    # Add edges to the graph
    edge_list = [(edge.source, edge.target) for edge in pipeline.edges]
    G.add_edges_from(edge_list)

    is_dag = nx.is_directed_acyclic_graph(G)

    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "is_dag": is_dag
    }
