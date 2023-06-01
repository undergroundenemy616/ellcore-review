// Устанавливает чекбоксы API_KEY в false, очщищает всю выгрузку, ставит false на Активация формул, ставит триггер на launchGetStocksWB
function startGetStocksWB() {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let apiKEY = ss.getSheetByName('API_KEY');
  apiKEY.getRange('D2:D').clear();
  apiKEY.getRange('D2:D').clearNote();
  console.info('startGetStocksWB', `Все чекбоксы API_KEY установлены в положения FALSE`);
  
  return;
};




// Функция запуска
function launchGetStocksWB() {
  console.time('Время выполнения');
  
  try{ // Обработка ошибок
    var lock = LockService.getDocumentLock(); // Блокировка не позволяющая любому пользователю текущего документа одновременно запускать раздел кода.
    lock.waitLock(0); // Получим блокировку
  } catch (err){ // Если ошибка, блокировка не получена
    console.error('launchGetStocksWB', `Блокировка не получена. Ошибка = ${err.message}`);
    console.timeEnd('Время выполнения');
    return;
  };

  let ss = SpreadsheetApp.getActiveSpreadsheet();
  
  let sheetSettings = ss.getSheetByName('Настройки');
  let gmt = sheetSettings.getRange('B1').getValue(); 
  
  let apiKEY = ss.getSheetByName('API_KEY');
  let dataKEY = apiKEY.getDataRange().getValues();
  dataKEY.splice(0, 1); // Удалим заголовок

  for (let i = 0; i < dataKEY.length; i++) {
    let use = dataKEY[i][0];
    if (!use) continue;
    
    let status =  dataKEY[i][3];
    if (status) continue; // Если статус тру
    
    let key = dataKEY[i][1]; // АпиКей
    let nameCompany = dataKEY[i][2]; // Название ЛК
    console.info('launchGetStocksWB', `Название ЛК = ${nameCompany}`);

    // Получим данные с ВБ и установим в выгрузку
    getDATA_WB(ss, key, gmt, nameCompany);
  
    let numRow = i + 2; // Номер СТРОКИ В ТАБЛИЦЕ
    apiKEY.getRange(numRow, 4).setValue(true).setNote(Utilities.formatDate(new Date(), "GMT+3", "dd.MM.yyyy HH:mm:ss '(GMT+3)'"));
    
    lock.releaseLock(); // Снимаем блокировку
    console.timeEnd('Время выполнения');

    return {'repeat': true};
  };

  lock.releaseLock(); // Снимаем блокировку
  console.info('launchGetStocksWB', 'Все функции успешно выполнены. Цикл завершен!');
  console.timeEnd('Время выполнения');
  
  return {'repeat': false};
};




// Получаем данные по апи с WB
function getDATA_WB(ss, key, gmt, nameCompany) {
  let dateFrom = "2000-01-01"; // За все время

  console.info('getDATA_WB', `Дата для запроса (dateFrom) = ${dateFrom}`);
  
  let data = [];
  do {
    let req = getStocksWB(key, dateFrom, gmt, nameCompany);
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

  // Удалим el.lastChangeDate, нужен для повторного запроса, но не нужен в таблице
  for (d in data) data[d].splice(1, 1);
  
  // Установим данные в таблицу;
  let sheet = ss.getSheetByName('Выгрузка');
  let lr = sheet.getLastRow();
  console.info('getDATA_WB', `Строка начала установки данных = ${lr + 1}`);

  console.time('Установка данных в таблицу');
  SpreadsheetApp.flush();

  // API Sheets
  let dataRange = sheet.getRange(lr + 1, 1, data.length, data[0].length);
  let request = {
    'majorDimension': 'ROWS',
    'values': data
  };

  let dop_arrgs = {
    'insertDataOption': 'OVERWRITE', // Использовать с Sheets.Spreadsheets.Values.append
    'valueInputOption': 'USER_ENTERED',
  };

  let ssId = ss.getId();
  let append_range = sheet.getName() + '!' + dataRange.getA1Notation();

  Sheets.Spreadsheets.Values.append(request, ssId, append_range, dop_arrgs);
  console.timeEnd('Установка данных в таблицу');
  SpreadsheetApp.flush();
  console.info('getDATA_WB', 'Данные с WB загружены и установлены на лист "Выгрузка"');

  return;
};


// Запрос в WB
function getStocksWB(key, dateFrom, gmt, nameCompany) {
  let date = Utilities.formatDate(new Date(), gmt, "dd.MM.yyyy");
  
  // Запрашиваем данные в WB
  let responseCode;
  while (responseCode != 200){
    try {
      let url = `https://statistics-api.wildberries.ru/api/v1/supplier/stocks?flag=0&dateFrom=${dateFrom}` // гггг-мм-дд
      let params = {
        'headers': {
          'Authorization': key
        }
      };
      var res = UrlFetchApp.fetch(url, params);
      responseCode = res.getResponseCode();
      console.info('getStocksWB', `Запрос в WB (responseCode) = ${responseCode}`);
    } catch (err){
      console.warn('getStocksWB', `WB не ответил, повтор запроса через 15 сек. Ошибка = ${err.message}`);
      Utilities.sleep(15000);
    };
  };


  let data = []; // Массив для установки в таблицу


  let contentText = res.getContentText();
  let json;
  try {
    json = JSON.parse(contentText); // Если ошибка, например длинный ответ и гугл его обрезал
  } catch (error) {
    console.error('getStocksWB', `Ошибка JSON.parse = ${error.message}`);
    contentText = correctStringJSON(contentText); // Востановим строку
    json = JSON.parse(contentText); // Пробуем еще раз
    console.warn('getStocksWB', `Строка JSON востановлена, JSON.parse успешно`);
  };


  for (i in json) {
    let el = json[i];

    let quantity = el.quantity;
    let arr = [//!!!!!! используем for (d in data) data[d].splice(1, 1);
      date, 
      el.lastChangeDate, 
      el.supplierArticle, 
      el.techSize, 
      quantity, 
      el.quantityFull - quantity, 
      String(el.barcode), 
      el.nmId, 
      nameCompany
    ]; 
    data.push(arr); 
  };


  let returnObj = {
    'dataLength': data.length,
    'data': data,
  };

  return returnObj;
};




// Востонавливает строку если она получена не полностью
function correctStringJSON(str) {
  let index = str.lastIndexOf('"},{"');
  let newString = str.slice(0, index)+'"}]';
  
  return newString;
};