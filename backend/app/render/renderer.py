# backend/app/render/renderer.py
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path

class ResumeRenderer:
    def __init__(self, resume_data: dict):
        self.resume = resume_data
        templates_path = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(templates_path)))

    def render_html(self, mode="ui") -> str:
        # Choose template based on mode
        template_file = "ui.html" if mode == "ui" else "formal.html"
        template = self.env.get_template(template_file)
        return template.render(resume=self.resume)

    def render_pdf(self, output_path: str, mode="formal"):
        html_content = self.render_html(mode=mode)
        HTML(string=html_content).write_pdf(output_path)
