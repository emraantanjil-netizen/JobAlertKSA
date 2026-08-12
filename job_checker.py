import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://www.expatriates.com/classifieds/saudi-arabia/jobs/?lang=en"

KEYWORDS = [
    # Electrical
    "electrician", "electrical", "electrical technician",
    "electrical helper", "electric helper", "electrician helper",
    "electrical maintenance", "maintenance electrician",
    "industrial electrician", "building electrician",
    "construction electrician", "wireman", "wiring",
    "cable technician", "cable pulling", "cable installation",
    "electrical installation", "electrical supervisor",
    "electrical foreman",

    # HVAC / AC
    "ac technician", "ac technician helper", "air conditioning",
    "air conditioner", "hvac", "hvac technician", "hvac helper",
    "refrigeration technician", "refrigeration", "chiller technician",
    "duct technician", "ducting", "ventilation", "mep",
    "mep technician", "mep helper",

    # Maintenance
    "maintenance", "maintenance technician", "maintenance helper",
    "maintenance worker", "building maintenance",
    "facility maintenance", "facility management", "facilities",
    "technician", "technical", "mechanic", "mechanical technician",
    "mechanical helper",

    # Construction
    "construction", "construction worker", "construction helper",
    "site worker", "site helper", "general worker", "general labor",
    "labour", "labor", "skilled worker", "unskilled worker",
    "foreman", "site supervisor", "site assistant", "civil",
    "civil helper", "civil technician", "mason", "masonry",
    "carpenter", "carpentry", "steel fixer", "shuttering carpenter",
    "scaffolder", "scaffolding", "welder", "welding", "fabricator",
    "fabrication", "pipe fitter", "pipefitter", "plumber",
    "plumbing", "painter",

    # Warehouse / Logistics
    "warehouse", "warehouse worker", "warehouse helper",
    "warehouse assistant", "warehouse associate", "warehouse operator",
    "warehouse staff", "warehouse supervisor", "storekeeper",
    "store keeper", "store assistant", "store helper", "inventory",
    "inventory assistant", "inventory controller", "stock keeper",
    "stock controller", "logistics", "logistics assistant",
    "logistics associate", "logistics coordinator", "logistics helper",
    "logistics worker", "supply chain", "material handler",
    "material handling", "loader", "unloader", "loading",
    "unloading", "picker", "packer", "packing", "packing helper",
    "order picker", "fulfillment", "dispatch", "delivery assistant",

    # Hospitality
    "housekeeper", "housekeeping", "housekeeping attendant",
    "housekeeping staff", "room attendant", "room boy",
    "hotel worker", "hotel staff", "hotel attendant", "cleaner",
    "cleaning", "cleaning worker", "cleaning staff", "janitor",
    "steward", "kitchen helper", "kitchen assistant", "commis",
    "waiter", "waitress", "restaurant worker", "restaurant staff",
    "barista", "cafe worker", "catering", "catering helper",
    "food service",

    # General jobs
    "helper", "assistant", "worker", "staff", "operator",
    "operator helper", "office boy", "office assistant",
    "tea boy", "messenger", "attendant", "service worker",
    "support staff", "general helper",

    # Factory / Industrial
    "factory", "factory worker", "factory helper", "production",
    "production worker", "production operator", "machine operator",
    "machine operator helper", "industrial", "industrial worker",
    "manufacturing", "assembly", "assembly worker",
    "production helper", "quality control", "quality inspector",
    "packaging", "packaging worker",

    # Oil & Gas / Projects
    "oil and gas", "oil & gas", "oil gas", "petrochemical",
    "refinery", "pipeline", "pipeline worker", "pipeline technician",
    "project", "project worker", "shutdown", "turnaround",
    "maintenance project", "industrial project", "site technician",
    "project helper",

    # Safety
    "safety", "safety officer", "safety assistant",
    "safety supervisor", "hse", "hse assistant", "hse officer",

    # Drivers / Transport
    "driver", "light driver", "heavy driver", "delivery driver",
    "delivery", "truck driver", "bus driver", "forklift",
    "forklift operator", "forklift driver",

    # Retail / Sales
    "sales", "salesman", "sales assistant", "sales associate",
    "shop assistant", "shop worker", "retail", "retail worker",
    "cashier", "customer service",
    "customer service representative",

    # Office / Admin
    "data entry", "data entry operator", "office assistant",
    "admin assistant", "administrative assistant",
    "document controller", "receptionist", "reception",
    "clerk", "coordinator",

    # Broad opportunity terms
    "immediate hiring", "immediate joining", "urgent hiring",
    "urgent requirement", "urgent vacancy", "vacancy",
    "job vacancy", "job opening", "hiring", "required",
    "requirement", "manpower", "manpower required",
    "staff required", "workers required", "workers wanted",
    "staff wanted", "job available", "employment", "career"
]


def send_telegram(message):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        api_url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False
        },
        timeout=30
    )

    response.raise_for_status()


def main():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    print("Checking Expatriates...")

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    page_text = soup.get_text(
        " ",
        strip=True
    ).lower()

    print("Page downloaded successfully.")

    print(
        "Page title:",
        soup.title.get_text(strip=True)
        if soup.title else "None"
    )

    # Find matching keywords
    matches = []

    for keyword in KEYWORDS:
        if keyword.lower() in page_text:
            matches.append(keyword)

    print("Matching keywords:")

    if matches:
        for keyword in matches:
            print("-", keyword)
    else:
        print("No matching keywords found.")

    # Telegram test message
    message = (
        "🔎 Saudi Job Alert\n\n"
        "Expatriates jobs page checked successfully.\n\n"
    )

    if matches:
        message += "🔑 Keywords found:\n"

        # Limit message length
        for keyword in matches[:20]:
            message += f"• {keyword}\n"

        if len(matches) > 20:
            message += f"\n+ {len(matches) - 20} more matches"

    else:
        message += "No matching keywords found."

    send_telegram(message)

    print("Telegram notification sent.")


if __name__ == "__main__":
    main()    "site worker", "site helper", "general worker", "general labor",
    "labour", "labor", "skilled worker", "unskilled worker",
    "foreman", "site supervisor", "site assistant", "civil",
    "civil helper", "civil technician", "mason", "masonry",
    "carpenter", "carpentry", "steel fixer", "shuttering carpenter",
    "scaffolder", "scaffolding", "welder", "welding", "fabricator",
    "fabrication", "pipe fitter", "pipefitter", "plumber",
    "plumbing", "painter",

    # Warehouse / Logistics
    "warehouse", "warehouse worker", "warehouse helper",
    "warehouse assistant", "warehouse associate", "warehouse operator",
    "warehouse staff", "warehouse supervisor", "storekeeper",
    "store keeper", "store assistant", "store helper", "inventory",
    "inventory assistant", "inventory controller", "stock keeper",
    "stock controller", "logistics", "logistics assistant",
    "logistics associate", "logistics coordinator", "logistics helper",
    "logistics worker", "supply chain", "material handler",
    "material handling", "loader", "unloader", "loading",
    "unloading", "picker", "packer", "packing", "packing helper",
    "order picker", "fulfillment", "dispatch", "delivery assistant",

    # Hospitality
    "housekeeper", "housekeeping", "housekeeping attendant",
    "housekeeping staff", "room attendant", "room boy",
    "hotel worker", "hotel staff", "hotel attendant", "cleaner",
    "cleaning", "cleaning worker", "cleaning staff", "janitor",
    "steward", "kitchen helper", "kitchen assistant", "commis",
    "waiter", "waitress", "restaurant worker", "restaurant staff",
    "barista", "cafe worker", "catering", "catering helper",
    "food service",

    # General jobs
    "helper", "assistant", "worker", "staff", "operator",
    "operator helper", "office boy", "office assistant",
    "tea boy", "messenger", "attendant", "service worker",
    "support staff", "general helper",

    # Factory / Industrial
    "factory", "factory worker", "factory helper", "production",
    "production worker", "production operator", "machine operator",
    "machine operator helper", "industrial", "industrial worker",
    "manufacturing", "assembly", "assembly worker",
    "production helper", "quality control", "quality inspector",
    "packaging", "packaging worker",

    # Oil & Gas / Projects
    "oil and gas", "oil & gas", "oil gas", "petrochemical",
    "refinery", "pipeline", "pipeline worker", "pipeline technician",
    "project", "project worker", "shutdown", "turnaround",
    "maintenance project", "industrial project", "site technician",
    "project helper",

    # Safety
    "safety", "safety officer", "safety assistant",
    "safety supervisor", "hse", "hse assistant", "hse officer",

    # Drivers / Transport
    "driver", "light driver", "heavy driver", "delivery driver",
    "delivery", "truck driver", "bus driver", "forklift",
    "forklift operator", "forklift driver",

    # Retail / Sales
    "sales", "salesman", "sales assistant", "sales associate",
    "shop assistant", "shop worker", "retail", "retail worker",
    "cashier", "customer service",
    "customer service representative",

    # Office / Admin
    "data entry", "data entry operator", "office assistant",
    "admin assistant", "administrative assistant",
    "document controller", "receptionist", "reception",
    "clerk", "coordinator",

    # Broad opportunity terms
    "immediate hiring", "immediate joining", "urgent hiring",
    "urgent requirement", "urgent vacancy", "vacancy",
    "job vacancy", "job opening", "hiring", "required",
    "requirement", "manpower", "manpower required",
    "staff required", "workers required", "workers wanted",
    "staff wanted", "job available", "employment", "career"
]


def send_telegram
