/**
 * JobAlertKSA - Google Sheets Order Notifications
 *
 * Sheet columns (exact order):
 * A Order ID
 * B Date
 * C Time
 * D Customer Name
 * E Phone
 * F Full Address
 * G District
 * H Area
 * I Product
 * J Quantity
 * K Unit Price
 * L Product Total
 * M Delivery Charge
 * N Grand Total
 * O Payment Method
 * P Transaction ID
 * Q Order Notes
 * R Order Status
 * S Notification Sent
 * T Notification Time
 *
 * IMPORTANT:
 * 1. Put TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in Script Properties.
 * 2. Run setupOrderNotifications() once manually to create the installable trigger.
 * 3. The trigger only processes rows edited in the configured sheet.
 */

const CONFIG = {
  SHEET_NAME: '', // Leave blank to use the sheet where the trigger fires.
  HEADER_ROW: 1,
  FIRST_DATA_ROW: 2,
  NOTIFICATION_SENT_COL: 19, // S
  NOTIFICATION_TIME_COL: 20, // T
  STATUS_COL: 18, // R
  ORDER_ID_COL: 1,
  TELEGRAM_TOKEN_PROPERTY: 'TELEGRAM_BOT_TOKEN',
  TELEGRAM_CHAT_ID_PROPERTY: 'TELEGRAM_CHAT_ID'
};

function setupOrderNotifications() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Remove duplicate triggers created by previous setup attempts.
  ScriptApp.getProjectTriggers().forEach(trigger => {
    if (trigger.getHandlerFunction() === 'onOrderEdit') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  ScriptApp.newTrigger('onOrderEdit')
    .forSpreadsheet(ss)
    .onEdit()
    .create();

  Logger.log('Order notification trigger created successfully.');
}

function onOrderEdit(e) {
  if (!e || !e.range) return;

  const sheet = e.range.getSheet();
  const row = e.range.getRow();
  const col = e.range.getColumn();

  if (row < CONFIG.FIRST_DATA_ROW) return;
  if (CONFIG.SHEET_NAME && sheet.getName() !== CONFIG.SHEET_NAME) return;

  // Only react to edits inside the order table A:T.
  if (col > CONFIG.NOTIFICATION_TIME_COL) return;

  processOrderRow_(sheet, row, col);
}

function processOrderRow_(sheet, row, editedCol) {
  const values = sheet.getRange(row, 1, 1, CONFIG.NOTIFICATION_TIME_COL).getDisplayValues()[0];

  const orderId = values[CONFIG.ORDER_ID_COL - 1].trim();
  const customerName = values[3].trim();
  const phone = values[4].trim();
  const product = values[8].trim();
  const quantity = values[9].trim();
  const status = values[CONFIG.STATUS_COL - 1].trim() || 'NEW';
  const notificationSent = values[CONFIG.NOTIFICATION_SENT_COL - 1].trim();

  // Do nothing until the row looks like a real order.
  if (!orderId || !customerName || !phone || !product) return;

  // If the order is already marked as notified, only send a status-change
  // notification when the user edits the Order Status column.
  if (notificationSent && editedCol !== CONFIG.STATUS_COL) return;

  const message = buildOrderMessage_(values, editedCol === CONFIG.STATUS_COL && notificationSent);
  const result = sendTelegram_(message);

  if (result.ok) {
    sheet.getRange(row, CONFIG.NOTIFICATION_SENT_COL).setValue('YES');
    sheet.getRange(row, CONFIG.NOTIFICATION_TIME_COL).setValue(new Date());
  } else {
    throw new Error('Telegram notification failed: ' + JSON.stringify(result));
  }
}

function buildOrderMessage_(v, statusUpdate) {
  const orderId = v[0];
  const date = v[1];
  const time = v[2];
  const customer = v[3];
  const phone = v[4];
  const fullAddress = v[5];
  const district = v[6];
  const area = v[7];
  const product = v[8];
  const quantity = v[9];
  const unitPrice = v[10];
  const productTotal = v[11];
  const delivery = v[12];
  const grandTotal = v[13];
  const payment = v[14];
  const transactionId = v[15];
  const notes = v[16];
  const status = v[17] || 'NEW';

  let text = statusUpdate
    ? '🔄 ORDER STATUS UPDATED\n\n'
    : '🛍️ NEW ORDER RECEIVED\n\n';

  text += '🆔 Order ID: #' + safe_(orderId) + '\n';
  text += '📅 Date: ' + safe_(date) + '\n';
  text += '⏰ Time: ' + safe_(time) + '\n\n';

  text += '👤 Customer: ' + safe_(customer) + '\n';
  text += '📞 Phone: ' + safe_(phone) + '\n';
  text += '📍 District: ' + safe_(district) + '\n';
  text += '📍 Area: ' + safe_(area) + '\n';
  text += '🏠 Address: ' + safe_(fullAddress) + '\n\n';

  text += '📦 Product: ' + safe_(product) + '\n';
  text += '🔢 Quantity: ' + safe_(quantity) + '\n';
  text += '💰 Unit Price: ৳' + safe_(unitPrice) + '\n';
  text += '📦 Product Total: ৳' + safe_(productTotal) + '\n';
  text += '🚚 Delivery: ৳' + safe_(delivery) + '\n';
  text += '💵 GRAND TOTAL: ৳' + safe_(grandTotal) + '\n\n';

  text += '💳 Payment: ' + safe_(payment) + '\n';
  if (transactionId) text += '🧾 Transaction ID: ' + safe_(transactionId) + '\n';
  if (notes) text += '📝 Notes: ' + safe_(notes) + '\n';
  text += '📊 Status: ' + safe_(status) + '\n\n';
  text += '━━━━━━━━━━━━━━\n';
  text += '⚡ EMUORA ORDERS';

  return text;
}

function sendTelegram_(message) {
  const props = PropertiesService.getScriptProperties();
  const token = props.getProperty(CONFIG.TELEGRAM_TOKEN_PROPERTY);
  const chatId = props.getProperty(CONFIG.TELEGRAM_CHAT_ID_PROPERTY);

  if (!token || !chatId) {
    throw new Error('Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in Script Properties.');
  }

  const url = 'https://api.telegram.org/bot' + token + '/sendMessage';
  const response = UrlFetchApp.fetch(url, {
    method: 'post',
    payload: {
      chat_id: chatId,
      text: message,
      disable_web_page_preview: 'true'
    },
    muteHttpExceptions: true
  });

  const body = response.getContentText();
  let parsed;
  try {
    parsed = JSON.parse(body);
  } catch (err) {
    parsed = { ok: false, raw: body };
  }

  if (!parsed.ok) {
    console.error(body);
  }

  return parsed;
}

function testTelegramNotification() {
  const message = '✅ JobAlertKSA order notification test\n\nTelegram connection is working.';
  const result = sendTelegram_(message);
  Logger.log(JSON.stringify(result));
}

function safe_(value) {
  return String(value || '').trim();
}
