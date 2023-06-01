// Устанавливает чекбоксы API_KEY в false  
function startGetSalesWB() {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let apiKEY = ss.getSheetByName('API_KEY');
  apiKEY.getRange('D2:D').clear();
  apiKEY.getRange('D2:D').clearNote();
  console.info('startGetSalesWB', `Все чекбоксы API_KEY установлены в положения FALSE`);
  
  return;
};


// Функция запуска
function launchGetSalesWB() {
  console.time('Время выполнения');

  try { // Обработка ошибок
    var lock = LockService.getDocumentLock(); // Блокировка не позволяющая любому пользователю текущего документа одновременно запускать раздел кода.
    lock.waitLock(0); // Получим блокировку
  } catch (err) { // Если ошибка, блокировка не получена
    console.error('launchGetSalesWB', `Блокировка не получена. Ошибка = ${err.message}`);
    console.timeEnd('Время выполнения');
    return;
  };

  let ss = SpreadsheetApp.getActiveSpreadsheet();

  let sheetSettings = ss.getSheetByName('Настройки');
  let gmt = sheetSettings.getRange('B1').getValue();
  let qDays = sheetSettings.getRange('B2').getValue();

  let apiKEY = ss.getSheetByName('API_KEY');
  let dataKEY = apiKEY.getDataRange().getValues();
  dataKEY.splice(0, 1); // Удалим заголовок

  for (let i = 0; i < dataKEY.length; i++) {
    let use = dataKEY[i][0];
    if (!use) continue;

    let status = dataKEY[i][3];
    if (status) continue; // Если статус тру

    let key = dataKEY[i][1]; // АпиКей
    let nameCompany = dataKEY[i][2]; // Название ЛК, оно же название листа для данных выгрузки
    console.info('launchGetSalesWB', `Название ЛК = ${nameCompany}`);

    // Получим данные с ВБ и установим в выгрузку
    getDATA_WB(ss, key, qDays, gmt, nameCompany); // Длинна массива с данными
    let numRow = i + 2; // Номер СТРОКИ В ТАБЛИЦЕ
    apiKEY.getRange(numRow, 4).setValue(true).setNote(Utilities.formatDate(new Date(), "GMT+3", "dd.MM.yyyy HH:mm:ss '(GMT+3)'"));

    lock.releaseLock(); // Снимаем блокировку
    console.timeEnd('Время выполнения');

    return {'repeat': true};
  };

  lock.releaseLock(); // Снимаем блокировку
  console.info('launchGetSalesWB', 'Все функции успешно выполнены. Цикл завершен!');
  console.timeEnd('Время выполнения');

  return {'repeat': false};
};


// Получаем данные по апи с WB
function getDATA_WB(ss, key, qDays, gmt, nameCompany) { // flag - смотри коммент ниже!!!
  let sheet = ss.getSheetByName(nameCompany);
  let arrayDataFrom = getRow_dateFrom(sheet, qDays, gmt);
  let dateFrom = arrayDataFrom[0];
  if (dateFrom) dateFrom = Utilities.formatDate(dateFrom, "GMT+3", "yyyy-MM-dd'T'HH:mm:ss");
  else dateFrom = '2000-01-01'; // Если dateFrom не определена в таблице, то выгружаем все что доступно от WB
  let rowDateFrom = arrayDataFrom[1];
  if (!rowDateFrom) rowDateFrom = 1;
  console.info('getDATA_WB', `Дата для запроса (dateFrom) = ${dateFrom}; Строка с датой для запроса (rowDateFrom) = ${rowDateFrom}`);

  
  let data = [];
  do {
    let req = getSalesWB(key, dateFrom, gmt);
    let data$ = req.data;
    data = data.concat(data$);
    var dataLength = req.dataLength;
    if (dataLength > 0) dateFrom = data$[data$.length - 1][1]; // Если получены не все данные, то переназначим dateFrom для новго запроса
    console.info('getDATA_WB', `Получено данных от WB за один запрос (dataLength) = ${dataLength}`); 
  } while (dataLength > 0);


  // Если данных с WB нет
  if (data.length == 0) {
    console.info('getDATA_WB', `Нет новых данных для установки в таблицу`); 
    return;
  };
    

  // Установим данные в таблицу;
  console.info('getDATA_WB',`Строка начала установки данных = ${rowDateFrom + 1}`);

  console.time('Установка данных в таблицу');
  SpreadsheetApp.flush();
  
  let clearRange = sheet.getRange(`${rowDateFrom + 1}:${sheet.getMaxRows()}`);
  clearRange.clearContent(); // Очистим строки от rowDateFrom + 1 до конца листа
  console.info('getDATA_WB',`Старые значения за ${qDays} дней удалены, диапазон очистки = ${clearRange.getA1Notation()}`);
  SpreadsheetApp.flush();

  // API Sheets
  let dataRange = sheet.getRange(rowDateFrom + 1, 1, data.length, data[0].length);
  let request = {
    'majorDimension': 'ROWS',
    'values': data
  };

  let dop_arrgs = {
    //'insertDataOption': 'OVERWRITE', // Использовать с Sheets.Spreadsheets.Values.append
    'valueInputOption': 'USER_ENTERED',
  };

  let ssId = ss.getId();
  let append_range = sheet.getName() + '!' + dataRange.getA1Notation();

  Sheets.Spreadsheets.Values.update(request, ssId, append_range, dop_arrgs);
  console.timeEnd('Установка данных в таблицу');
  console.info('Данные с WB загружены и установлены на лист "Выгрузка"');

  return;
};



// Запрос в  WB
function getSalesWB(key, dateFrom, gmt) {
  // Запрашиваем данные в WB
  let responseCode;
  while (responseCode != 200){
    try {
      let url = `https://statistics-api.wildberries.ru/api/v1/supplier/sales?&flag=0&dateFrom=${dateFrom}`; // гггг-мм-дд
      let params = {
        'headers': {
          'Authorization': key
        }
      };
      var res = UrlFetchApp.fetch(url, params);
      responseCode = res.getResponseCode();
      console.info('getSalesWB', `Запрос в WB (responseCode) = ${responseCode}`);
    } catch (err){
      console.warn('getSalesWB', `WB не ответил, повтор запроса через 15 сек. Ошибка = ${err.message}`);
      Utilities.sleep(15000);
    };
  };

  let data = []; // Массив для установки в таблицу

  let contentText = res.getContentText();

  let json;
  try {
    json = JSON.parse(contentText); // Если ошибка, например длинный ответ и гугл его обрезал
  } catch (error) {
    console.error('getSalesWB', `Ошибка JSON.parse = ${error.message}`);
    contentText = correctStringJSON(contentText); // Востановим строку
    json = JSON.parse(contentText); // Пробуем еще раз
    console.warn('getSalesWB', `Строка JSON востановлена, JSON.parse успешно`);
  };


  for (i in json) {
    let el = json[i];
    

    let typ
    let saleID = el.saleID;
    if (saleID[0] == 'S'){typ = 'Продажа'};
    if (saleID[0] == 'R'){typ = 'Возврат'};
    if (saleID[0] == 'D'){typ = 'Доплата'};
    if (saleID[0] == 'A'){typ = 'Сторно продаж'};
    if (saleID[0] == 'B'){typ = 'Сторно возврата'};

    
    let arr = [
      Utilities.formatDate(new Date(el.date), gmt, "dd.MM.yyyy"), 
      el.lastChangeDate, 
      String(el.supplierArticle),
      el.forPay,
      typ,
      el.odid,
      el.techSize,
      String(el.barcode),
      el.nmId
    ];
    data.push(arr); 
  };

  
  let returnObj = {
    'dataLength': data.length,
    'data': data,
  };

  return returnObj;
};




// Перебераем столбец 'Дата обновления WB (lastChangeDate)' и находим строку с первой датой qDays дней назад.
// qDays - кол-во дней которое будет отниматься от текущей даты
function getRow_dateFrom(sheet, qDays) {
  let date = new Date(); // Текущая дата в часовом поясе манефеста
  date.setDate(date.getDate() - qDays);
 
  console.info('getRow_dateFrom', `Сейчас - ${qDays} дней = ${date}`);

  let columnLCD = getNumColumn(sheet, 'Дата обновления WB (lastChangeDate)'); // Номер столбца 'Дата обновления WB (lastChangeDate)'
  let lr = sheet.getLastRow();
  if (lr <= 1) return [null, null]; // [дата, в какой строке найдена]


  let data = sheet.getRange(2, columnLCD, lr - 1).getValues().flat();
  let row;
  let dateFrom;
  for (var i = data.length - 1; i > 0; i--) {
    let lcd = new Date(data[i]);
    if (lcd <= date) {
      row = Number(i) + 2;
      dateFrom = sheet.getRange(row, columnLCD).getValue();
      break;
    };
  };

  return [dateFrom, row]; // [дата, в какой строке найдена]
};



// Возвращает номер столбца с нужным значением заголовка
function getNumColumn(sheet, head) {
  let headers = sheet.getRange('1:1').getValues().flat();
  let poz = headers.indexOf(head);
  if (poz >= 0) return poz + 1;
};



// Востонавливает строку если она получена не полностью
function correctStringJSON(str) {
  let index = str.lastIndexOf('"},{"');
  let newString = str.slice(0, index)+'"}]';
  
  return newString;
};