

From a theoretical perspective, these prompts can be categorized based on their purpose and the type of information they provide. Here's a possible categorization:

### Situation Descriptions
These prompts provide context for the dialogue. They set the scene and describe the current state of the world. In this code, the game_description and character_specifier_prompt fall into this category. They describe the debate topic and the presidential candidates.

### Goal Descriptions
These prompts describe the objectives or goals that the agents are trying to achieve. In this code, the goal is implicitly described in the character_system_messages (to be creative and convince voters).

### Behavior Descriptions
These prompts describe the behavior or characteristics of the agents. The character_headers and character_system_messages fall into this category. They describe the personality of the candidates and how they should speak.

### Action Commands
These prompts instruct the agents on what actions to take. The bidding_template falls into this category. It guides the agents in generating a bid to speak next in the debate.

### Constraints
These prompts describe any constraints or rules that the agents must follow. In this code, the character_system_messages and bidding_template include constraints such as speaking in the first person, not changing roles, and keeping responses within a certain word limit.

This categorization can help in understanding the role of each prompt and how they guide the behavior of the agents. It can also be useful when designing new prompts or modifying existing ones.

### Example
Situation Descriptions

The game_description sets the scene for a presidential debate on a specific topic (e.g., "transcontinental high speed rail") with specific candidates (e.g., "Donald Trump", "Kanye West", "Elizabeth Warren").

Goal Descriptions

The goal for each candidate, as described in the character_system_messages, is to debate the topic creatively and convincingly to make voters think they are the best candidate.

Behavior Descriptions

The character_headers and character_system_messages describe the behavior of the candidates. For example, Donald Trump might be described as a bold and assertive speaker, while Elizabeth Warren might be described as a thoughtful and articulate speaker.

Action Commands

The bidding_template instructs each candidate to generate a bid to speak next in the debate. This might involve assessing how contradictory the recent message is to their ideas and generating a bid based on this assessment.

Constraints

The character_system_messages and bidding_template include constraints such as speaking in the first person, not changing roles, and keeping responses within a certain word limit.