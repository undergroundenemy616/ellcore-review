// Если sumEL не указан, кол-во строк
function report_temp_dlya_planirovaniya_Sales(nameReportSheet) {
  let now = new Date().getTime();
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  
  let unique_0 = getDateBack(); // Даты выгрузки
  let DATA = getDATA_temp_plan(ss, unique_0[0]);
  

  let NEW_DATA = [];

  NEW_DATA.push(['ЛК', 'Баркод', 'Артикул', 'Размер', '30 дней', '7 дней', '3 дня', '1 день']); // Пушим заголовок


  
  // Фильтр по ЛК
  let unique_9 = get_UNIQUE(DATA, 9); // ЛК
  for (a in unique_9) {
    let lk = unique_9[a];
    let data_lk = DATA.filter(element => {
      if (element[9] == lk) return element; 
    });
  
    // Фильтр по артикулу
    let unique_2 = get_UNIQUE(data_lk, 2); // Артикул поставщика (SupplierArticle)
    for (b in unique_2) {
      let art = unique_2[b];
      let data_art = data_lk.filter(element => {
        if (element[2] == art) return  element;
      });

      let DATA_ROWS = []; // Массив всех размеров одного артикула

      // Фильтр по размеру
      let unique_6 = get_UNIQUE(data_art, 6); // Размер (techSize)
      unique_6 = sort(unique_6); // Сортировка
      for (c in unique_6) {
        let size = unique_6[c];
        let data_size = data_art.filter(element => {
          if (element[6] == size) return element; 
        });

        let barcode = getBarcode(data_size);
        let DataROW = [lk, barcode, art, size]; // Массив строки отчета
        
        // Фильтр по дню
        for (d in unique_0) {
          let day = unique_0[d];
          let data_day = data_size.filter(element => {
            let elDate = element[0].getTime();
            if (elDate >= day && elDate <= now) return element;
          });

          let sum_kol = 0;
          for (i in data_day) {
            let row = data_day[i];
            let typ = row[4];
            if (typ === 'Продажа') sum_kol += 1;
            if (typ === 'Возврат') sum_kol -= 1;
            if (typ === 'Сторно продаж') sum_kol -= 1;
            if (typ === 'Сторно возврата') sum_kol -= 1;
            if (typ === 'Доплата') continue;
          };
          
          DataROW.push(sum_kol);
        };

        DATA_ROWS.push(DataROW); // Строки артикул/ размер
      };
  
      NEW_DATA.push(sumDataRows(DATA_ROWS), ...DATA_ROWS); // Пушим в массив для установки данных добаляя заголовок и сумму по артикулу
    };
  };

  console.info('report_v_den', `Данные готовы для установки в таблицу: NEW_DATA.length = ${NEW_DATA.length}`);
  SpreadsheetApp.flush();
  let sheetReport = ss.getSheetByName(nameReportSheet);
  sheetReport.clear(); 
  SpreadsheetApp.flush();
  sheetReport.getRange(1, 1, NEW_DATA.length, NEW_DATA[0].length).setValues(NEW_DATA);
  console.info('report_v_den', `Новые значения установлены.`); 
};  



function getDateBack() {
  let date = new Date();
  let back_30 = new Date(new Date(date).setDate(date.getDate() - 30));
  let back_7 = new Date(new Date(date).setDate(date.getDate() - 7));
  let back_3 = new Date(new Date(date).setDate(date.getDate() - 3));
  let back_1 = new Date(new Date(date).setDate(date.getDate() - 1));


  let arr = [back_30, back_7, back_3, back_1];
  for (i in arr) {
    arr[i].setHours(00);
    arr[i].setMinutes(00);
    arr[i].setSeconds(00);
    arr[i].setMilliseconds(00);

    arr[i] = arr[i].getTime();
  };

  return arr;
};




function getDATA_temp_plan(ss, back_30) {
  //let ss  = SpreadsheetApp.getActiveSpreadsheet();
  let apiKEY = ss.getSheetByName('API_KEY');
  let names = []; // Имена листов, они же названия ЛК
  let dataKEY = apiKEY.getDataRange().getValues();
  dataKEY.splice(0, 1);


  for (i in dataKEY) {
    let row  = dataKEY[i];
    if (row[0]) names.push(row[2]);
  };

  
  let DATA = [];
  for (n in names) {
    let name = names[n];
    let sheet = ss.getSheetByName(name);
    let data = sheet.getDataRange().getValues();
    data.splice(0, 1);
    
    for (d in data) {
      data[d].push(name);
    };

    DATA = DATA.concat(data);
  };


  DATA = DATA.filter(element => {
    if (element[0].getTime() >= back_30) return element
  });

  return DATA; 
};