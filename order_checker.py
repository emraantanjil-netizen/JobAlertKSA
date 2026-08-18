import os
import requests

API_URL = os.environ["GOOGLE_SHEET_API_URL"].strip()
API_KEY = os.environ["GOOGLE_SHEET_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def api_get():
    r = requests.get(API_URL, params={"key": API_KEY}, timeout=30, allow_redirects=True)
    if r.status_code != 200:
        raise RuntimeError(f"Apps Script HTTP {r.status_code}: {r.text[:500]}")
    try:
        return r.json()
    except ValueError:
        raise RuntimeError(
            "Apps Script did not return JSON. "
            f"Final URL={r.url}\nResponse={r.text[:1000]}\n"
            "Deploy Apps Script as Web app: Execute as Me, Who has access Anyone, "
            "and use the /exec URL (not /dev). Also ensure the GitHub key matches "
            "GITHUB_ORDER_SECRET in Apps Script."
        )


def get_orders():
    data = api_get()
    if not data.get("ok"):
        raise RuntimeError(data.get("error", "Google Sheets API error"))
    return data.get("orders", [])


def send_telegram(order):
    text = (
        "🛍️ NEW ORDER RECEIVED\n\n"
        f"🆔 Order ID: #{order['order_id']}\n"
        f"📅 Date: {order['date']}\n"
        f"⏰ Time: {order['time']}\n\n"
        f"👤 Customer: {order['customer_name']}\n"
        f"📞 Phone: {order['phone']}\n"
        f"📍 District: {order['district']}\n"
        f"📍 Area: {order['area']}\n"
        f"🏠 Address: {order['full_address']}\n\n"
        f"📦 Product: {order['product']}\n"
        f"🔢 Quantity: {order['quantity']}\n"
        f"💰 Unit Price: ৳{order['unit_price']}\n"
        f"📦 Product Total: ৳{order['product_total']}\n"
        f"🚚 Delivery: ৳{order['delivery_charge']}\n"
        f"💵 GRAND TOTAL: ৳{order['grand_total']}\n\n"
        f"💳 Payment: {order['payment_method']}\n"
    )
    if order.get("transaction_id"):
        text += f"🧾 Transaction ID: {order['transaction_id']}\n"
    if order.get("order_notes"):
        text += f"📝 Notes: {order['order_notes']}\n"
    text += f"📊 Status: {order['order_status'] or 'NEW'}\n\n━━━━━━━━━━━━━━\n⚡ EMUORA ORDERS"

    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=30
    )
    r.raise_for_status()
    result = r.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram error: {result}")


def mark_sent(row):
    r = requests.post(
        API_URL, params={"key": API_KEY},
        json={"action": "mark_sent", "row": row}, timeout=30
    )
    if r.status_code != 200:
        raise RuntimeError(f"Could not mark row {row}: HTTP {r.status_code}: {r.text[:500]}")
    try:
        result = r.json()
    except ValueError:
        raise RuntimeError(f"Could not mark row {row}: Apps Script returned non-JSON: {r.text[:500]}")
    if not result.get("ok"):
        raise RuntimeError(result.get("error", "Could not mark order sent"))


def main():
    print(f"Checking Google Sheet API: {API_URL}")
    orders = get_orders()
    print(f"Found {len(orders)} unsent order(s).")
    for order in orders:
        send_telegram(order)
        mark_sent(order["row"])
        print(f"Sent order #{order['order_id']}")


if __name__ == "__main__":
    main()
