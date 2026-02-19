# AI Implementation Notes

## LLM Selection
I chose **GPT-3.5-Turbo** (`gpt-3.5-turbo-1106`) for the summarization task.

**Why?**
- **JSON Mode**: The `1106` model supports `response_format={"type": "json_object"}`, which was critical for generating the structured insights (Pricing vs. Strategy) reliably.
- **Cost/Performance**: It's significantly faster and cheaper than GPT-4, which is vital for a "Check Now" feature where user latency matters.
- **Task Suitability**: The task is extraction and summarization, which 3.5 handles well. Complex reasoning (GPT-4 level) wasn't required for diff summarization.

## AI Assistance in Development
I used AI to accelerate development in the following areas:

1.  **Regex Generation**: Used AI to generate the complex regex patterns in `services/preprocess.py` for stripping timestamps (`\b\d+\s+(points?|hours?)...`) and navigation menus.
2.  **CSS Polish**: Generated the modern SaaS color palette and shadow variables to ensure a professional look without importing a heavy framework like Tailwind.
3.  **Boilerplate**: Quickly scaffolded the SQLAlchemy async patterns and Pydantic models.

## Manual Verification & Quality Control
I personally verified:

-   **Noise Reduction**: Tested against *Hacker News* and *Stripe* to ensure that identifying "14 hours ago" vs "15 hours ago" did NOT trigger a false positive change.
-   **Security**: Ensured `OPENAI_API_KEY` and `DATABASE_URL` are strictly loaded from environment variables and never hardcoded.
-   **Docker**: Verified the multi-stage build process to keep the image size reasonable.
