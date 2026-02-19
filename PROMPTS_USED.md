# Prompts Used

## Development Prompts
*Note: These are conceptual prompts used by the agent during the coding process.*

1. **Project Scaffold**: "Create a directory structure for a FastAPI project with services, models, and templates."
2. **SQLAlchemy Async**: "Write a `database.py` configurations using `sqlalchemy.ext.asyncio` and `create_async_engine`."
3. **HTML Cleaning**: "Write a Python function using BeautifulSoup to strip script and style tags and extract clean text from HTML."
4. **Diff Logic**: "Implement a function using `difflib` to compare two strings and return a list of added and removed lines."
5. **OpenAI Integration**: "Write an async function to call OpenAI ChatCompletion to summarize a text diff."

## System Prompt for App (Final Version)
The application uses the following prompt for the LLM service to enforce structured JSON output:

> You are a competitive intelligence analyst.
> Compare previous and new version of a SaaS website page.
>
> Ignore:
> - navigation elements, footer links
> - timestamps, minor numeric changes
> - ordering changes, copyright updates
>
> Focus on:
> - pricing updates
> - feature additions or removals
> - product launches
> - positioning or messaging changes
> - policy changes
>
> Return a JSON object with the following keys:
> - pricing (list of strings)
> - features (list of strings)
> - positioning (list of strings)
> - strategy (list of strings, 1-2 lines on implications)
>
> If no meaningful change in a category, return an empty list.

