// Проверка кол-ва ячеек в таблице
function checkQuantityCell() {

  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName('Настройки');
  let email = sheet.getRange('B3').getValue();
  let qCheckCells = sheet.getRange('B4').getValue();

  let cells = 0
  let sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  
  for (i in sheets) {
    let sheet = sheets[i];
    cells += sheet.getMaxRows() * sheet.getMaxColumns();
  };
  
  let check = 10000000 - cells;
  console.info(`Ячеек в таблице = ${cells}; Еще можно добавить ячеек = ${check}`);

  if (email !='' && check <= qCheckCells) {
    MailApp.sendEmail(email, `Заканчивается кол-во ячеек в таблице ${ss.getName()}`, `Еще можно добавить ${check} ячеек. Ссылка на таблицу = ${ss.getUrl()}`);
    console.log('Сообщеине с предупреждением о превышении лимита ячеек отправлено на почту');
  };

  return;
};