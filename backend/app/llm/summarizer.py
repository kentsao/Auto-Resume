# backend/app/llm/summarizer.py
import os
from typing import Protocol, Dict, Any, List, runtime_checkable
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

@runtime_checkable
class LLMSummarizer(Protocol):
    async def summarize_text(self, text: str, category: str, target_audience: str = "a recruiter") -> str:
        ...

    async def summarize_resume_data(self, resume_data: Dict[str, Any], category: str, target_audience: str = "a recruiter") -> Dict[str, Any]:
        ...

class GeminiSummarizer:
    """A summarizer using the Gemini API."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please add it to your .env file.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def summarize_text(self, text: str, category: str, target_audience: str = "a recruiter") -> str:
        """Summarizes a single piece of text for a given category and target audience."""
        prompt = f"Please rephrase and summarize the following {category} information for {target_audience}:\n\n{text}"
        response = self.model.generate_content(prompt)
        return response.text

    async def summarize_work_experience(self, work_item: Dict[str, Any], target_audience: str) -> Dict[str, Any]:
        """Summarizes a single work experience item."""
        # Combine relevant fields for a comprehensive summary
        summary_input = f"Company: {work_item.get('company')}, Position: {work_item.get('position')}\nSummary: {work_item.get('summary')}\nHighlights: {', '.join(work_item.get('highlights', []))}"
        
        summarized_text = await self.summarize_text(summary_input, "work experience", target_audience)
        
        # Create a new dictionary to avoid modifying the original
        new_work_item = work_item.copy()
        new_work_item['summary'] = summarized_text
        return new_work_item

    async def summarize_resume_data(self, resume_data: Dict[str, Any], category: str, target_audience: str = "a recruiter") -> Dict[str, Any]:
        """Summarizes a specific category in the resume data."""
        
        if category == "work" and "work" in resume_data:
            summarized_work = []
            for work_item in resume_data["work"]:
                summarized_work.append(await self.summarize_work_experience(work_item, target_audience))
            resume_data["work"] = summarized_work

        # Add more categories here as needed, e.g., 'basics', 'projects'
        # Example for 'basics.summary'
        elif category == "basics" and "basics" in resume_data and "summary" in resume_data["basics"]:
            summary = resume_data["basics"]["summary"]
            if summary:
                resume_data["basics"]["summary"] = await self.summarize_text(summary, "personal summary", target_audience)

        return resume_data

def get_summarizer() -> LLMSummarizer:
    """Factory function to get the configured LLM summarizer."""
    return GeminiSummarizer()
