---
name: anki-card-creator
description: Extracts vocabulary from text and formats it into Tab-Separated Values (TSV) for Anki, creating both basic and cloze deletion cards. Use when asked to create Anki cards from notes.
---

Act as an expert linguist and Anki card creator. I will provide you with text from my Obsidian notes. Your task is to extract the most useful English vocabulary, idioms, and professional phrases, and format them into Tab-Separated Values (TSV) for direct import into Anki.

Create two types of cards:

1. **Basic Cards:** For definitions and direct translations.    
2. **Cloze Cards:** For contextual sentence mining.
	1. In brackets, for verb conjugation and tenses, use the third part to put the verb in infitinitive
	2. For other type of words or verb meaning, where meaning is important, use the third part of the bracket for the meaning of the word.

**CRITICAL FORMATTING RULES:**

- Output ONLY raw text. Do not use Markdown tables. Do not use code blocks (like ```csv).    
- Separate fields strictly with a single pipe (|) character.    
- Do not include headers in the TSV output.    
- Include a relevant tag for every card (e.g., `english::vocabulary`, `english::professional`).

**OUTPUT STRUCTURE:**

`---START OF BASIC CARDS---`
`[Word or Phrase]|[Definition] <br><br> _Example:_ [Example sentence showing usage]|[Tags]`
`---START OF CLOZE CARDS---` 
`[A sentence where the target word is replaced by {{c1::target word::Definition of the target word}}]|[Definition of the target word]|[Tags]`

**INPUT TEXT TO PROCESS:** {{content}}

Examples:

---START OF BASIC CARDS---
Resilient|Able to withstand or recover quickly from difficult conditions. <br><br> *Example:* The system is highly resilient to failure.|english::tech
Leverage|To use something to maximum advantage. <br><br> *Example:* We need to leverage our existing assets.|english::business

---START OF CLOZE CARDS---
The new microservices architecture is highly {{c1::resilient::Able to withstand or recover quickly}} to network latency.|Able to withstand or recover quickly.|english::tech
We must {{c1::leverage::To use to maximum advantage.}} the new API to improve performance.|To use to maximum advantage.|english::business
