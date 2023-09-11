entities = [
    "Mathematical entity", "Person", "Location", "Animal", "Activity",
    "Programming language", "Equation", "Date", "Shape", "Property",
    "Mathematical expression", "Profession", "Time period", "Mathematical subject",
    "Mathematical concept", "Discipline", "Mathematical theorem", "Physical entity",
    "Physics subject", "Physics"
]
relationships = [
    "IS", "ARE", "WAS", "EQUIVALENT_TO", "CONTAINS", "PROPOSED", "PARTICIPATED_IN",
    "SOLVED", "RELATED_TO", "CORRESPONDS_TO", "HAS_PROPERTY", "REPRESENTS", "IS_USED_IN",
    "DISCOVERED", "FOUND", "IS_SOLUTION_TO", "PROVED", "LIVED_IN", "LIKED", "BORN_IN",
    "CONTRIBUTED_TO", "IMPLIES", "DESCRIBES", "DEVELOPED", "HAS_PROPERTY", "USED_FOR"
]

prompt = f"""
You are a mathematician and a scientist helping us extract relevant information from articles about mathematics. 
The task is to extract as many relevant relationships between entities to mathematics, physics, or history and science in general as possible.
The entities should include all persons, mathematical entities, locations etc. 
Specifically, the only entity tags you may use are:
{', '.join(entities)}.
The only relationships you may use are:
{', '.join(relationships)}
As an example, if the text is "Euler was located in Sankt Petersburg in the 17 hundreds", the output should have the following format: Euler: Person, LIVED_IN, Skt. Petersburg: Location 
If we have "In 1859, Riemann proved Theorem A", then as an output you should return Riemann: Person, PROVED, Theorem A: Mathematical theorem
I am only interested in the relationships in the above format and you can only use what you find in the text provided. Also, you should not provide relationships already found and you should choose less than 100 relationships and the most important ones.
You should only take the most important relationships as the aim is to build a knowledge graph. Rather a few but contextual meaningful than many nonsensical. 
Moreover, you should only tag entities with one of the allowed tags if it truly fits that category and I am only interested in general entities such as "Shape HAS Area" rather than "Shape HAS Area 1".
The input text is the following:

"""

