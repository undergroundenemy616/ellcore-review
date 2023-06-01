//1C29h_-ZKYebD8dYfVFuFkzKrD4nnmntQS5OazL_vrqmEcKGGLKcn91QZ

// Суммирует выгрузку по артикулам / дням
function getRealization() {
  let ss = SpreadsheetApp.getActiveSpreadsheet();

  let sheetData = ss.getSheetByName('Выгрузка');
  let lr = sheetData.getLastRow();
  if (lr == 1) {
    console.error('Лист "Выгрузка" не содержит данных');
    return
  };

  let OBJ = getOBJ_sa_name(sheetData);

  let DATA = sheetData.getRange(`B2:M${lr}`).getValues();
  let setData = [];
  
  let companys = [...new Set(getArrayColumn(DATA, 11).flat())]; // Уникальные значения ЛК
  for (c in companys) {
    let company = companys[c]; // ЛК
    
    let data = DATA.filter(element => { // Массив значений с нужным ЛК
     return element[11] == company
    });

    let obj = _.cloneDeep(OBJ);

    for (i in data) {
    
      let row = data[i];
      let sa_name = row[0]; // Артикул поставщика (sa_name)
      let doc_type_name = row[1]; // Тип документа (doc_type_name)
      let sale_dt = row[2]; // Дата продажи в часовом поясе указаного в настройках (sale_dt)

      let quantity = row[3]; // Количество (quantity)
      let ppvz_for_pay = row[4]; // К перечислению продавцу за реализованный товар (ppvz_for_pay)
      let delivery_amount = row[5]; // Количество доставок (delivery_amount)
      let return_amount = row[6]; // Количество возвратов (return_amount)
      let delivery_rub = row[7]; // Стоимость логистики (delivery_rub)
      let retail_price_withdisc_rub = row[8]; // Цена розничная с учетом согласованной скидки (retail_price_withdisc_rub)
      let barcode = row[9]; // Баркод
      let nmId = row[10]; // Артукул WB
      let nameCompany = row[11]; // ЛК


      let obj$ = obj[sa_name][doc_type_name][sale_dt];
      if (!obj$) obj$ = ['', '', '', 0, 0, 0, 0, 0, 0, '', '', ''];
      
      obj[sa_name][doc_type_name][sale_dt] = [
        sa_name, 
        doc_type_name, 
        sale_dt, 
        Number(quantity) + obj$[3], 
        Number(ppvz_for_pay) + obj$[4], 
        Number(delivery_amount) + obj$[5],
        Number(return_amount) + obj$[6],
        Number(delivery_rub) + obj$[7],
        Number(retail_price_withdisc_rub) + obj$[8],
        String(barcode),
        String(nmId),
        String(nameCompany)
      ];

    };

    let keys = Object.keys(obj);
    for (k in keys) {
      let sku = obj[keys[k]];
    
      let sale = sku.Продажа;
      let keysSale = Object.keys(sale);
      for (ks in keysSale) {
        let row = sale[keysSale[ks]];
        if (row[0] != '') setData.push(row);
      };


      let return$ = sku.Возврат;
      let keysReturn$ = Object.keys(return$);
      for (kr in keysReturn$) {
        let row = return$[keysReturn$[kr]];
        if (row[0] != '') setData.push(row);
      };
    };
  };


  let sheet = ss.getSheetByName('Реализации');
  let lr_2 = sheet.getLastRow();
  if (lr_2 > 1) sheet.getRange(`2:${lr_2}`).clearContent();
  //SpreadsheetApp.flush();
  sheet.getRange(2, 1, setData.length, setData[0].length).setValues(setData);


  console.info('getRealization', 'Данные успешно загружены');

};



// Получаем массив уникальных артикулов поставщика
function getOBJ_sa_name(sheetData) {
  let data = sheetData.getRange('B2:B').getValues().flat();
  let sku = [...new Set(data)];
  
  let obj = {};
  for (i in sku) {
    obj[sku[i]] = {Продажа: {}, Возврат: {}};
  };

  return obj; 
};


// Получаем массив вида [[1], [1]] из массива вида [[0, 1, 2, 3], [0, 1, 2, 3]]
function getArrayColumn(data, num) {
  let newData = [];
  for (i in data) {
    let row = data[i]
    let val = row[num];
    newData.push([val]);
  };

  return newData;
}