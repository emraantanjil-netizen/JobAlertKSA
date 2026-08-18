# Google Sheets Order Notifications

JobAlertKSA now includes a Google Apps Script integration for the order sheet.

## Sheet columns

The script expects these columns in this exact order:

1. Order ID
2. Date
3. Time
4. Customer Name
5. Phone
6. Full Address
7. District
8. Area
9. Product
10. Quantity
11. Unit Price
12. Product Total
13. Delivery Charge
14. Grand Total
15. Payment Method
16. Transaction ID
17. Order Notes
18. Order Status
19. Notification Sent
20. Notification Time

## Setup

1. Open the Google Sheet.
2. Go to **Extensions → Apps Script**.
3. Copy the contents of `google_apps_script/order_notifications.gs` into the Apps Script editor.
4. Open **Project Settings → Script Properties**.
5. Add:
   - `TELEGRAM_BOT_TOKEN` = your Telegram bot token
   - `TELEGRAM_CHAT_ID` = the chat ID that should receive order notifications
6. Save the project.
7. Run `setupOrderNotifications()` once from the Apps Script editor and authorize it.
8. Run `testTelegramNotification()` to confirm Telegram delivery.
9. Add a test order to row 2 of the sheet.

## Behavior

- A sufficiently complete new order sends an immediate Telegram notification.
- Column S is marked `YES` after successful delivery.
- Column T records the notification time.
- Editing the Order Status column after the first notification sends a status-update message.
- Other edits to an already-notified row do not create duplicate notifications.

## Security

Never put the Telegram bot token in the spreadsheet cells or public GitHub files. Keep it in Google Apps Script Script Properties and GitHub Actions Secrets where required.
