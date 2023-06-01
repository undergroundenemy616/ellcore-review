function report_v_den(nameReportSheet, sumEL) {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheetVygruzka = ss.getSheetByName('Выгрузка');
  let DATA = sheetVygruzka.getDataRange().getDisplayValues();
  DATA.splice(0, 1);
  
  let unique_0 = get_UNIQUE(DATA, 0); // Дата выгрузки

  let NEW_DATA = [];

  NEW_DATA.push(['ЛК', 'Баркод', 'Артикул', 'Размер', ...unique_0]); // Пушим заголовок


  
  // Фильтр по ЛК
  let unique_7 = get_UNIQUE(DATA, 7); // ЛК
  for (a in unique_7) {
    let lk = unique_7[a];
    let data_lk = DATA.filter(element => {
      if (element[7] == lk) return element; 
    });
  
    // Фильтр по артикулу
    let unique_1 = get_UNIQUE(data_lk, 1); // Артикул поставщика (SupplierArticle)
    for (b in unique_1) {
      let art = unique_1[b];
      let data_art = data_lk.filter(element => {
        if (element[1] == art) return  element;
      });

      let DATA_ROWS = []; // Массив всех размеров одного артикула

      // Фильтр по размеру
      let unique_2 = get_UNIQUE(data_art, 2); // Размер (techSize)
      unique_2 = sort(unique_2); // Сортировка
      for (c in unique_2) {
        let size = unique_2[c];
        let data_size = data_art.filter(element => {
          if (element[2] == size) return element; 
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
          for (i in data_day) {
            let row = data_day[i];
            sum_kol += Number(row[sumEL]);
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
  sheetReport.getDataRange().clear(); 
  SpreadsheetApp.flush();
  sheetReport.getRange(1, 1, NEW_DATA.length, NEW_DATA[0].length).setValues(NEW_DATA);
  console.info('report_v_den', `Новые значения установлены.`); 
};  
  
// Находит баркод среди массива (нужен так как баркод есть не у всех строк)
function getBarcode(data_size) {
  for (i in data_size) {
    let row = data_size[i];
    let bc = row[5];
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