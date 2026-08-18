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
        raise RuntimeError(f"Apps Script did not return JSON. Final URL={r.url}\nResponse={r.text[:1000]}")


def get_orders():
    data = api_get()
    if not data.get("ok"):
        raise RuntimeError(data.get("error", "Google Sheets API error"))
    return data.get("orders", [])


def get_value(order, camel, snake=None, default=""):
    if camel in order:
        return order.get(camel, default)
    if snake and snake in order:
        return order.get(snake, default)
    return default


def send_telegram(order):
    order_id = get_value(order, "orderId", "order_id")
    text = (
        "🛍️ NEW ORDER RECEIVED\n\n"
        f"🆔 Order ID: #{order_id}\n"
        f"📅 Date: {get_value(order, 'date')}\n"
        f"⏰ Time: {get_value(order, 'time')}\n\n"
        f"👤 Customer: {get_value(order, 'customerName', 'customer_name')}\n"
        f"📞 Phone: {get_value(order, 'phone')}\n"
        f"📍 District: {get_value(order, 'district')}\n"
        f"📍 Area: {get_value(order, 'area')}\n"
        f"🏠 Address: {get_value(order, 'fullAddress', 'full_address')}\n\n"
        f"📦 Product: {get_value(order, 'product')}\n"
        f"🔢 Quantity: {get_value(order, 'quantity')}\n"
        f"💰 Unit Price: ৳{get_value(order, 'unitPrice', 'unit_price')}\n"
        f"📦 Product Total: ৳{get_value(order, 'productTotal', 'product_total')}\n"
        f"🚚 Delivery: ৳{get_value(order, 'deliveryCharge', 'delivery_charge')}\n"
        f"💵 GRAND TOTAL: ৳{get_value(order, 'grandTotal', 'grand_total')}\n\n"
        f"💳 Payment: {get_value(order, 'paymentMethod', 'payment_method')}\n"
    )

    transaction_id = get_value(order, "transactionId", "transaction_id")
    notes = get_value(order, "orderNotes", "order_notes")
    status = get_value(order, "orderStatus", "order_status", "NEW") or "NEW"

    if transaction_id:
        text += f"🧾 Transaction ID: {transaction_id}\n"
    if notes:
        text += f"📝 Notes: {notes}\n"
    text += f"📊 Status: {status}\n\n━━━━━━━━━━━━━━\n⚡ EMUORA ORDERS"

    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=30,
    )
    r.raise_for_status()
    result = r.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram error: {result}")


def mark_sent(order):
    row = order.get("sheetRow", order.get("row"))
    order_id = get_value(order, "orderId", "order_id", "?")
    if not row:
        raise RuntimeError(f"Order {order_id} has no sheet row")

    r = requests.post(
        API_URL,
        params={"key": API_KEY},
        json={"sheetRow": row},
        timeout=30,
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
        order_id = get_value(order, "orderId", "order_id", "?")
        print(f"Processing order #{order_id}...")
        send_telegram(order)
        mark_sent(order)
        print(f"Sent order #{order_id} successfully.")


if __name__ == "__main__":
    main()
