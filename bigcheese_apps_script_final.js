/**
 * Big Cheese Languages — Google Sheets CRM + Telegram notifications
 * Works with:
 * 1) Google Forms submit trigger: onFormSubmit(e)
 * 2) Telegram bot webhook into Sheets: doPost(e)
 *
 * Recommended Script Properties:
 * TELEGRAM_BOT_TOKEN = token from BotFather
 * TELEGRAM_CHAT_ID = 1175970327
 */

const MANAGER_EMAILS = ["i@rusovich-top.ru", "granatmediar@gmail.com"];

const CONFIG = {
  "RU Form Responses": {
    targetSheet: "RU Leads",
    flow: "RU",
    status: "Новая заявка"
  },
  "EN Form Responses": {
    targetSheet: "EN Leads",
    flow: "EN",
    status: "New lead"
  }
};

function onFormSubmit(e) {
  const sourceSheet = e.range.getSheet();
  const sourceSheetName = sourceSheet.getName();
  const config = CONFIG[sourceSheetName];
  if (!config) return;

  const row = e.range.getRow();
  const lastColumn = sourceSheet.getLastColumn();
  const values = sourceSheet.getRange(row, 1, 1, lastColumn).getValues()[0];

  const timestamp = values[0] || new Date();
  const name = values[1] || "";
  const contact = values[2] || "";
  const email = values[3] || "";
  const goal = values[4] || "";
  const languages = values[5] || "";

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const targetSheet = ss.getSheetByName(config.targetSheet);
  if (!targetSheet) throw new Error("Target sheet not found: " + config.targetSheet);

  const newRow = [
    timestamp,
    name,
    contact,
    email,
    languages,
    goal,
    "",
    "",
    "",
    config.status,
    "Google Form",
    ""
  ];

  targetSheet.appendRow(newRow);

  const lead = {
    timestamp,
    name,
    contact,
    email,
    goal,
    languages,
    source: "Google Form",
    status: config.status
  };

  sendLeadEmailNotification(config.flow, lead);
  sendLeadTelegramNotification(config.flow, lead);
}

function doPost(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("Bot Leads");
  if (!sheet) throw new Error("Sheet 'Bot Leads' not found");

  const data = JSON.parse(e.postData.contents || "{}");
  const timestamp = new Date();

  sheet.appendRow([
    timestamp,
    data.name || "",
    data.username || "",
    data.telegram_id || "",
    data.lang || "",
    data.segment || "",
    data.lead_type || "",
    data.source || "Telegram Bot",
    data.status || "New bot lead",
    data.comment || ""
  ]);

  sendBotLeadTelegramNotification(data);

  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok" }))
    .setMimeType(ContentService.MimeType.JSON);
}

function sendLeadEmailNotification(flow, lead) {
  const subject = flow === "RU"
    ? "Новая заявка Big Cheese Languages"
    : "New lead — Big Cheese Languages";

  const message = flow === "RU"
    ? `Новая заявка Big Cheese Languages\n\nИмя: ${lead.name}\nКонтакт: ${lead.contact}\nEmail: ${lead.email}\nЦель: ${lead.goal}\nЯзык(и): ${lead.languages}\nДата заявки: ${lead.timestamp}\n\nПроверьте вкладку RU Leads и свяжитесь с клиентом.`
    : `New lead — Big Cheese Languages\n\nName: ${lead.name}\nContact: ${lead.contact}\nEmail: ${lead.email}\nGoal: ${lead.goal}\nLanguage(s): ${lead.languages}\nRequest date: ${lead.timestamp}\n\nPlease check the EN Leads sheet and contact the client.`;

  MailApp.sendEmail(MANAGER_EMAILS.join(","), subject, message);
}

function sendLeadTelegramNotification(flow, lead) {
  const token = getTelegramToken_();
  const chatId = getTelegramChatId_();
  if (!token || !chatId) return;

  const text = flow === "RU"
    ? `🟡 Новая заявка Big Cheese Languages\n\n👤 Имя: ${lead.name || "-"}\n📱 Контакт: ${lead.contact || "-"}\n📧 Email: ${lead.email || "-"}\n🎯 Цель: ${lead.goal || "-"}\n🌐 Язык(и): ${lead.languages || "-"}\n🕘 Дата заявки: ${lead.timestamp || "-"}\n\nПроверьте вкладку RU Leads и свяжитесь с клиентом.`
    : `🟡 New lead — Big Cheese Languages\n\n👤 Name: ${lead.name || "-"}\n📱 Contact: ${lead.contact || "-"}\n📧 Email: ${lead.email || "-"}\n🎯 Goal: ${lead.goal || "-"}\n🌐 Language(s): ${lead.languages || "-"}\n🕘 Request date: ${lead.timestamp || "-"}\n\nPlease check the EN Leads sheet and contact the client.`;

  sendTelegram_(token, chatId, text);
}

function sendBotLeadTelegramNotification(data) {
  const token = getTelegramToken_();
  const chatId = getTelegramChatId_();
  if (!token || !chatId) return;

  const text = `🤖 Новая заявка из Telegram-бота!\n\n👤 Имя: ${data.name || "-"}\n💬 Username: ${data.username || "-"}\n🆔 Telegram ID: ${data.telegram_id || "-"}\n🌐 Язык интерфейса: ${data.lang || "-"}\n🎯 Сегмент: ${data.segment || "-"}\n📌 Тип заявки: ${data.lead_type || "-"}\n💬 Комментарий: ${data.comment || "-"}\n\nИсточник: Telegram Bot`;

  sendTelegram_(token, chatId, text);
}

function sendTelegram_(token, chatId, text) {
  const url = "https://api.telegram.org/bot" + token + "/sendMessage";
  const payload = { chat_id: chatId, text: text };
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };
  UrlFetchApp.fetch(url, options);
}

function getTelegramToken_() {
  return PropertiesService.getScriptProperties().getProperty("TELEGRAM_BOT_TOKEN") || "";
}

function getTelegramChatId_() {
  return PropertiesService.getScriptProperties().getProperty("TELEGRAM_CHAT_ID") || "1175970327";
}
