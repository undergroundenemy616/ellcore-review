// Если sumEL не указан, кол-во строк
function report_v_den_Sales(nameReportSheet, sumEL) {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let DATA = getDATA(ss);
  
  let unique_0 = get_UNIQUE(DATA, 0); // Дата выгрузки
  unique_0 = sortStringDate(unique_0); // Сортируем дату
  

  let NEW_DATA = [];

  NEW_DATA.push(['ЛК', 'Баркод', 'Артикул', 'Размер', ...unique_0]); // Пушим заголовок


  
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
            if (element[0] == day) return element;
          });

          
          // Суммируем отфильтрованный массив
          let sum_kol = 0;
          if (sumEL) {
            for (i in data_day) {
              let row = data_day[i];
              let typ = row[4];
              let str = row[sumEL].replace(',', '.');
              if (typ === 'Продажа') sum_kol += Number(str);
              if (typ === 'Возврат') sum_kol -= Number(str);
              if (typ === 'Сторно продаж') sum_kol -= Number(str);
              if (typ === 'Сторно возврата') sum_kol -= Number(str);
              if (typ === 'Доплата') continue;
            };
          }
          else {
            for (i in data_day) {
              let row = data_day[i];
              let typ = row[4];
              if (typ === 'Продажа') sum_kol += 1;
              if (typ === 'Возврат') sum_kol -= 1;
              if (typ === 'Сторно продаж') sum_kol -= 1;
              if (typ === 'Сторно возврата') sum_kol -= 1;
              if (typ === 'Доплата') continue;
            };
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
  
// Находит баркод среди массива (нужен так как баркод есть не у всех строк)
function getBarcode(data_size) {
  for (i in data_size) {
    let row = data_size[i];
    let bc = row[7];
    if (bc) return bc;
  };
};
  

// Суммирем кол-во по дню/артикулу
function sumDataRows(DATA_ROWS) {
  let head = [DATA_ROWS[0][0], 'head', DATA_ROWS[0][2], DATA_ROWS[0][2]];
  for (r in DATA_ROWS) {
    let row = DATA_ROWS[r];
    for (let i = 4; i < row.length; i++) {
      if(!head[i]) head[i] = row[i];
      else head[i] += row[i];
    };
  };
  return head;
};
  

function sort(data) {
  let arr = ['XXS', 'XS', 'XXS', 'M', 'L', 'XL', 'XXL','XXS', '40', '42', '44', '46', '48', '50', '52', '54', '56']; // Порядок сортиоовки

  let newData = [];
  for (i in arr) {
    let serch = arr[i];
    let poz = data.indexOf(serch);
    if (poz >= 0) {
      newData.push(serch);
      data.splice(poz, 1);
    };
  };
  newData = newData.concat(data);

  return newData;
};

function getDATA(ss) {
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
    let data = sheet.getDataRange().getDisplayValues();
    data.splice(0, 1);
    
    for (d in data) data[d].push(name);

    DATA = DATA.concat(data);
  };

  return DATA; 
};


function get_UNIQUE(array, numElement) {
  let data = [];
  for (i in array) {
    let row = array[i];
    data.push(row[numElement]);
  };
  return [...new Set(data)];
};


// Сортирует дату в виде строки
function sortStringDate(arr) {
  for (i in arr) {
    arr[i] = Utilities.parseDate(arr[i], "GMT+3", "dd.MM.yyyy");
  };

  arr.sort((d1, d2) => d1 > d2 ? 1 : -1);

  for (e in arr) {
    arr[e] = Utilities.formatDate(arr[e], "GMT+3", "dd.MM.yyyy");
  };
  
  return arr;
}