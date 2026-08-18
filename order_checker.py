import os
import requests

API_URL = os.environ["GOOGLE_SHEET_API_URL"]
API_KEY = os.environ["GOOGLE_SHEET_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def get_orders():
    r = requests.get(API_URL, params={"key": API_KEY}, timeout=30)
    r.raise_for_status()
    data = r.json()
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

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=30)
    r.raise_for_status()
    result = r.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram error: {result}")


def mark_sent(row):
    r = requests.post(
        API_URL,
        params={"key": API_KEY},
        json={"action": "mark_sent", "row": row},
        timeout=30,
    )
    r.raise_for_status()
    result = r.json()
    if not result.get("ok"):
        raise RuntimeError(result.get("error", "Could not mark order sent"))


def main():
    orders = get_orders()
    print(f"Found {len(orders)} unsent order(s).")
    for order in orders:
        send_telegram(order)
        mark_sent(order["row"])
        print(f"Sent order #{order['order_id']}")


if __name__ == "__main__":
    main()
