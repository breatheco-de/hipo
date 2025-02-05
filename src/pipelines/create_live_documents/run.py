from src.utils.breathecode import (
    get_technology_assets,
    get_ai_context,
    get_academy_technologies,
    make_url,
)
from src.utils.printer import Printer
from src.services.redis_manager import redis_manager
from prefect import task, flow

config = {"identificator": "exercises-{technology}", "separator": "---SEPARATOR---"}

printer = Printer(__file__)


@task
def create_live_documents(technology: str):
    live_document_text = ""
    assets = get_technology_assets(technology)

    if len(assets) == 0:
        printer.red(f"No assets found for technology {technology}")
        return

    # printer.yellow(f"EXAMPLE ASSET FOR TECH: {technology}:", assets[0])
    # Get the ai context for the first asset
    for asset in assets:
        ai_context = get_ai_context(asset["id"])
        ai_context = ai_context["ai_context"]
        translations = asset.get("translations", {})
        available_languages = list(translations.keys())
        # Ignore the us translation
        available_languages = [
            language for language in available_languages if language != "us"
        ]

        translations_text = ""
        for language in available_languages:
            url = make_url("EXERCISE", asset["translations"][language], language)
           
            translations_text += f'- {language}: <a href="{url}">{url}</a>\n'

        english_url = make_url("EXERCISE", asset["slug"])
        translations_text += f'- us: <a href="{english_url}">{english_url}</a>\n'
        live_document_text += f"""
<ASSET>

<TITLE>
{asset["title"]}
</TITLE>
<SLUG>
{asset["slug"]}
</SLUG>
<URLS>
{translations_text}
</URLS>
</ASSET>



<AI CONTEXT>
{ai_context}
</AI CONTEXT>

{config["separator"]}
"""

    if len(live_document_text) == 0:
        printer.red(f"No live document text found for technology {technology}")
    else:
        identificator = config["identificator"].replace("{technology}", technology)
        redis_manager.set(identificator, live_document_text)
        printer.green(
            f"Live document for {technology} created in redis using key {identificator}"
        )


@task
def decide_technologies():
    technologies = get_academy_technologies()
    priorities = []
    for technology in technologies:
        if technology["sort_priority"] == 1:
            priorities.append(technology["slug"])

    return priorities


@flow
def create_live_documents_flow():
    priorities = decide_technologies()
    for priority in priorities:
        create_live_documents(priority)


if __name__ == "__main__":
    create_live_documents_flow()
