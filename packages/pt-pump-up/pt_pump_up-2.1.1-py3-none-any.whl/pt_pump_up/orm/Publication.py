from beanie import Document
from typing import Optional, List


class Publication(Document):
    title: str
    abstract: str
    authors: List[str]
    url_abstract: Optional[str] = None
    url_pdf: str
    published_date: str
    journal_or_conference: str
    github_url: Optional[str] = None
    doi: Optional[str] = None
    bibtex: Optional[str] = None
