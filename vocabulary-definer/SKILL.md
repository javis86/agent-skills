---
name: vocabulary-definer
description: Finds definitions and pronunciations for a list of vocabulary words in a markdown file and updates the file with the formatted results. Use when asked to define a list of words.
---

# Vocabulary Definer

## Overview

This skill enables the agent to find definitions and pronunciations for a list of vocabulary words and format them in a clear, consistent way within a markdown file.

## Workflow

1.  **Identify the Vocabulary List**: Locate the list of vocabulary words in the specified markdown file. The words are typically under a heading like "## Vocab".

2.  **Gather Definitions and Pronunciations**: For each word in the list, use the `google_web_search` tool to find its definition and pronunciation.
    -   Use search queries like:
        -   `"define <word> and pronunciation"`
        -   `"define <phrasal verb> phrasal verb and pronunciation"`
    -   If a search fails, try more general queries like `"definition of <word> noun"` and `"pronunciation of <word>"`.

3.  **Format the Output**: Format the collected information according to the structure specified in `references/output-format.md`.

4.  **Update the File**: Use the `replace` tool to replace the original vocabulary list in the markdown file with the newly formatted, detailed list.
