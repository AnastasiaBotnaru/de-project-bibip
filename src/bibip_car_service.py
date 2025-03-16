from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from pathlib import Path


class CarService:
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
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами

        # Конструируем запись "автомобиль" в виде объекта json
        row_value_car = (f'{{"vin" : "{car.vin}", '
                            f'"model" : {car.model}, '
                            f'"price" : "{car.price}", '
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
        """Метод добавляет запись в файл sales.txt (факты продаж), добавляет запись в индексный файл.
        Перестраивает индекс, чтобы сохранить корректную сортировку по ключу sales_number.
        Обновляет статус автомобиля в файле cars.txt - на sold.
        """

        file_path_sales = f'{self.root_directory_path}/sales.txt' # Путь до файла с продажами
        file_path_index = f'{self.root_directory_path}/sales_index.txt' # Путь до файла с индексами

        # Конструируем запись "продажа" в виде объекта json
        row_value_sale = (f'{{"sales_number" : "{sale.sales_number}", '
                            f'"car_vin" : "{sale.car_vin}", '
                            f'"sales_date" : "{sale.sales_date}", '
                            f'"cost" : {sale.cost}}}').ljust(500) + '\n'

        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Считаем, что оба файла (sales и индексы) должны существовать одновременно.
        # Если обоих файлов нет, создаем их и добавляем первую запись.
        if (not Path(file_path_sales).exists() and
            not Path(file_path_index).exists()
        ):
            with open(file_path_sales, 'w') as file:
                file.write(f'{row_value_sale}')
                
            row_value_index = f'{sale.sales_number},1'.ljust(500) + '\n'

            with open(file_path_index, 'x') as ifile:
                ifile.write(f'{row_value_index}')

        # Если оба файла есть:
        # 1. Вычисляем кол-во строк и добавляем новую запись в конец.
        # 2. Сортируем файл с индексами и перезаписываем его.
        elif (Path(file_path_sales).exists() and
            Path(file_path_index).exists()
        ):
            # Добавляем запись в sales.txt
            with open(file_path_sales, "r+") as file:
                # Для подсчета уже записанных строк использую enumarate, чтобы можно 
                # было работать с большими файлами.
                for line_number, line in enumerate(file):
                    pass

                line_number += 1 
                file.seek(line_number * (501)) # длина строки 501, т.к. добавили символ перехода строки — он тоже считается.
                file.write(f'{row_value_sale}')    
            
            row_value_index = f'{sale.sales_number},{line_number + 1}'.ljust(500) + '\n'
            
            # Добавляем запись в индексный файл
            with open(file_path_index, 'r+') as ifile:
                ifile.seek(line_number * (501))
                ifile.write(f'{row_value_index}')

            # Сортировка индексного файла:
            # 1. Читаем строки в список.
            with open(file_path_index, 'r') as ifile:
                rows = [row for row in ifile]
            
            # 2. Т.к. sales_number - строка, можем сортировать список строк, не разбивая строки на элементы. 
            sorted_rows = sorted(rows)
            
            # 3. Перезаписываем индексный файл в отсортированном порядке.    
            with open(file_path_index, 'w') as ifile:
                line_number = 0    
                for row in sorted_rows:
                    ifile.seek(line_number * (501))
                    ifile.write(row)
                    line_number += 1

            # Обновляем запись в cars.txt
            # TO DO
        
        # Во всех остальных случаях считаем, что что-то пошло не так - 
        # возвращаем сообщение об ошибке, переданную для записи модель и 
        # завершаем работу метода.
        else:
            print('Что-то пошло не так:()')
            return # TO DO: возвращать объект "автомобиль"

        return # TO DO: возвращать объект "автомобиль"    

    
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
print('Row added: ', carservice.add_model(model))

model = Model(id=3, name='3', brand='Mazda')
print('Row added: ', carservice.add_model(model))

model = Model(id=9, name='Optima', brand='Kia')
print('Row added: ', carservice.add_model(model))

model = Model(id=4, name='Pathfinder', brand='Nissan')
print('Row added: ', carservice.add_model(model))

model = Model(id=100, name='Sorento', brand='Kia')
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