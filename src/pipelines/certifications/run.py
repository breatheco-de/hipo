import json

from src.utils.breathecode import get_specialties
from src.utils.printer import Printer
from prefect import task, flow
from src.services.redis_manager import redis_manager

printer = Printer(__file__)


# @task
# def create_live_documents(technology: str):
#     live_document_text = ""
#     assets = get_technology_assets(technology)

#     if len(assets) == 0:
#         printer.red(f"No assets found for technology {technology}")
#         return

#     # printer.yellow(f"EXAMPLE ASSET FOR TECH: {technology}:", assets[0])
#     # Get the ai context for the first asset
#     for asset in assets:
#         ai_context = get_ai_context(asset["id"])
#         ai_context = ai_context["ai_context"]
#         translations = asset.get("translations", {})
#         available_languages = list(translations.keys())

#         # Ignore the current language
#         available_languages = [
#             language for language in available_languages if language != asset["lang"]
#         ]

#         translations_text = ""
#         for language in available_languages:
#             url = make_url("EXERCISE", asset["translations"][language], language)

#             translations_text += f'- {language}: <a href="{url}">{url}</a>\n'

#         original_url = make_url("EXERCISE", asset["slug"], asset["lang"])
#         translations_text += (
#             f'- {asset["lang"]}: <a href="{original_url}">{original_url}</a>\n'
#         )
#         live_document_text += f"""
# <ASSET>


# <TITLE>
# {asset["title"]}
# </TITLE>
# <SLUG>
# {asset["slug"]}
# </SLUG>
# <URLS>
# {translations_text}
# </URLS>
# </ASSET>


# <AI CONTEXT>
# {ai_context}
# </AI CONTEXT>

# {config["separator"]}
# """

#     if len(live_document_text) == 0:
#         printer.red(f"No live document text found for technology {technology}")
#     else:
#         identificator = config["identificator"].replace("{technology}", technology)
#         redis_manager.set(identificator, live_document_text)
#         printer.green(
#             f"Live document for {technology} created in redis using key {identificator}"
#         )


@task
def get_certifications():
    _specialties = get_specialties()
    specialties = []
    for specialty in _specialties:
        specialties.append(
            {
                "name": specialty["name"],
                "slug": specialty["slug"],
                "description": specialty["description"],
            }
        )

    return specialties


@flow
def create_certifications_flow():
    specialties = get_certifications()
    DOCUMENT = f"""
## Which are the available certifications at 4Geeks?
{json.dumps(specialties, indent=4)}

---SEPARATOR---

## What are the prerequisites to get a certification?

To get a certification you need to complete all the exercises, projects, and lessons for the corresponding specialty.

---SEPARATOR---

## How are the certifications structured?

To obtain a certification you must finalize a course that contains quizzes, real-world projects, AI assistance and a final project F.

---SEPARATOR---

## What does the certification exam look like?

There is not an exam, you should finish the course to obtain a certification.

---SEPARATOR---

## How long does it take to complete a certification?

It depends on the specialty, but in general it takes 2-6 months to complete a certification.

---SEPARATOR---

## How much does a certification cost?

The price of a certification depends on the specialty.

---SEPARATOR---

## Are there official endorsements or accreditations?

Yes, there are our official partners:

### Educational Partners:
- **Miami Dade College** – Partner for full-stack, web development, and AI programs.
- **Inter-American Development Bank (IDB)** – Recognized 4Geeks as the designated coding school in Costa Rica and Uruguay.
- **UTEC** – Collaborating on full-stack development and AI/ML programs since 2021.
- **IESA** – Supporting high-quality coding education.

### Industry & Tech Partners:
- **Google Developers**
- **Facebook Developer Circle**
- **Women Who Code**
- **Shell Hacks**
- **Bloktech**
- **Startup Worldcamp**

### Workforce & Community Partners:
- **United Way Miami** – Partnered for the Miami Workforce Project.
- **Clark University** – Providing partial scholarships for unemployed and underemployed students.
- **Miami Tech Coalition** – Supporting tech education and workforce development.

### Hiring & Corporate Partners:
Our graduates have been hired by top companies such as:
- **Facebook**
- **Microsoft**
- **Apple**
- **Uber**
- **Twilio**
- **Telefonica**
- **National Geographic**
- **KPMG**
- **Ebay**

4Geeks Academy has built strong partnerships with global institutions, ensuring high-quality education and career opportunities for students worldwide.


---SEPARATOR---

## Is there a recertification process?

No, our certifications are not renewable.

---SEPARATOR---

## What career outcomes can I expect after getting a certification?

It depends on the specialty, but in general you should be able to get a job as a developer, machine learning engineer, front-end developer, back-end developer, full-stack developer, cybersecurity engineer, etc.

---SEPARATOR---

## What kind of support is offered during preparation?

- We offer a 1-on-1 mentorship program to help you prepare for the certification.
- AI assistance is available to help you with your projects 24/7.
- You will have access to a community of students and alumni to help you with your preparation.

---SEPARATOR---

## How is the exam graded?

There is not an exam, you should finish the course to obtain a certification.

---SEPARATOR---

## What is the process if I fail the exam?

There is not an exam, you should finish the course to obtain a certification.

---SEPARATOR---

## Are there community resources or study groups?

Yes, you can join our community of students and alumni to help you with your preparation in our Slack channel.

"""

    redis_manager.set("certifications", DOCUMENT)
    printer.green("Certifications document saved in redis")


if __name__ == "__main__":
    create_certifications_flow()
