/* // Функция обрабатывает данные с выгрузки и устанавливает на сводный лист "В день"
const RANGE = 'B2:C'; // Диапазон для столбцов "Техническая"и "Артикул"

function get_ArtSize(sheetName) {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheetVygruzka = ss.getSheetByName('Выгрузка');
  
  let obj = {};

  let data = sheetVygruzka.getRange('B2:C').getValues();
  for (i in data) {
    let row = data[i];
    let art = row[0];
    if (art == '') continue;
    let size = row[1];
    if (size == '') continue;

    if (!obj[art]) obj[art] = [size];
    else if (obj[art].includes(size)) continue;
    else obj[art] = obj[art].concat(size);
  };


  let groups = [];
  let newData = [];
  let keys = Object.keys(obj);
  keys.sort();
  for (k in keys) {
    let art = keys[k];
    newData.push(['<head>', art]);
    let grupStart = newData.length + 2; // Номер строки для группировки
    let grupLenght = 0;
    let sizes = obj[art]; // Масиив размеров для артикула
    sizes = sort(sizes); // Отсортируем по размерам
    for (s in sizes) {
      let size = sizes[s];
      newData.push([art, size]);
      grupLenght += 1;
    };

    groups.push([grupStart, grupStart + (grupLenght - 1)]);
  };
  

  let sheet = ss.getSheetByName(sheetName);
  sheet.getRange(RANGE).clearContent().setFontWeight(null);
  SpreadsheetApp.flush();

  //sheet.getRange(2, 2, newData.length, newData[0].length).setValues(newData);
  sheet.getRange(RANGE + (newData.length + 1)).setValues(newData);
  console.info('Данные установлены в таблицу');
  

  // ГРУППИРОВКИ
  let maxRows = sheet.getMaxRows();
  sheet.getRange(`1:${maxRows}`).shiftRowGroupDepth(-10); // Снимаем группировки если были и скидываем шрифт
  sheet.showRows(1, maxRows); // Раскрываем скрытые строки


  // Группируем новые
  for (g in groups) {
    let range = groups[g];
    //sheet.getRange(`${range[0]}:${range[1]}`).shiftRowGroupDepth(1);
    sheet.getRange(`${range[0] - 1}:${range[0] - 1}`).setFontWeight('bold');
  };
  
  
  
  return;
};


function sort(data) {
  let arr = ['XXS', 'XS', 'XXS', 'M', 'L', 'XL', 'XXL','XXS', 40, 42, 44, 46, 48, 50, 52, 54, 56]; // Порядок сортиоовки

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
}; */