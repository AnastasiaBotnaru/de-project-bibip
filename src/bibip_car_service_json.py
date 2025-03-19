from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from pathlib import Path


class CarService:
    """Хранение данных организовано в виде объектов json. Подумала, что читать и редактировать такие
    данные будет сложнее, чем список через запятую. Решила переписать.
    """
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение моделей
    def add_model(self, model: Model) -> Model:
        file_path_models = f'{self.root_directory_path}/models.txt' # Путь до файла с моделями
        file_path_index = f'{self.root_directory_path}/models_index.txt' # Путь до файла с индексами

        # Конструируем запись "модель" в виде объекта json
        row_value_model = (f'{{"id" : {model.id}, '
                            f'"name" : "{model.name}", '
                            f'"brand" : "{model.brand}}}"').ljust(500) + '\n'

        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Считаем, что оба файла (models и индексы) должны существовать одновременно.
        # Если обоих файлов нет, создаем их и добавляем первую запись.
        if (not Path(file_path_models).exists() and
            not Path(file_path_index).exists()
        ):
            with open(file_path_models, 'w') as file:
                file.write(f'{row_value_model}')
                
            row_value_index = f'{model.id},1'.ljust(500) + '\n'

            with open(file_path_index, 'x') as ifile:
                ifile.write(f'{row_value_index}')

        # Если оба файла есть:
        # 1. Вычисляем кол-во строк и добавляем новую запись в конец.
        # 2. Сортируем файл с индексами и перезаписываем его.
        elif (Path(file_path_models).exists() and
            Path(file_path_index).exists()
        ):
            # Добавляем запись в models.txt
            with open(file_path_models, "r+") as file:
                # Для подсчета уже записанных строк использую enumarate, чтобы можно 
                # было работать с большими файлами.
                for line_number, line in enumerate(file):
                    pass

                line_number += 1 
                file.seek(line_number * (501)) # длина строки 501, т.к. добавили символ перехода строки — он тоже считается.
                file.write(f'{row_value_model}')    
            
            row_value_index = f'{model.id},{line_number + 1}'.ljust(500) + '\n'
            
            # Добавляем запись в индексный файл
            with open(file_path_index, 'r+') as ifile:
                ifile.seek(line_number * (501))
                ifile.write(f'{row_value_index}')

            # Сортировка индексного файла:
            # 1. Читаем строки в список кортежей.
            with open(file_path_index, 'r') as ifile:
                rows = []
                for row in ifile:
                    model_id, index = tuple(row.split(','))
                    rows.append((int(model_id),int(index)))
            
            # 2. Сортируем кортежи внутри списка по первому элементу. 
            sorted_rows = sorted(rows, key=lambda x: int(x[0]))
            
            # 3. Перезаписываем индексный файл в отсортированном порядке.    
            with open(file_path_index, 'w') as ifile:
                line_number = 0    
                for row in sorted_rows:
                    row_added = f'{row[0]},{row[1]}'.ljust(500) + '\n'
                    ifile.seek(line_number * (501))
                    ifile.write(row_added)
                    line_number += 1
        
        # Во всех остальных случаях считаем, что что-то пошло не так - 
        # возвращаем сообщение об ошибке, переданную для записи модель и 
        # завершаем работу метода.
        else:
            print('Что-то пошло не так:()')
            return model

        return model
    
    # Задание 1. Сохранение автомобилей
    def add_car(self, car: Car) -> Car:
        """Добавить обработку ошибки - добавлен автомобиль, для которого нет модели."""

        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами

        # Конструируем запись "автомобиль" в виде объекта json
        row_value_car = (f'{{"vin" : "{car.vin}", '
                            f'"model" : {car.model}, '
                            f'"price" : {car.price}, '
                            f'"date_start" : "{car.date_start}", '
                            f'"status" : "{car.status}"}}').ljust(500) + '\n'

        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Считаем, что оба файла (cars и индексы) должны существовать одновременно.
        # Если обоих файлов нет, создаем их и добавляем первую запись.
        if (not Path(file_path_cars).exists() and
            not Path(file_path_index).exists()
        ):
            with open(file_path_cars, 'w') as file:
                file.write(f'{row_value_car}')
                
            row_value_index = f'{car.vin},1'.ljust(500) + '\n'

            with open(file_path_index, 'x') as ifile:
                ifile.write(f'{row_value_index}')

        # Если оба файла есть:
        # 1. Вычисляем кол-во строк и добавляем новую запись в конец.
        # 2. Сортируем файл с индексами и перезаписываем его.
        elif (Path(file_path_cars).exists() and
            Path(file_path_index).exists()
        ):
            # Добавляем запись в cars.txt
            with open(file_path_cars, "r+") as file:
                # Для подсчета уже записанных строк использую enumarate, чтобы можно 
                # было работать с большими файлами.
                for line_number, line in enumerate(file):
                    pass

                line_number += 1 
                file.seek(line_number * (501)) # длина строки 501, т.к. добавили символ перехода строки — он тоже считается.
                file.write(f'{row_value_car}')    
            
            row_value_index = f'{car.vin},{line_number + 1}'.ljust(500) + '\n'
            
            # Добавляем запись в индексный файл
            with open(file_path_index, 'r+') as ifile:
                ifile.seek(line_number * (501))
                ifile.write(f'{row_value_index}')

            # Сортировка индексного файла:
            # 1. Читаем строки в список.
            with open(file_path_index, 'r') as ifile:
                rows = [row for row in ifile]
            
            # 2. Т.к. vin - строка, можем сортировать список строк, не разбивая строки на элементы. 
            sorted_rows = sorted(rows)
            
            # 3. Перезаписываем индексный файл в отсортированном порядке.    
            with open(file_path_index, 'w') as ifile:
                line_number = 0    
                for row in sorted_rows:
                    ifile.seek(line_number * (501))
                    ifile.write(row)
                    line_number += 1
        
        # Во всех остальных случаях считаем, что что-то пошло не так - 
        # возвращаем сообщение об ошибке, переданную для записи модель и 
        # завершаем работу метода.
        else:
            print('Что-то пошло не так:()')
            return car

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        """Метод sell_car(Sale):
        1. Добавляет запись в файл sales.txt (факты продаж).
        2. Добавляет запись в индексный файл.
        3. Перестраивает индекс, чтобы сохранить корректную сортировку по ключу sales_number.
        4. Обновляет статус автомобиля в файле cars.txt - на sold.
        На будущее - добавить обработку ошибки "факт продаж ссылается на vin автомобиля, которого нет".
        """

        file_path_sales = f'{self.root_directory_path}/sales.txt' # Путь до файла с продажами
        file_path_index = f'{self.root_directory_path}/sales_index.txt' # Путь до файла с индексами
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами

        # Конструируем запись "продажа" в виде объекта json
        row_value_sale = (f'{{"sales_number" : "{sale.sales_number}", '
                            f'"car_vin" : "{sale.car_vin}", '
                            f'"sales_date" : "{sale.sales_date}", '
                            f'"cost" : {sale.cost}}}').ljust(500) + '\n'

        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Считаем, что sales и sales_index должны существовать одновременно.
        # Если обоих файлов нет, требуем, чтобы был cars.txt и создаем sales и sales_index,
        # добавляем первую запись о продаже.
        if (not Path(file_path_sales).exists() and
            not Path(file_path_index).exists() and
            Path(file_path_cars).exists() and
            Path(file_path_car_index).exists()
        ):
            with open(file_path_sales, 'w') as file:
                file.write(f'{row_value_sale}')
                
            row_value_index = f'{sale.sales_number},1'.ljust(500) + '\n'

            with open(file_path_index, 'x') as ifile:
                ifile.write(f'{row_value_index}')

            # Ищем в cars_index.txt номер строки с нужным vin.
            with open(file_path_car_index, 'r') as cifile:
                for row in cifile:
                    car_vin, car_index = tuple(row.split(','))
                    if car_vin == sale.car_vin:
                        car_index = int(car_index)
                        break

                if  car_vin == '':          
                    print(f'Ошибка. Автомобиль с vin = {sale.car_vin} не найден.')
                    return #TO DO: вернуть объект Sale

            # Ищем в cars.txt строку с нужным vin - номер строки нашли в cars_index.txt.
            with open(file_path_cars, 'r+') as cfile:
                cfile.seek(car_index)
                print(f'Найдена запись: {cfile.readline()}')

        # Если оба файла есть, требуем, чтобы был cars.txt:
        # 1. Вычисляем кол-во строк и добавляем новую запись в конец sales и sales_index.
        # 2. Сортируем sales_index и перезаписываем его.
        # 3. Обновляем cars.txt.
        elif (Path(file_path_sales).exists() and
            Path(file_path_index).exists()
        ):
            pass
            # # Добавляем запись в sales.txt
            # with open(file_path_sales, "r+") as file:
            #     # Для подсчета уже записанных строк использую enumarate, чтобы можно 
            #     # было работать с большими файлами.
            #     for line_number, line in enumerate(file):
            #         pass

            #     line_number += 1 
            #     file.seek(line_number * (501)) # длина строки 501, т.к. добавили символ перехода строки — он тоже считается.
            #     file.write(f'{row_value_sale}')    
            
            # row_value_index = f'{sale.sales_number},{line_number + 1}'.ljust(500) + '\n'
            
            # # Добавляем запись в индексный файл
            # with open(file_path_index, 'r+') as ifile:
            #     ifile.seek(line_number * (501))
            #     ifile.write(f'{row_value_index}')

            # # Сортировка индексного файла:
            # # 1. Читаем строки в список.
            # with open(file_path_index, 'r') as ifile:
            #     rows = [row for row in ifile]
            
            # # 2. Т.к. sales_number - строка, можем сортировать список строк, не разбивая строки на элементы. 
            # sorted_rows = sorted(rows)
            
            # # 3. Перезаписываем индексный файл в отсортированном порядке.    
            # with open(file_path_index, 'w') as ifile:
            #     line_number = 0    
            #     for row in sorted_rows:
            #         ifile.seek(line_number * (501))
            #         ifile.write(row)
            #         line_number += 1

            # # Обновляем запись в cars.txt
            # # TO DO
        
        # Во всех остальных случаях считаем, что что-то пошло не так - 
        # возвращаем сообщение об ошибке, переданный для записи факт продаж и 
        # завершаем работу метода.
        # На будущее - разделить обработку ошибок, например, выделить в отдельную 
        # ветку ситуацию, когда sales и sales_index уже существуют, а cars.txt нет.
        else:
            print('Что-то пошло не так:()')
            return # TO DO: возвращать объект "факт продажи"

        return # TO DO: возвращать объект "факт продажи"    

    
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
model = Model(id=5, name='Logan', brand='Renault')
print('Model row added: ', carservice.add_model(model))

model = Model(id=3, name='3', brand='Mazda')
print('Model row added: ', carservice.add_model(model))

model = Model(id=2, name='Optima', brand='Kia')
print('Model row added: ', carservice.add_model(model))

model = Model(id=4, name='Pathfinder', brand='Nissan')
print('Model row added: ', carservice.add_model(model))

model = Model(id=1, name='Sorento', brand='Kia')
print('Model row added: ', carservice.add_model(model))

# Добавление автомобилей
car = Car(vin='KNAGM4A77D5316538', model=1, price=2000, date_start='2024-02-08', status=CarStatus('available'))
print('Car row added: ', carservice.add_car(car))

car = Car(vin='5XYPH4A10GG021831', model=2, price=2300, date_start='2024-02-20', status=CarStatus('reserve'))
print('Car row added: ', carservice.add_car(car))

car = Car(vin='KNAGH4A48A5414970', model=1, price=2100, date_start='2024-04-04', status=CarStatus('available'))
print('Car row added: ', carservice.add_car(car))

car = Car(vin='JM1BL1TFXD1734246', model=3, price=2276.65, date_start='2024-05-17', status=CarStatus('available'))
print('Car row added: ', carservice.add_car(car))

car = Car(vin='JM1BL1M58C1614725', model=3, price=2549.10, date_start='2024-05-17', status=CarStatus('reserve'))
print('Car row added: ', carservice.add_car(car))

# Добавление продаж
# «код автосалона#номер продажи»
sale = Sale(sales_number='YASENEVO#1', car_vin='5XYPH4A10GG021831', sales_date='2025-03-17', cost=2300)
print('Sale row added: ', carservice.sell_car(sale))
# Проблемы
# Вложенный тип CarStatus
# Добавить обработку повторного добавления записи с уже существующим ключом