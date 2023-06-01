function compress_VygruzkaSklad() {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheetVygruzka = ss.getSheetByName('Выгрузка');
  let DATA = sheetVygruzka.getDataRange().getDisplayValues();
  DATA.splice(0, 1);
  

  let NEW_DATA = [];

  // Фильтр по дню
  let unique_0 = get_UNIQUE(DATA, 0); // Дата выгрузки
  for (a in unique_0) {
    let day = unique_0[a];
    let data_day = DATA.filter(element => {
      if (element[0] == day) return element; 
    });
    // Фильтр по артикулу
    let unique_1 = get_UNIQUE(data_day, 1); // Артикул поставщика (SupplierArticle)
    for (b in unique_1) {
      let art = unique_1[b];
      let data_art = data_day.filter(element => {
        if (element[1] == art) return  element;
      });

      // Фильтр по размеру
      let unique_2 = get_UNIQUE(data_art, 2); // Размер (techSize)
      for (c in unique_2) {
        let size = unique_2[c];
        let data_size = data_art.filter(element => {
          if (element[2] == size) return element; 
        });

        // Фильтр по ЛК
        let unique_7 = get_UNIQUE(data_size, 7); // ЛК
        for (d in unique_7) {
          let lk = unique_7[d];
          let data_lk = data_size.filter(element => {
            if (element[7] == lk) return element; 
          });

          // Суммируем отфильтрованный массив
          let sum_kol_svobodnoe = 0;
          let sum_kol_v_pyti = 0;
          for (i in data_lk) {
            let row = data_lk[i];
            sum_kol_svobodnoe += Number(row[3]);
            sum_kol_v_pyti += Number(row[4]);
          };

          // Добавим полученый результат в массив для установки в таблицу
          if (data_lk.length > 0) {
            let data = data_lk[0];
            NEW_DATA.push([data[0], data[1], data[2], sum_kol_svobodnoe, sum_kol_v_pyti, data[5], data[6], data[7]]);
          };
        };
      };
    };
  };

  console.info('compress_VygruzkaSklad', `Данные готовы для установки в таблицу: NEW_DATA.length = ${NEW_DATA.length}`);
  SpreadsheetApp.flush();
  let lr = sheetVygruzka.getLastRow();
  if (lr > 1) sheetVygruzka.getRange(`2:${lr}`).clear(); 
  SpreadsheetApp.flush();
  console.info('compress_VygruzkaSklad', `Старые значения удалены: Очищен диапазон "${`2:${lr}`}"`);

  let rangeSetVals = sheetVygruzka.getRange(2, 1, NEW_DATA.length, NEW_DATA[0].length);
  rangeSetVals.setValues(NEW_DATA);
  console.info('compress_VygruzkaSklad', `Новые значения установлены. Сжатие выгрузки завершено.`);
  
  sheetVygruzka.getRange(`A2:A`).setNumberFormat('dd.mm.yyyy');
  rangeSetVals.sort({column: 1, ascending: true});
};



function get_UNIQUE(array, numElement) {
  let data = [];
  for (i in array) {
    let row = array[i];
    data.push(row[numElement]);
  };
  return [...new Set(data)];
};