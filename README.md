# Multimodal Dialogue Generation for Pepper and Furhat using Gemini LLM

This project leverages Google's Gemini LLM to generate expressive and dynamic conversations for two social robots: **Pepper** and **Furhat**. The system produces not only spoken dialogue, but also accompanying **gestures** and, in Furhat's case, **audio expressions** and **voice adaptation**.

## Robot-Specific Behaviors

- **Pepper (SoftBank Robotics)**  
  - Generates spoken dialogue enriched with **gestures** such as head movements and arm motions.  
  - Focused on embodied, physical interaction.

- **Furhat (Furhat Robotics)**  
  - Generates spoken dialogue with both **gestures** and **non-verbal audio expressions** using **Acapela voice smileys**.  
  - Adapts the **voice based on the user's age**:
    - 👶 Uses a **child-like voice** for users aged 12 or younger.
    - 🧑 Switches to a **standard adult voice** for users aged 13 and above.

## Key Features

- 💡 LLM-powered generation of conversational content
- 🧠 Context-aware integration of gestures and sounds
- 🎭 Emotional expressivity through Acapela voice smileys (Furhat only)
- 👤 Age-aware voice selection (Furhat only)

## Goals

The goal of this project is to bridge natural language understanding with expressive multimodal output in robotics. This includes:

- Structuring LLM output into timed sequences of dialogue, motion, and audio
- Mapping abstract commands to each robot’s API
- Creating an adaptable architecture for extending to other platforms or interaction modes

---

This repository includes the source code and configuration files needed to deploy the system on either Pepper or Furhat. Contributions and feedback are welcome.
