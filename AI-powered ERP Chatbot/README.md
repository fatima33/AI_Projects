I have created an AI-powered ERP Chatbot that retrieves, explains, and analyzes company data intelligently.
Its an ERP AI Assistant: A Flask + Flutter chatbot using local LLMs for salary, attendance, and invoice data retrieval.

*Design:*
✅ Using MySQL pool (fast + safe)

✅ Use LangChain/Qwen (yes)/Gemini (only for converting natural language → SQL + summarizing results)

✅ Keep database credentials isolated in db.py

✅ Keep all AI logic separate in chain.py
