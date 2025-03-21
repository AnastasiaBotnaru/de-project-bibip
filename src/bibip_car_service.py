from datetime import date, datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from pathlib import Path


class CarService:
    """Хранение данных организовано в виде списков элементов через запятую.
    С такими записями проще взаимодействовать, чем с json-ами.
    """

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение моделей
    def add_model(self, model: Model) -> Model:
        file_path_models = f'{self.root_directory_path}/models.txt' # Путь до файла с моделями
        file_path_index = f'{self.root_directory_path}/models_index.txt' # Путь до файла с индексами

        # Конструируем запись "модель" в виде строки id,name,brand
        row_value_model = (f'{model.id},{model.name},{model.brand}').ljust(500) + '\n'

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

        # Конструируем запись "автомобиль" в виде строки vin,model,price,date_start,status
        row_value_car = (f'{car.vin},{car.model},{car.price},{car.date_start.strftime('%Y-%m-%d')},{car.status}').ljust(500) + '\n'

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
        """Метод "продать автомобиль" принимает на вход объект "Факт продажи":
        1. Добавляет запись в файл sales.txt (факты продаж).
        2. Добавляет запись в индексный файл.
        3. Перестраивает индекс, чтобы сохранить корректную сортировку по ключу sales_number.
        4. Обновляет статус автомобиля в файле cars.txt - на sold.
        Добавлена обработка ошибки "факт продаж ссылается на vin автомобиля, которого нет".
        """

        file_path_sales = f'{self.root_directory_path}/sales.txt' # Путь до файла с продажами
        file_path_index = f'{self.root_directory_path}/sales_index.txt' # Путь до файла с индексами
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами

        # Конструируем запись "продажа" в виде строки sales_number,car_vin,sales_date,cost
        row_value_sale = (
            f'{sale.sales_number},{sale.car_vin},{sale.sales_date.strftime('%Y-%m-%d')},{sale.cost},{sale.is_deleted}'
            ).ljust(500) + '\n'

        # Считаем, что sales и sales_index должны существовать одновременно.
        # 
        # Если обоих файлов нет, требуем, чтобы был cars.txt и его индекс и создаем sales и sales_index,
        # добавляем первую запись о продаже.
        if (not Path(file_path_sales).exists() and
            not Path(file_path_index).exists() and
            Path(file_path_cars).exists() and
            Path(file_path_car_index).exists()
        ):
            # Проверяем, существует ли автомобиль с таким vin - ищем значение в cars_index.txt.
            # Если такой записи нет, возвращаем сообщение об ошибке - факт продаж не сохраняем.
            with open(file_path_car_index, 'r') as cifile:
                rows = {}
                for row in cifile:
                    car_vin, car_index = tuple(row.split(','))
                    rows[car_vin] = int(car_index)
                    
                if sale.index() in rows:
                    car_index = rows[sale.index()]
                    print(f'vin нашелся')
                else:
                    print(f'Ошибка. Автомобиль с vin = {sale.index()} не найден.')
                    return
                
            print(f'Ветка 1 - первая запись о продаже. car_vin = {sale.index()}')
            print(f'{rows}')
            
            with open(file_path_sales, 'w') as file:
                file.write(f'{row_value_sale}')
                
            row_value_index = f'{sale.sales_number},1'.ljust(500) + '\n'

            with open(file_path_index, 'x') as ifile:
                ifile.write(f'{row_value_index}')

            # Ищем в cars.txt строку с нужным vin - номер строки нашли в cars_index.txt.
            with open(file_path_cars, 'r+') as cfile:
                cfile.seek((car_index - 1) * (501))
                rows = cfile.readline().rstrip().split(',')
                print(rows)
                rows[4] = 'sold'
                updated_row = ','.join(rows).ljust(500)
                print(len(updated_row))
                cfile.seek((car_index - 1) * (501))
                cfile.write(updated_row)
                print(rows)
                print(updated_row)

        # Если оба файла есть, требуем, чтобы был cars.txt:
        # 1. Вычисляем кол-во строк и добавляем новую запись в конец sales и sales_index.
        # 2. Сортируем sales_index и перезаписываем его.
        # 3. Обновляем cars.txt.
        elif (Path(file_path_sales).exists() and
            Path(file_path_index).exists() and
            Path(file_path_cars).exists() and
            Path(file_path_car_index).exists()
        ):
            # Проверяем, существует ли автомобиль с таким vin - ищем значение в cars_index.txt.
            # Если такой записи нет, возвращаем сообщение об ошибке - факт продаж не сохраняем.
            with open(file_path_car_index, 'r') as cifile:
                rows = {}
                for row in cifile:
                    car_vin, car_index = tuple(row.split(','))
                    rows[car_vin] = int(car_index)
                    
                if sale.index() in rows:
                    car_index = rows[sale.index()]
                    print(f'vin нашелся')
                else:
                    print(f'Ошибка. Автомобиль с vin = {sale.index()} не найден.')
                    return
                
            print(f'Ветка 2 - не первая запись о продаже. car_vin = {sale.index()}')
            print(f'{rows}')

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

            # Ищем в cars.txt строку с нужным vin - номер строки нашли в cars_index.txt.
            with open(file_path_cars, 'r+') as cfile:
                cfile.seek((car_index - 1) * (501))
                rows = cfile.readline().rstrip().split(',')
                print(rows)
                rows[4] = 'sold'
                updated_row = ','.join(rows).ljust(500)
                print(len(updated_row))
                cfile.seek((car_index - 1) * (501))
                cfile.write(updated_row)
                print(rows)
                print(updated_row)
                
                # TO DO: тут заполняем объект car, чтобы вернуть его из метода
        
        # Во всех остальных случаях считаем, что что-то пошло не так - 
        # возвращаем сообщение об ошибке, переданный для записи факт продаж и 
        # завершаем работу метода.
        # На будущее - разделить обработку ошибок, например, выделить в отдельную 
        # ветку ситуацию, когда sales и sales_index уже существуют, а cars.txt нет.
        else:
            print('Что-то пошло не так:()')
            return

        return # TO DO: возвращать объект "автомобиль"    

    
    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        """Дописать проверку на существование файла cars.txt. Если его нет, 
        возвращать сообщение об ошибке."""
        
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями

        cars_list = []
        with open(file_path_cars, "r") as file:
                # Используем enumarate, чтобы можно было работать с большими файлами
                # и не читать весь файл целиком в память.
                for line in enumerate(file):
                    rows = line[1].rstrip().split(',')
                    if rows[4] == status: # проверка на статус
                        car = Car(
                                vin=rows[0],
                                model=rows[1],
                                price=rows[2],
                                date_start=rows[3],
                                status=rows[4])
                        cars_list.append(car)    

        # cars_list.sort(key=lambda car: car.vin, reverse=False)

        return cars_list


    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
    
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами
        file_path_sales = f'{self.root_directory_path}/sales.txt' # Путь до файла с продажами
        file_path_sales_index = f'{self.root_directory_path}/sales_index.txt' # Путь до файла с индексами
        file_path_models = f'{self.root_directory_path}/models.txt' # Путь до файла с моделями
        file_path_models_index = f'{self.root_directory_path}/models_index.txt' # Путь до файла с индексами

        # Если какого-то из файлов нет, возвращаем ошибку и завершаем работу метода
        if (not Path(file_path_cars).exists() or
            not Path(file_path_car_index).exists() or
            not Path(file_path_models).exists() or
            not Path(file_path_models_index).exists()
        ):
            print('Ошибка. Не существует один или несколько файлов с данными.')
            return

        # Создаем пустой объект CarFullInfo - заполним его по ходу дела
        car_info = CarFullInfo(
            vin=vin,
            car_model_name='',
            car_model_brand='',
            price=0,
            date_start='1900-01-01',
            status=CarStatus('available'),
            sales_date=None,
            sales_cost=None
            )
        
        # Ищем машину по vin в индексе
        with open(file_path_car_index, 'r') as cifile:
                rows = {}
                for row in cifile:
                    car_vin, car_index = tuple(row.split(','))
                    rows[car_vin] = int(car_index)
                    
                if vin in rows:
                    car_index = rows[vin]
                    # print(f'Задание 4. vin нашелся')
                else:
                    # print(f'Задание 4. Ошибка. Автомобиль с vin = {vin} не найден.')
                    return 
                
        # Ищем машину в cars.txt - номер строки нашли в cars_index.txt.
        # Обновляем car_info.
        with open(file_path_cars, 'r') as cfile:
            cfile.seek((car_index - 1) * (501))
            rows = cfile.readline().rstrip().split(',')
            # print(f'Задание 4. Ищем машину по vin: {rows}')
            car_info.car_model_name = str(rows[1]) # Временно сохраняем сюда id модели в виде строки
            car_info.price = Decimal(rows[2])
            car_info.date_start = datetime.strptime(rows[3], '%Y-%m-%d') #date_start=datetime(2024, 2, 8),
            car_info.status = CarStatus(rows[4])
            # print(f'Задание 4. Обновили объект car_info: {car_info}')

        # Ищем модель по id в индексе
        with open(file_path_models_index, 'r') as mifile:
                rows = {}
                for row in mifile:
                    model_id, model_index = tuple(row.split(','))
                    rows[model_id] = int(model_index)
                # print(f'Задание 4. Заполняем rows записями из индекса моделей: {rows}')    
                    
                if car_info.car_model_name in rows: # Здесь временно лежит id модели из cars.txt
                    model_index = rows[car_info.car_model_name]
                    # print(f'Задание 4. id модели нашелся. Индекс - {model_index}, {rows[car_info.car_model_name]}')
                else:
                    # print(f'Задание 4. Ошибка. Модель с id = {car_info.car_model_name} не найдена.')
                    return
                
        # Ищем модель в models.txt - номер строки нашли в models_index.txt.
        # Обновляем car_info.
        with open(file_path_models, 'r') as mfile:
            mfile.seek((model_index - 1) * (501))
            rows = mfile.readline().rstrip().split(',')
            # print(f'Задание 4. Ищем модель по id: {rows}')
            car_info.car_model_name = rows[1]
            car_info.car_model_brand = rows[2]
            # print(f'Задание 4. Обновили объект car_info: {car_info}')

        # Ищем запись о факте продаж в sales.txt. Индекса на vin нет, поэтому разбираем файл построчно.
        # 1. Проверяем, есть ли файл с продажами. Если нет, возвращаем car_info, который к этому времени
        # уже заполнили. Дата и цена продажи останутся None.
        if (not Path(file_path_sales).exists() and
            not Path(file_path_sales_index).exists()
        ):
            return car_info
        else:
            with open(file_path_sales, "r") as sfile:
                    # Используем enumarate, чтобы можно было работать с большими файлами
                    # и не читать весь файл целиком в память.
                    for line in enumerate(sfile):
                        rows = line[1].rstrip().split(',')
                        if (
                            rows[1] == vin and
                            rows[4] == 'False'
                            ): # проверка на vin и на is_deleted=False
                            car_info.sales_date = datetime.strptime(rows[2], '%Y-%m-%d')
                            car_info.sales_cost = Decimal(rows[3])  
                            # Считаем, что запись о продаже машины может быть только одна или не
                            # существовать вовсе, поэтому если нашли, выходим из цикла.
                            # Если не нашли - в car_info останутся значения по умолчанию = None.
                            break     

        return car_info

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        """На будущее: обновлять vin в sales.txt."""
        
        # Создаем два пустых объекта Car, чтобы возвращать их в разных ситуациях.
        car = Car(
            vin=vin, # Со "старым" vin, когда что-то пошло не так
            model=0,
            price=0,
            date_start='1900-01-01',
            status=CarStatus('available')
        )

        car_new = Car(
            vin=new_vin, # С "новым" vin, когда все завершилось успешно
            model=0,
            price=0,
            date_start='1900-01-01',
            status=CarStatus('available')
        )
        
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами
        
        # Если какого-то из файлов нет, возвращаем ошибку и завершаем работу метода
        if (not Path(file_path_cars).exists() or
            not Path(file_path_car_index).exists()
        ):
            print('Ошибка. Не существует один или несколько файлов с данными.')
            return car

        # Ищем машину по vin в индексе
        with open(file_path_car_index, 'r+') as cifile:
            # Используем enumerate, чтобы за один прием достать и сохранить:
            # номер строки в индексном файле,
            # номер vin,
            # индекс vin. 
            rows = {}
            for line in enumerate(cifile):
                row = line[1].rstrip().split(',')
                # ключ словаря - vin,
                # первый элемент списка - номер строки в индексе,
                # второй элемент - номер строки в файле cars.txt
                rows[row[0]] = [line[0] + 1, int(row[1])] 
                print(f'Задание 5. В словарь rows добавили запись - {rows}')
            
            if vin in rows:
                car_index = rows[vin][1] # Сохраняем индекс vin, чтобы использовать его для замены в cars.txt
                car_index_row_num = rows[vin][0]
                print(f'Задание 5. vin нашелся: rows[{row[0]}] = {rows[row[0]]}')
            else:
                print(f'Задание 5. Ошибка. Автомобиль с vin = {vin} не найден.')
                return car
                
            # Заменяем vin в индексе
            cifile.seek((car_index_row_num - 1) * (501))
            row = cifile.readline().rstrip().split(',')
            row[0] = new_vin
            updated_row = ','.join(row).ljust(500)
            cifile.seek((car_index_row_num - 1) * (501))
            cifile.write(updated_row)
            print(f'Задание 5. Обновили строку в индексе - {updated_row}')
            
        # Перестраиваем индекс
        # 1. Читаем строки в список.
        with open(file_path_car_index, 'r') as cifile:
            rows = [row for row in cifile]
            
            # 2. Т.к. sales_number - строка, можем сортировать список строк, не разбивая строки на элементы. 
            sorted_rows = sorted(rows)
            
            # 3. Перезаписываем индексный файл в отсортированном порядке.    
            with open(file_path_car_index, 'w') as cifile:
                line_number = 0    
                for row in sorted_rows:
                    cifile.seek(line_number * (501))
                    cifile.write(row)
                    line_number += 1
                
        # Ищем машину в cars.txt - номер строки нашли в cars_index.txt.
        # Обновляем объект car.
        # Обновляем поле с vin в файле.
        with open(file_path_cars, 'r+') as cfile:
            cfile.seek((car_index - 1) * (501))
            rows = cfile.readline().rstrip().split(',')
            print(f'Задание 5. Ищем машину по vin: {rows}')
            car_new.model = rows[1]
            car_new.price = rows[2]
            car_new.date_start = rows[3]
            car_new.status = rows[4]

            rows[0] = new_vin
            updated_row = ','.join(rows).ljust(500)
            cfile.seek((car_index - 1) * (501))
            cfile.write(updated_row)
            print(f'Задание 5. Обновили vin: {updated_row}')

        return car_new

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        
        # Создаем пустой объект Car, чтобы было, что возвращать.
        car = Car(
            vin='',
            model=0,
            price=0,
            date_start='1900-01-01',
            status=CarStatus('available')
        )

        file_path_sales = f'{self.root_directory_path}/sales.txt' # Путь до файла с продажами
        file_path_sales_index = f'{self.root_directory_path}/sales_index.txt' # Путь до файла с индексами
        file_path_cars = f'{self.root_directory_path}/cars.txt' # Путь до файла с автомобилями
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt' # Путь до файла с индексами

        # Если какого-то из файлов нет, возвращаем ошибку и завершаем работу метода
        if (not Path(file_path_sales).exists() or
            not Path(file_path_sales_index).exists() or
            not Path(file_path_cars).exists() or
            not Path(file_path_car_index).exists()
        ):
            print('Ошибка. Не существует один или несколько файлов с данными.')
            return car
        
        # Проверяем, существует ли продажа с переданным sales_number - ищем значение в sales_index.txt.
        # Если такой записи нет, возвращаем сообщение об ошибке.
        with open(file_path_sales_index, 'r') as sifile:
            rows = {}
            for row in sifile:
                sales_number, sales_index = tuple(row.split(','))
                rows[sales_number] = int(sales_index)
                    
            if sales_number in rows:
                sales_index = rows[sales_number]
                print(f'Задание 6. Факт продажи {sales_number} нашелся.')
            else:
                print(f'Задание 6. Ошибка. Факт продажи {sales_number} не найден.')
                return car

        # Делаем update продажи в sales.txt - проставляем записи флаг is_deleted = True
        with open(file_path_sales, 'r+') as sfile:
            sfile.seek((sales_index - 1) * (501))
            rows = sfile.readline().rstrip().split(',')
            print(f'Задание 6. Ищем продажу по sales_number: {rows}')
            rows[4] = str(True)
            reset_sale_vin = rows[1] # Сохраняем vin машины с отмененной продажей
            updated_row = ','.join(rows).ljust(500)
            sfile.seek((sales_index - 1) * (501))
            sfile.write(updated_row)
            print(f'Задание 6. Обновили флаг активности у продажи: {updated_row}')

        # Делаем update машины в cars.txt - проставляем статус = available
        # 1. Ищем индекс машины по vin
        with open(file_path_car_index, 'r') as cifile:
            rows = {}
            for row in cifile:
                car_vin, car_index = tuple(row.split(','))
                rows[car_vin] = int(car_index)
                    
            if reset_sale_vin in rows:
                car_index = rows[reset_sale_vin]
                print(f'Задание 6. vin с удаленной продажей {reset_sale_vin} нашелся в cars.txt')
            else:
                print(f'Задание 6. Ошибка. Автомобиль с vin = {vin} не найден.')
                return car

        # 2. Ищем машину в cars.txt - номер строки нашли в cars_index.txt.
        # Обновляем объект car.
        # Обновляем поле с vin в файле.
        with open(file_path_cars, 'r+') as cfile:
            cfile.seek((car_index - 1) * (501))
            rows = cfile.readline().rstrip().split(',')
            print(f'Задание 6. Ищем машину по vin: {rows}')
            car.vin = rows[0]
            car.model = rows[1]
            car.price = rows[2]
            car.date_start = rows[3]
            car.status = CarStatus("available")

            rows[4] = CarStatus("available")
            updated_row = ','.join(rows).ljust(500)
            cfile.seek((car_index - 1) * (501))
            cfile.write(updated_row)
            print(f'Задание 6. Обновили статус: {updated_row}')

        return car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError

# Отладка
carservice = CarService('database')
# # Добавление моделей
# model = Model(id=5, name='Logan', brand='Renault')
# print('Model row added: ', carservice.add_model(model))

# model = Model(id=3, name='3', brand='Mazda')
# print('Model row added: ', carservice.add_model(model))

# model = Model(id=2, name='Optima', brand='Kia')
# print('Model row added: ', carservice.add_model(model))

# model = Model(id=4, name='Pathfinder', brand='Nissan')
# print('Model row added: ', carservice.add_model(model))

# model = Model(id=1, name='Sorento', brand='Kia')
# print('Model row added: ', carservice.add_model(model))

# # Добавление автомобилей
# car = Car(vin='KNAGM4A77D5316538', model=1, price=2000, date_start='2024-02-08', status=CarStatus('available'))
# print('Car row added: ', carservice.add_car(car))

# car = Car(vin='5XYPH4A10GG021831', model=2, price=2300, date_start='2024-02-20', status=CarStatus('reserve'))
# print('Car row added: ', carservice.add_car(car))

# car = Car(vin='KNAGH4A48A5414970', model=1, price=2100, date_start='2024-04-04', status=CarStatus('available'))
# print('Car row added: ', carservice.add_car(car))

# car = Car(vin='JM1BL1TFXD1734246', model=3, price=2276.65, date_start='2024-05-17', status=CarStatus('available'))
# print('Car row added: ', carservice.add_car(car))

# car = Car(vin='JM1BL1M58C1614725', model=3, price=2549.10, date_start='2024-05-17', status=CarStatus('reserve'))
# print('Car row added: ', carservice.add_car(car))

# car = Car(vin='VC1BL1M58C1614725', model=5, price=4540.10, date_start='2025-02-10', status=CarStatus('available'))
# print('Car row added: ', carservice.add_car(car)) # Для замены vin

# # Добавление продаж
# # «код автосалона#номер продажи»
# sale = Sale(sales_number='YASENEVO#1', car_vin='5XYPH4A10GG021831', sales_date='2025-03-17', cost=2300, is_deleted=False)
# print('Sale row added: ', carservice.sell_car(sale))

# # несуществующий vin
# sale = Sale(sales_number='BOBROVO#9', car_vin='JM1BL1M58C1614725', sales_date='2025-03-10', cost=2400, is_deleted=False)
# print('Sale row added: ', carservice.sell_car(sale))

# sale = Sale(sales_number='YASENEVO#1', car_vin='JM1BL1TFXD1734246', sales_date='2025-03-10', cost=2700, is_deleted=False)
# print('Sale row added: ', carservice.sell_car(sale))

# car = Car(vin='KNAGM4A77D5316549', model=1, price=4050, date_start='2024-02-08', status=CarStatus('available'))
# print('Car row added: ', carservice.add_car(car))

# car = Car(vin='5XYPH4A10GG021999', model=2, price=7300, date_start='2024-02-20', status=CarStatus('reserve'))
# print('Car row added: ', carservice.add_car(car))

# print(carservice.get_cars(CarStatus('available')))

# print(carservice.get_car_info('5XYPH4A10GG021999')) # Нет записи в продажах

full_info_no_sale = CarFullInfo(
            vin="KNAGM4A77D5316538",
            car_model_name="Optima",
            car_model_brand="Kia",
            price=Decimal("2000"),
            date_start=datetime(2024, 2, 8),
            status=CarStatus.available,
            sales_date=None,
            sales_cost=None,
        )

sale = Sale(
            sales_number="20240903#KNAGM4A77D5316538",
            car_vin="KNAGM4A77D5316538",
            sales_date=datetime(2024, 9, 3),
            cost=Decimal("2999.99"),
        )

full_info_with_sale = CarFullInfo(
            vin="KNAGM4A77D5316538",
            car_model_name="Optima",
            car_model_brand="Kia",
            price=Decimal("2000"),
            date_start=datetime(2024, 2, 8),
            status=CarStatus.sold,
            sales_date=sale.sales_date,
            sales_cost=sale.cost,
        )

# if carservice.get_car_info("KNAGM4A77D5316538") == full_info_with_sale:
#     print('ok')
# else:
#     print('err')
#     print(carservice.get_car_info("KNAGM4A77D5316538"))
#     print(full_info_with_sale)

# if full_info_no_sale == carservice.get_car_info('KNAGM4A77D5316538'):
#         print('ok')
# else:
#     print('err')

# # Замена vin

# print(carservice.update_vin('VC1BL1M58C1614725', 'AA1BL1M58C5555555')) #исходный - VC1BL1M58C1614725

# # Отмена продажи JM1BL1TFXD1734246

# print(carservice.revert_sale('YASENEVO#1'))

# Добавила обработку продажи с несуществующим vin - показывается сообщение об ошибке
# Отсортировала по вин-номеру список объектов car, которые возвращает get_cars()
# Задание 4: протестировала сценарии: нет/есть запись в продажах
# Задание 4: есть проверка на существование файлов, наличие vin, id модели
# TO DO:
# Добавить обработку повторного добавления записи с уже существующим ключом
# Добавить проверку на существование cars.txt в методе get_cars()