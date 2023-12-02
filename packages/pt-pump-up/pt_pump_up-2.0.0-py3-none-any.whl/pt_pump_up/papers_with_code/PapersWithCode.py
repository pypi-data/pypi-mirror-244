from abc import abstractmethod, ABC
from mechanize import Item, Browser
import os

PAPERS_WITH_CODE_USERNAME = os.environ.get('PAPERS_WITH_CODE_USERNAME', None)
PAPERS_WITH_CODE_PASSWORD = os.environ.get('PAPERS_WITH_CODE_PASSWORD', None)
PAPERS_WITH_CODE_API_KEY = os.environ.get('PAPERS_WITH_CODE_API_KEY', None)

if PAPERS_WITH_CODE_USERNAME is None or PAPERS_WITH_CODE_PASSWORD is None or PAPERS_WITH_CODE_API_KEY is None:
    raise Exception(
        "PAPERS_WITH_CODE_USERNAME, PAPERS_WITH_CODE_PASSWORD and PAPERS_WITH_CODE_API_KEY must be set"
    )


class PaperWithCodeElement(ABC):
    # Abstract method findall
    @abstractmethod
    def insert(self, br: Browser) -> list:
        pass

    def bypass_select(self, select_control, value):
        select_control.items.append(
            Item(select_control, {"name": value, "value": value})
        )


class PapersWithCodeDataset(PaperWithCodeElement):
    def __init__(self, name, full_name, description, url, introduced_data, license_name, license_url, modalities, languages, tasks) -> None:
        self.post_url = "https://paperswithcode.com/contribute/dataset/new"
        self.name = name
        self.full_name = full_name
        self.description = description
        self.url = url
        self.introduced_data = introduced_data
        self.license_name = license_name
        self.license_url = license_url
        self.modalities = modalities
        self.languages = languages
        self.tasks = tasks

    def insert(self, br: Browser) -> list:
        br.open(self.post_url)
        br.select_form(nr=2)

        br.form['name'] = self.name
        br.form['full_name'] = self.full_name
        br.form['description'] = self.description
        br.form['url'] = self.url
        br.form['introduced_date'] = self.introduced_data
        br.form['license_name'] = self.license_name
        br.form['license_url'] = self.license_url

        # Selects must be bypassed
        self.bypass_select(br.form.find_control(
            name='modalities'), self.modalities)
        self.bypass_select(br.form.find_control(
            name='languages'), self.languages)
        self.bypass_select(br.form.find_control(name='tasks'), self.tasks)

        # Bypasse done. Now we can assign the values
        br.form['modalities'] = self.modalities
        br.form['languages'] = self.languages
        br.form['tasks'] = self.tasks

        return br.submit()


class PaperWithCodePaper(PaperWithCodeElement):
    def __init__(self) -> None:
        self.post_url = "https://paperswithcode.com/submit-paper"

    def insert(self, br: Browser) -> list:
        pass


class PapersWithCode:
    def __init__(self, login: bool) -> None:
        self.br = Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [
            ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        if login and self.login() == 200:
            self.is_login = True
        else:
            self.is_login = False

    def login(self) -> int:
        self.br.open("https://paperswithcode.com/accounts/login?next=/")
        self.br.select_form(nr=2)
        self.br.form['username'] = self.username
        self.br.form['password'] = self.password
        req = self.br.submit()
        return req.code

    def insert(self, element: PaperWithCodeElement) -> int:
        if not self.is_login:
            raise Exception("You must login first")

        return element.insert()
