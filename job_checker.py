import os
import requests
from bs4 import BeautifulSoup

# ============================================================
# TELEGRAM SETTINGS
# ============================================================

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ============================================================
# EXPATRIATES JOBS PAGE
# ============================================================

URL = "https://www.expatriates.com/classifieds/saudi-arabia/jobs/?lang=en"

# ============================================================
# KEYWORDS
# ============================================================

KEYWORDS = [

    # Electrical
    "electrician",
    "electrical",
    "electrical technician",
    "electrical helper",
    "electric helper",
    "electrician helper",
    "electrical maintenance",
    "maintenance electrician",
    "industrial electrician",
    "building electrician",
    "construction electrician",
    "wireman",
    "wiring",
    "cable technician",
    "cable pulling",
    "cable installation",
    "electrical installation",
    "electrical supervisor",
    "electrical foreman",

    # HVAC / AC
    "ac technician",
    "ac technician helper",
    "air conditioning",
    "air conditioner",
    "hvac",
    "hvac technician",
    "hvac helper",
    "hvac technician helper",
    "refrigeration technician",
    "refrigeration",
    "chiller technician",
    "duct technician",
    "ducting",
    "ventilation",
    "mep",
    "mep technician",
    "mep helper",

    # Maintenance
    "maintenance",
    "maintenance technician",
    "maintenance helper",
    "maintenance worker",
    "building maintenance",
    "facility maintenance",
    "facility management",
    "facilities",
    "technician",
    "technical",
    "mechanic",
    "mechanical technician",
    "mechanical helper",

    # Construction
    "construction",
    "construction worker",
    "construction helper",
    "site worker",
    "site helper",
    "general worker",
    "general labor",
    "general labour",
    "labor",
    "labour",
    "skilled worker",
    "unskilled worker",
    "foreman",
    "site supervisor",
    "site assistant",
    "civil",
    "civil helper",
    "civil technician",
    "mason",
    "masonry",
    "carpenter",
    "carpentry",
    "steel fixer",
    "shuttering carpenter",
    "scaffolder",
    "scaffolding",
    "welder",
    "welding",
    "fabricator",
    "fabrication",
    "pipe fitter",
    "pipefitter",
    "plumber",
    "plumbing",
    "painter",

    # Warehouse / Logistics
    "warehouse",
    "warehouse worker",
    "warehouse helper",
    "warehouse assistant",
    "warehouse associate",
    "warehouse operator",
    "warehouse staff",
    "warehouse supervisor",
    "storekeeper",
    "store keeper",
    "store assistant",
    "store helper",
    "inventory",
    "inventory assistant",
    "inventory controller",
    "stock keeper",
    "stock controller",
    "logistics",
    "logistics assistant",
    "logistics associate",
    "logistics coordinator",
    "logistics helper",
    "logistics worker",
    "supply chain",
    "material handler",
    "material handling",
    "loader",
    "unloader",
    "loading",
    "unloading",
    "picker",
    "packer",
    "packing",
    "packing helper",
    "order picker",
    "fulfillment",
    "dispatch",
    "delivery assistant",

    # Hospitality
    "housekeeper",
    "housekeeping",
    "housekeeping attendant",
    "housekeeping staff",
    "room attendant",
    "room boy",
    "hotel worker",
    "hotel staff",
    "hotel attendant",
    "cleaner",
    "cleaning",
    "cleaning worker",
    "cleaning staff",
    "janitor",
    "steward",
    "kitchen helper",
    "kitchen assistant",
    "commis",
    "waiter",
    "waitress",
    "restaurant worker",
    "restaurant staff",
    "barista",
    "cafe worker",
    "catering",
    "catering helper",
    "food service",

    # General jobs
    "helper",
    "assistant",
    "worker",
    "staff",
    "operator",
    "operator helper",
    "office boy",
    "office assistant",
    "tea boy",
    "messenger",
    "attendant",
    "service worker",
    "support staff",
    "general helper",

    # Factory / Industrial
    "factory",
    "factory worker",
    "factory helper",
    "production",
    "production worker",
    "production operator",
    "machine operator",
    "machine operator helper",
    "industrial",
    "industrial worker",
    "manufacturing",
    "assembly",
    "assembly worker",
    "production helper",
    "quality control",
    "quality inspector",
    "packaging",
    "packaging worker",

    # Oil / Gas / Projects
    "oil and gas",
    "oil & gas",
    "oil gas",
    "petrochemical",
    "refinery",
    "pipeline",
    "pipeline worker",
    "pipeline technician",
    "project",
    "project worker",
    "shutdown",
    "turnaround",
    "maintenance project",
    "industrial project",
    "site technician",
    "project helper",

    # Safety
    "safety",
    "safety officer",
    "safety assistant",
    "safety supervisor",
    "hse",
    "hse assistant",
    "hse officer",

    # Drivers / Transport
    "driver",
    "light driver",
    "heavy driver",
    "delivery driver",
    "delivery",
    "truck driver",
    "bus driver",
    "forklift",
    "forklift operator",
    "forklift driver",

    # Retail / Sales
    "sales",
    "salesman",
    "sales assistant",
    "sales associate",
    "shop assistant",
    "shop worker",
    "retail",
    "retail worker",
    "cashier",
    "customer service",
    "customer service representative",

    # Office / Administration
    "data entry",
    "data entry operator",
    "office assistant",
    "admin assistant",
    "administrative assistant",
    "document controller",
    "receptionist",
    "reception",
    "clerk",
    "coordinator",

    # Broad job / hiring terms
    "immediate hiring",
    "immediate joining",
    "urgent hiring",
    "urgent requirement",
    "urgent vacancy",
    "vacancy",
    "job vacancy",
    "job opening",
    "hiring",
    "required",
    "requirement",
    "manpower",
    "manpower required",
    "staff required",
    "workers required",
    "workers wanted",
    "staff wanted",
    "job available",
    "employment",
    "career"
]


# ============================================================
# SEND TELEGRAM MESSAGE
# ============================================================

def send_telegram(message):

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False
        },
        timeout=30
    )

    print("Telegram response:")
    print(response.text)

    response.raise_for_status()


# ============================================================
# CHECK EXPATRIATES
# ============================================================

def check_expatriates():

    print("===================================")
    print("Saudi Job Alert")
    print("Checking Expatriates...")
    print("===================================")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:

        response = requests.get(
            URL,
            headers=headers,
            timeout=30
        )

        print("HTTP status:", response.status_code)

        response.raise_for_status()

    except Exception as error:

        print("ERROR while accessing Expatriates:")
        print(error)

        send_telegram(
            "⚠️ Saudi Job Alert\n\n"
            "Could not access Expatriates.com.\n\n"
            f"Error: {error}"
        )

        return

    # ========================================================
    # PARSE PAGE
    # ========================================================

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    if soup.title:

        page_title = soup.title.get_text(
            strip=True
        )

    else:

        page_title = "Unknown"

    print("Page title:", page_title)

    # Get all visible text
    page_text = soup.get_text(
        " ",
        strip=True
    ).lower()

    # ========================================================
    # FIND KEYWORDS
    # ========================================================

    matches = []

    for keyword in KEYWORDS:

        if keyword.lower() in page_text:

            matches.append(keyword)

    # Remove duplicates
    matches = list(dict.fromkeys(matches))

    print("-----------------------------------")
    print("Matching keywords:")

    if matches:

        for keyword in matches:

            print("✓", keyword)

    else:

        print("No matching keywords found.")

    print("-----------------------------------")

    # ========================================================
    # TELEGRAM MESSAGE
    # ========================================================

    message = (
        "🔎 SAUDI JOB ALERT\n\n"
        "Expatriates jobs page checked successfully.\n\n"
        f"🌐 Page: {page_title}\n"
        f"🔗 {URL}\n\n"
    )

    if matches:

        message += "🔑 KEYWORDS FOUND:\n\n"

        for keyword in matches[:30]:

            message += f"• {keyword}\n"

        if len(matches) > 30:

            message += (
                f"\n+ {len(matches) - 30} more matches"
            )

    else:

        message += "❌ No matching keywords found."

    message += "\n\n🤖 JobAlertKSA"

    send_telegram(message)

    print("Notification sent successfully.")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    check_expatriates()
