from google.adk.agents import LlmAgent, SequentialAgent

GEMINI_MODEL = "gemini-1.5-flash"

# --- Code Writer Agent ---
code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Python Code Generator.
Based only on the user's request, write Python code that fulfills the requirement.
Output only the complete Python code block, enclosed in triple backticks (```python ... ```).
Do not add any other text before or after the code block.""",
    description="Writes initial Python code based on a specification.",
    output_key="generated_code"
)

# --- Code Reviewer Agent ---
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model=GEMINI_MODEL,
    instruction="""You are an expert Python Code Reviewer. 
Your task is to provide constructive feedback on the provided code.

**Code to Review:**
```java
{generated_code}
```

**Review Checklist (Be Specific):**

1. ✅ **Correctness** – Does the code behave as expected? Any logical bugs?
2. 🧹 **Readability** – Is the code clean and well-structured? Could variable names be more meaningful?
3. ⚡ **Efficiency** – Are there unnecessary loops or redundant conditions?
4. 🔒 **Edge Case Handling** – Does the code handle nulls, empty inputs, or unusual cases?
5. 🧠 **Best Practices** – Is the code using modern Java syntax (e.g. `List.of(...)`, try-with-resources, Streams)? Are comments and structure professional?
6. 🛠️ **Refactor Suggestions** – Suggest at least one concrete improvement (even if minor), unless code is already optimized.


Output only the review comments as a bulleted list, or say "No major issues found." if the code is perfect.""",
    description="Reviews code and provides feedback.",
    output_key="review_comments"
)

# --- Code Refactorer Agent ---
code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Python Code Refactoring AI.
Improve the provided Python code based on the review comments.

**Original Code:**
```python
{generated_code}
```

**Review Checklist (Be Specific):**

1. ✅ **Correctness** – Does the code behave as expected? Any logical bugs?
2. 🧹 **Readability** – Is the code clean and well-structured? Could variable names be more meaningful?
3. ⚡ **Efficiency** – Are there unnecessary loops or redundant conditions?
4. 🔒 **Edge Case Handling** – Does the code handle nulls, empty inputs, or unusual cases?
5. 🧠 **Best Practices** – Is the code using modern Java syntax (e.g. `List.of(...)`, try-with-resources, Streams)? Are comments and structure professional?
6. 🛠️ **Refactor Suggestions** – Suggest at least one concrete improvement (even if minor), unless code is already optimized.


**Review Comments:**
{review_comments}

Output only the final, refactored Python code block, enclosed in triple backticks (```python ... ```).
""",
    description="Refactors code based on review comments.",
    output_key="refactored_code"
)

# --- Sequential Agent ---
code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[code_writer_agent, code_reviewer_agent],
    description="Executes a sequence of code writing, reviewing, and refactoring."
)

# Required for ADK Web or runners
root_agent = code_pipeline_agent
