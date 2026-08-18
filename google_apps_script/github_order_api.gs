const CONFIG = {
  SHEET_NAME: '',
  SECRET_PROPERTY: 'GITHUB_ORDER_SECRET',
  FIRST_DATA_ROW: 2,
  NOTIFICATION_SENT_COL: 19,
  NOTIFICATION_TIME_COL: 20
};

// GitHub calls this endpoint every 5 minutes.
function doGet(e) {
  if (!authorized_(e)) return json_({ ok: false, error: 'Unauthorized' });

  const sheet = getSheet_();
  const lastRow = sheet.getLastRow();
  if (lastRow < CONFIG.FIRST_DATA_ROW) return json_({ ok: true, orders: [] });

  const rows = sheet.getRange(CONFIG.FIRST_DATA_ROW, 1, lastRow - CONFIG.FIRST_DATA_ROW + 1, 20).getDisplayValues();
  const orders = [];

  rows.forEach((r, i) => {
    const orderId = r[0].trim();
    const sent = r[18].trim();
    if (!orderId || sent === 'YES') return;
    if (!r[3].trim() || !r[4].trim() || !r[8].trim()) return;

    orders.push({
      row: i + CONFIG.FIRST_DATA_ROW,
      order_id: r[0], date: r[1], time: r[2], customer_name: r[3], phone: r[4],
      full_address: r[5], district: r[6], area: r[7], product: r[8], quantity: r[9],
      unit_price: r[10], product_total: r[11], delivery_charge: r[12], grand_total: r[13],
      payment_method: r[14], transaction_id: r[15], order_notes: r[16], order_status: r[17]
    });
  });

  return json_({ ok: true, orders: orders });
}

// GitHub calls this after Telegram accepts the notification.
function doPost(e) {
  if (!authorized_(e)) return json_({ ok: false, error: 'Unauthorized' });

  let body;
  try { body = JSON.parse(e.postData.contents || '{}'); }
  catch (err) { return json_({ ok: false, error: 'Invalid JSON' }); }

  if (body.action !== 'mark_sent' || !Number.isInteger(body.row)) {
    return json_({ ok: false, error: 'Invalid request' });
  }

  const sheet = getSheet_();
  const row = body.row;
  if (row < CONFIG.FIRST_DATA_ROW || row > sheet.getLastRow()) {
    return json_({ ok: false, error: 'Invalid row' });
  }

  sheet.getRange(row, CONFIG.NOTIFICATION_SENT_COL).setValue('YES');
  sheet.getRange(row, CONFIG.NOTIFICATION_TIME_COL).setValue(new Date());
  SpreadsheetApp.flush();
  return json_({ ok: true, row: row });
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (CONFIG.SHEET_NAME) return ss.getSheetByName(CONFIG.SHEET_NAME);
  return ss.getSheets()[0];
}

function authorized_(e) {
  const secret = PropertiesService.getScriptProperties().getProperty(CONFIG.SECRET_PROPERTY);
  const supplied = e && e.parameter ? e.parameter.key : '';
  return !!secret && supplied === secret;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
