from beanie import Document


class NLPTask(Document):
    name: str
    acronym: str
    papers_with_code_id: str
