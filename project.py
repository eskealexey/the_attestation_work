import csv
import os


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path=''):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        file_path = os.getcwd()
        new_dict = {}
        with open('file.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['наименование', 'цена', 'вес', 'файл', 'цена за кг'], delimiter=',')
            writer.writeheader()
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if 'price' in file:
                    with open(file, "r", encoding='utf8') as csvf:
                        reader = csv.DictReader(csvf)
                        for line in reader:
                            if 'товар' in line:
                                new_dict['наименование'] = line['товар']
                            elif 'название' in line:
                                new_dict['наименование'] = line['название']
                            elif 'наименование' in line:
                                new_dict['наименование'] = line['наименование']
                            elif 'продукт' in line:
                                new_dict['наименование'] = line['продукт']
                            if 'розница' in line:
                                new_dict['цена'] = line['розница']
                            elif 'цена' in line:
                                new_dict['цена'] = line['цена']
                            if 'вес' in line:
                                new_dict['вес'] = line['вес']
                            elif 'масса' in line:
                                new_dict['вес'] = line['масса']
                            elif 'фасовка' in line:
                                new_dict['вес'] = line['фасовка']
                            new_dict['файл'] = file
                            new_dict['цена за кг'] = round(float(new_dict['цена']) / float(new_dict['вес']), 2)
                            with open('file.csv', 'a', newline='') as f:
                                writer = csv.DictWriter(f, fieldnames=['наименование', 'цена', 'вес', 'файл', 'цена за кг'])
                                writer.writerow(new_dict)
        return 'Прайс загружен'

    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''

    def export_to_html(self, fname='output.html'):

        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        count_ = 1
        for line in self.data:
            result += f'<tr>'
            result += f'<td>{count_}</td>'
            result += f'<td>{line["наименование"]}</td>'
            result += f'<td>{line["цена"]}</td>'
            result += f'<td>{line["вес"]}</td>'
            result += f'<td>{line["файл"]}</td>'
            result += f'<td>{line["цена за кг"]}</td>'
            result += f'</tr>'
            count_ += 1
            result += '''
            </table>
            </body>
            </html>
            '''
        with open(fname, 'w', encoding='utf8') as f:
            f.write(result)
        return f"Данные экспортированны в {fname}"

    def find_text(self, text):
        self.data = []
        with open('file.csv', 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for line in reader:
                if text.lower() in line['наименование'].lower():
                    self.data.append(line)
        self.data =  sorted(self.data, key=lambda d: float(d['цена за кг']))
        num = 1
        columns = ['№', 'Наименование', 'цена', 'вес', 'файл', 'цена за кг.']
        print(f'{columns[0]:3s}{columns[1]:50s}\t{columns[2]:4s}\t{columns[3]:3s}\t{columns[4]:15s}\t{columns[5]}')
        print('----------------------------------------------------------------------------------------------')
        for line in self.data:
            print(f"{num}\t{line['наименование']:50s}\t{line['цена']:4s}\t{line['вес']:3s}\t{line['файл']:15s}\t{line['цена за кг']}")
            num += 1
        return  self.data


pm = PriceMachine()
print(pm.load_prices())

while True:
    text = input('Введите строку поиска (для выхода введите "exit"):')
    if text == 'exit':
        break
    print('==============================================================================================')
    pm.find_text(text)
    print('==============================================================================================')
    print()

print('the end')
print(pm.export_to_html())
