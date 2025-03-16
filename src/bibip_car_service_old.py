from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from pathlib import Path


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        file_path_models = f'{self.root_directory_path}/models.txt' # Путь до файла с моделями
        file_path_index = f'{self.root_directory_path}/models_index.txt' # Путь до файла с индексами

        # Конструируем запись "модель" в виде объекта json
        row_value_model = (f'{{"id" : {model.id}, '
                            f'"name" : "{model.name}", '
                            f'"brand" : "{model.brand}}}"').ljust(500) + '\n'

        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Шаг 1. Пытаемся создать файл для записи моделей. 
        # Если такого файла еще нет, создаем его и добавляем туда первую запись.
        # Для простоты считаем, что если не существует файл models.txt, то не существует и models_index.txt.
        try:
            with open(file_path_models, 'x') as file:
                file.write(f'{row_value_model}')
                row_value_index = f'{model.id}, 1'.ljust(500) + '\n'
                try:
                    with open(file_path_index, 'x') as ifile:
                        ifile.write(f'{row_value_index}')
                except FileExistsError:
                    pass
                return model
        # Если такой файл уже есть пропускаем ход и ниже откроем файл повторно
        # в режиме r+, чтобы одновременно и читать, и писать в него.        
        except FileExistsError:
            pass

        # Если файл с моделями уже есть:
        # - открываем его на чтение+запись,
        # - считаем кол-во строк,
        # добавляем новую строку в конец файла.        
        with open(file_path_models, "r+") as file:
            # Для подсчета уже записанных строк использую enumarate, чтобы можно 
            # было работать с большими файлами.
            for line_number, line in enumerate(file):
                pass

            line_number += 1 
            file.seek(line_number * (501)) # длина строки 501, т.к. добавили символ перехода строки — он тоже считается.
            file.write(f'{row_value_model}')
            row_value_index = f'{model.id}, {line_number + 1}'.ljust(500) + '\n'
            with open(file_path_index, 'r+') as ifile:
                ifile.seek(line_number * (501))
                ifile.write(f'{row_value_index}')
                # Выгрузим содержимое индексного файла в список, отсортируем по первому полю и запишем обратно
                # в отсортированном порядке. 
                # temp_index = {} * line_number   
                temp_index = [] * line_number             
                for iline in enumerate(ifile):
                    id, row_num = iline[1].split(',')
                    temp_index.append((int(id), row_num))
                
                sorted_temp_index = sorted(temp_index, key=lambda x: x[0])
                for _ in sorted_temp_index:
                    ifile.write(f'{_}')


        return model
    
    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами

        # Конструируем запись "автомобиль" в виде объекта json
        row_value_car = (f'{{"vin" : "{car.vin}", '
                            f'"model" : {car.model}, '
                            f'"price" : "{car.price}", '
                            f'"date_start" : "{car.date_start}", '
                            f'"status" : "{car.status}"}}').ljust(500) + '\n'

        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Шаг 1. Пытаемся создать файл для записи моделей. 
        # Если такого файла еще нет, создаем его и добавляем туда первую запись.
        # Для простоты считаем, что если не существует файл models.txt, то не существует и models_index.txt.
        try:
            with open(file_path_cars, 'x') as file:
                file.write(f'{row_value_car}')
                row_value_index = f'{car.vin}, 1'.ljust(500) + '\n'
                try:
                    with open(file_path_index, 'x') as ifile:
                        ifile.write(f'{row_value_index}')
                except FileExistsError:
                    pass
                return car
        # Если такой файл уже есть пропускаем ход и ниже откроем файл повторно
        # в режиме r+, чтобы одновременно и читать, и писать в него.        
        except FileExistsError:
            pass

        # Если файл с моделями уже есть:
        # - открываем его на чтение+запись,
        # - считаем кол-во строк,
        # добавляем новую строку в конец файла.        
        with open(file_path_cars, "r+") as file:
            # Для подсчета уже записанных строк использую enumarate, чтобы можно 
            # было работать с большими файлами.
            for line_number, line in enumerate(file):
                pass

            line_number += 1 
            file.seek(line_number * (501)) # длина строки 501, т.к. добавили символ перехода строки — он тоже считается.
            file.write(f'{row_value_car}')
            row_value_index = f'{car.vin}, {line_number + 1}'.ljust(500) + '\n'
            with open(file_path_index, 'r+') as ifile:
                ifile.seek(line_number * (501))
                ifile.write(f'{row_value_index}')

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        raise NotImplementedError

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        raise NotImplementedError

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError

# Отладка
carservice = CarService('database')
# Добавление моделей
model = Model(id='5', name='Logan', brand='Renault')
print('Row added: ', carservice.add_model(model))

model = Model(id='3', name='3', brand='Mazda')
print('Row added: ', carservice.add_model(model))

model = Model(id='1', name='Optima', brand='Kia')
print('Row added: ', carservice.add_model(model))

model = Model(id='4', name='Pathfinder', brand='Nissan')
print('Row added: ', carservice.add_model(model))

model = Model(id='2', name='Sorento', brand='Kia')
print('Row added: ', carservice.add_model(model))

# Добавление автомобилей
# KNAGM4A77D5316538	1	2000	2024-02-08	available
#status = CarStatus('available')
car = Car(vin='KNAGM4A77D5316538', model=1, price=2000, date_start='2024-02-08', status=CarStatus('available'))
print('Row added: ', carservice.add_car(car))

car = Car(vin='5XYPH4A10GG021831', model=2, price=2300, date_start='2024-02-20', status=CarStatus('reserve'))
print('Row added: ', carservice.add_car(car))

car = Car(vin='KNAGH4A48A5414970', model=1, price=2100, date_start='2024-04-04', status=CarStatus('available'))
print('Row added: ', carservice.add_car(car))

car = Car(vin='JM1BL1TFXD1734246', model=3, price=2276.65, date_start='2024-05-17', status=CarStatus('available'))
print('Row added: ', carservice.add_car(car))

car = Car(vin='JM1BL1M58C1614725', model=3, price=2549.10, date_start='2024-05-17', status=CarStatus('reserve'))
print('Row added: ', carservice.add_car(car))
# Проблемы
# Вложенный тип CarStatus
# Подозреваю, что при каждой новой записи индекса, их нужно сортировать по возрастанию id сущности
# Добавить обработку повторного добавления записи с уже существующим ключом