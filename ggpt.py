# Copyright 2025 Rafael Augusto Campo Jr

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from rdflib import Graph, Namespace
import openai

# Load ontology
ONTOLOGY_FILE = "GeospatialOntology.ttl"  # Update with actual file path

g = Graph()
g.parse(str(ONTOLOGY_FILE), format="ttl")

# Define namespaces
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
CAM = Namespace("https://www.camposibs.com/")

# OpenAI API configuration (set your API key)
# openai.api_key = "api-key"

with open(".secretes", "a") as f:
    openai.api_key = f.read()

# Generate TTL output
ttl_output = """
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix ex: <http://example.org/ontology#> .
"""

def query_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "system", "content": "You are an Charming Assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]


with open("ontology_output.ttl", "w") as f:
    print(f"File Created: {f}")
    f.write(ttl_output)

# Iterate through ontology terms
for subject in g.subjects(RDFS.label):
    label = g.value(subject, RDFS.label)
    terminal = g.value(subject, CAM.terminal, default="No definition provided.")
    
    # Template for ChatGPT
    prompt = f"""
    You are an Charming Assistant.
    The context: {label}.
    Troubleshoot the issue please: {terminal}
    """

    response = query_chatgpt(prompt)

    output = f"""<{subject}> rdfs:label "{label}" ; :terminal "{terminal}" ;
            ex:chatgptResponse "{response}" ."""
    
    print(output)

    # Write to a TTL file
    with open("ontology_output.ttl", "a") as f:
        f.write(output)
