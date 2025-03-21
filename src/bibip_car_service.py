from datetime import datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from pathlib import Path


class CarService:
    """Класс CarService позволяет работать с данными автосервиса: машинами,
    моделями, фактами продаж. При инициализации объекта задается директория,
    где будут лежать текстовые файлы с данными. Данные хранятся в виде списков
    элементов через запятую.
    """

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение моделей
    def add_model(self, model: Model) -> Model:
        """Метод add_model() принимает в качестве аргумента объект Model и
        добавляет запись в файл models.txt, а также в индексный файл
        models_index.txt. Индекс установлен на id модели.
        На будущее - добавить проверку на повторное добавление одной и той же
        модели."""

        # Пути до файлов с данными.
        file_path_models = f'{self.root_directory_path}/models.txt'
        file_path_index = f'{self.root_directory_path}/models_index.txt'

        # Конструируем запись "модель" в виде строки id,name,brand
        row_value_model = (
            f'{model.id},{model.name},{model.brand}'
            ).ljust(500) + '\n'

        # Проверяем, существует ли директория. Если нет, создаем.
        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Считаем, что оба файла (models и индексы) должны существовать
        # одновременно. Если обоих файлов нет, создаем их и добавляем
        # первую запись.
        if (
            not Path(file_path_models).exists() and
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
        elif (
            Path(file_path_models).exists() and
            Path(file_path_index).exists()
                ):
            # Добавляем запись в models.txt
            with open(file_path_models, "r+") as file:
                # Для подсчета уже записанных строк использую enumarate, чтобы
                # можно было работать с большими файлами, не загружая их в
                # память целиком.
                for line_number, line in enumerate(file):
                    pass

                line_number += 1
                # Длина строки 501, т.к. добавили символ перехода строки —
                # он тоже считается.
                file.seek(line_number * (501))
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
                    rows.append((int(model_id), int(index)))

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
        """Метод add_car() принимает в качестве аргумента объект Car и
        добавляет запись в файл cars.txt, а также в индексный файл
        cars_index.txt. Индекс установлен на VIN-номер машины.
        На будущее: 1. добавить обработку ошибки "добавлен автомобиль, для
        которого нет модели", 2. добавить обработку ситуации, когда повторно
        добавляется уже существующий VIN-номер.
        """

        # Пути до файлов с данными.
        file_path_cars = f'{self.root_directory_path}/cars.txt'
        file_path_index = f'{self.root_directory_path}/cars_index.txt'

        # Конструируем запись "автомобиль" в виде строки
        # vin,model,price,date_start,status.
        row_value_car = (
            f'{car.vin},{car.model},{car.price},'
            f'{car.date_start.strftime('%Y-%m-%d')},'
            f'{car.status}').ljust(500) + '\n'

        # Проверяем, существует ли директория. Если нет, создаем.
        Path(self.root_directory_path).mkdir(exist_ok=True)

        # Считаем, что оба файла (cars и индексы) должны существовать
        # одновременно. Если обоих файлов нет, создаем их и добавляем
        # первую запись.
        if (
            not Path(file_path_cars).exists() and
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
        elif (
            Path(file_path_cars).exists() and
            Path(file_path_index).exists()
        ):
            # Добавляем запись в cars.txt
            with open(file_path_cars, "r+") as file:
                # Для подсчета уже записанных строк использую enumarate, чтобы
                # можно было работать с большими файлами, не загружая их в
                # память целиком.
                for line_number, line in enumerate(file):
                    pass

                line_number += 1
                # Длина строки 501, т.к. добавили символ перехода строки — он
                # тоже считается.
                file.seek(line_number * (501))
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

            # 2. Т.к. vin - строка, можем сортировать список строк, не разбивая
            # строки на элементы.
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
        """Метод sell_car() принимает на вход объект "Факт продажи" (Sale):
        1. Добавляет запись в файл sales.txt (факты продаж).
        2. Добавляет запись в индексный файл.
        3. Перестраивает индекс, чтобы сохранить корректную сортировку по ключу
        sales_number.
        4. Обновляет статус автомобиля в файле cars.txt - на sold.
        Добавлена обработка ошибки "факт продаж ссылается на vin автомобиля,
        которого нет".
        """

        # Пути до файлов с данными.
        file_path_sales = f'{self.root_directory_path}/sales.txt'
        file_path_index = f'{self.root_directory_path}/sales_index.txt'
        file_path_cars = f'{self.root_directory_path}/cars.txt'
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt'

        # Конструируем запись "продажа" в виде строки
        # sales_number,car_vin,sales_date,cost.
        row_value_sale = (
            f'{sale.sales_number},{sale.car_vin},'
            f'{sale.sales_date.strftime('%Y-%m-%d')},{sale.cost},'
            f'{sale.is_deleted}'
            ).ljust(500) + '\n'

        # Создаем пустой объект Car - заполним его по ходу дела
        car = Car(
            vin=sale.car_vin,
            model=0,
            price=Decimal("0"),
            date_start=datetime(1900, 1, 1),
            status=CarStatus('available')
        )

        # Считаем, что sales и sales_index должны существовать одновременно.
        # Если обоих файлов нет, требуем, чтобы был cars.txt и его индекс и
        # создаем sales и sales_index, добавляем первую запись о продаже.
        if (
            not Path(file_path_sales).exists() and
            not Path(file_path_index).exists() and
            Path(file_path_cars).exists() and
            Path(file_path_car_index).exists()
        ):
            # Проверяем, существует ли автомобиль с таким vin - ищем значение
            # в cars_index.txt. Если такой записи нет, возвращаем сообщение об
            # ошибке - факт продаж не сохраняем.
            with open(file_path_car_index, 'r') as cifile:
                rows = {}
                for row in cifile:
                    car_vin, car_index = tuple(row.split(','))
                    rows[car_vin] = int(car_index)

                if sale.index() in rows:
                    car_index = rows[sale.index()]
                else:
                    print(f'Ошибка. Автомобиль с vin = {sale.index()} '
                          f'не найден.')
                    return

            with open(file_path_sales, 'w') as file:
                file.write(f'{row_value_sale}')

            row_value_index = f'{sale.sales_number},1'.ljust(500) + '\n'

            with open(file_path_index, 'x') as ifile:
                ifile.write(f'{row_value_index}')

            # Ищем в cars.txt строку с нужным vin - номер строки нашли в
            # cars_index.txt.
            with open(file_path_cars, 'r+') as cfile:
                cfile.seek((car_index - 1) * (501))
                rows = cfile.readline().rstrip().split(',')
                rows[4] = 'sold'  # Меняем статус машины на sold (продана)
                updated_row = ','.join(rows).ljust(500)
                cfile.seek((car_index - 1) * (501))
                cfile.write(updated_row)

        # Если оба файла есть, требуем, чтобы был cars.txt:
        # 1. Вычисляем кол-во строк и добавляем новую запись в конец sales и
        # sales_index.
        # 2. Сортируем sales_index и перезаписываем его.
        # 3. Обновляем cars.txt.
        elif (
            Path(file_path_sales).exists() and
            Path(file_path_index).exists() and
            Path(file_path_cars).exists() and
            Path(file_path_car_index).exists()
        ):
            # Проверяем, существует ли автомобиль с таким vin - ищем значение в
            # cars_index.txt. Если такой записи нет, возвращаем сообщение об
            # ошибке - факт продаж не сохраняем.
            with open(file_path_car_index, 'r') as cifile:
                rows = {}
                for row in cifile:
                    car_vin, car_index = tuple(row.split(','))
                    rows[car_vin] = int(car_index)

                if sale.index() in rows:
                    car_index = rows[sale.index()]
                else:
                    print(f'Ошибка. Автомобиль с vin = {sale.index()}'
                          f' не найден.')
                    return

            # Добавляем запись в sales.txt
            with open(file_path_sales, "r+") as file:
                # Для подсчета уже записанных строк использую enumarate, чтобы
                # можно было работать с большими файлами, не загружая их в
                # память целиком.
                for line_number, line in enumerate(file):
                    pass

                line_number += 1
                # длина строки 501, т.к. добавили символ перехода строки — он
                # тоже считается.
                file.seek(line_number * (501))
                file.write(f'{row_value_sale}')

            row_value_index = f'{sale.sales_number},'
            f'{line_number + 1}'.ljust(500) + '\n'

            # Добавляем запись в индексный файл
            with open(file_path_index, 'r+') as ifile:
                ifile.seek(line_number * (501))
                ifile.write(f'{row_value_index}')

            # Сортировка индексного файла:
            # 1. Читаем строки в список.
            with open(file_path_index, 'r') as ifile:
                rows = [row for row in ifile]

            # 2. Т.к. sales_number - строка, можем сортировать список строк,
            # не разбивая их на элементы.
            sorted_rows = sorted(rows)

            # 3. Перезаписываем индексный файл в отсортированном порядке.
            with open(file_path_index, 'w') as ifile:
                line_number = 0
                for row in sorted_rows:
                    ifile.seek(line_number * (501))
                    ifile.write(row)
                    line_number += 1

            # Ищем в cars.txt строку с нужным vin - номер строки нашли в
            # cars_index.txt.
            with open(file_path_cars, 'r+') as cfile:
                cfile.seek((car_index - 1) * (501))
                rows = cfile.readline().rstrip().split(',')
                rows[4] = 'sold'  # Обновляем статус машины на "Продана"
                car = Car(
                    vin=rows[0],
                    model=rows[1],
                    price=Decimal(rows[2]),
                    date_start=datetime.strptime(rows[3], '%Y-%m-%d'),
                    status=CarStatus(rows[4])
                )
                updated_row = ','.join(rows).ljust(500)
                cfile.seek((car_index - 1) * (501))
                cfile.write(updated_row)

        # Во всех остальных случаях считаем, что что-то пошло не так -
        # возвращаем сообщение об ошибке, переданный для записи факт продаж и
        # завершаем работу метода.
        # На будущее - разделить обработку ошибок, например, выделить в
        # отдельную ветку ситуацию, когда sales и sales_index уже существуют,
        # а cars.txt нет.
        else:
            print('Что-то пошло не так:()')
            return car

        return car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        """Метод get_cars() возвращает список автомобилей с заданным статусом.
        """

        # Путь до файла с данными.
        file_path_cars = f'{self.root_directory_path}/cars.txt'

        if (not Path(file_path_cars).exists()):
            print('Не найден файл с данными об автомобилях.')
            return

        cars_list = []
        with open(file_path_cars, "r") as file:
            # Используем enumarate, чтобы можно было работать с большими
            # файлами и не читать весь файл целиком в память.
            for line in enumerate(file):
                rows = line[1].rstrip().split(',')
                if rows[4] == status:  # Проверка на статус
                    car = Car(
                            vin=rows[0],
                            model=rows[1],
                            price=Decimal(rows[2]),
                            date_start=datetime.strptime(rows[3], '%Y-%m-%d'),
                            status=rows[4])
                    cars_list.append(car)

        # Закомментировала сортировку, т.к. с ней падает автотест.
        # cars_list.sort(key=lambda car: car.vin, reverse=False)

        return cars_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        """Метод get_car_info() принимает на вход VIN-номер автомобиля и
        возвращает информацию о нем:
        VIN-номер, название модели, название бренда, цену, дату начала продаж,
        статус, дату продажи (если есть), по какой цене был продан (если есть).
        """

        # Пути до файлов с данными.
        file_path_cars = f'{self.root_directory_path}/cars.txt'
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt'
        file_path_sales = f'{self.root_directory_path}/sales.txt'
        file_path_sales_index = f'{self.root_directory_path}/sales_index.txt'
        file_path_models = f'{self.root_directory_path}/models.txt'
        file_path_models_index = f'{self.root_directory_path}/models_index.txt'

        # Если какого-то из файлов нет, возвращаем ошибку и
        # завершаем работу метода.
        if (
            not Path(file_path_cars).exists() or
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
            price=Decimal("0"),
            date_start=datetime(1900, 1, 1),
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
            else:
                print(f'Ошибка. Автомобиль с vin = {vin} не найден.')
                return

        # Ищем машину в cars.txt - номер строки нашли в cars_index.txt.
        # Обновляем car_info.
        with open(file_path_cars, 'r') as cfile:
            cfile.seek((car_index - 1) * (501))
            rows = cfile.readline().rstrip().split(',')
            # Временно сохраняем сюда id модели в виде строки
            car_info.car_model_name = str(rows[1])
            car_info.price = Decimal(rows[2])
            car_info.date_start = datetime.strptime(rows[3], '%Y-%m-%d')
            car_info.status = CarStatus(rows[4])

        # Ищем модель по id в индексе
        with open(file_path_models_index, 'r') as mifile:
            rows = {}
            for row in mifile:
                model_id, model_index = tuple(row.split(','))
                rows[model_id] = int(model_index)

            # Здесь временно лежит id модели из cars.txt
            if car_info.car_model_name in rows:
                model_index = rows[car_info.car_model_name]
            else:
                print(
                    f'Ошибка. Модель с id = {car_info.car_model_name} '
                    f'не найдена.')
                return

        # Ищем модель в models.txt - номер строки нашли в models_index.txt.
        # Обновляем car_info.
        with open(file_path_models, 'r') as mfile:
            mfile.seek((model_index - 1) * (501))
            rows = mfile.readline().rstrip().split(',')
            car_info.car_model_name = rows[1]
            car_info.car_model_brand = rows[2]

        # Ищем запись о факте продаж в sales.txt. Индекса на vin нет, поэтому
        # разбираем файл построчно.
        # 1. Проверяем, есть ли файл с продажами. Если нет, возвращаем
        # car_info, который к этому времени уже заполнили. Дата и цена продажи
        # останутся None.
        if (
            not Path(file_path_sales).exists() and
            not Path(file_path_sales_index).exists()
        ):
            return car_info
        else:
            with open(file_path_sales, "r") as sfile:
                # Используем enumarate, чтобы можно было работать с большими
                # файлами и не читать весь файл целиком в память.
                for line in enumerate(sfile):
                    rows = line[1].rstrip().split(',')
                    if (
                        rows[1] == vin and
                        rows[4] == 'False'
                    ):  # Проверка на vin и на is_deleted=False
                        car_info.sales_date = datetime.strptime(
                            rows[2], '%Y-%m-%d')
                        car_info.sales_cost = Decimal(rows[3])
                        # Считаем, что запись о продаже машины может быть
                        # только одна или не существовать вовсе, поэтому если
                        # нашли, выходим из цикла. Если не нашли - в car_info
                        # останутся значения по умолчанию = None.
                        break

        return car_info

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        """Метод update_vin() принимает на вход старый VIN-номер и новый
        VIN-номер, на который нужно обновить. Значение обновляется только в
        файле cars.txt.
        На будущее: обновлять vin в sales.txt.
        """

        # Создаем два пустых объекта Car, чтобы возвращать их в разных
        # ситуациях.
        car = Car(
            vin=vin,  # Со "старым" vin, когда что-то пошло не так
            model=0,
            price=0,
            date_start='1900-01-01',
            status=CarStatus('available')
        )

        car_new = Car(
            vin=new_vin,  # С "новым" vin, когда все завершилось успешно
            model=0,
            price=0,
            date_start='1900-01-01',
            status=CarStatus('available')
        )

        # Пути до файлов с данными.
        file_path_cars = f'{self.root_directory_path}/cars.txt'
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt'

        # Если какого-то из файлов нет, возвращаем ошибку и завершаем работу
        # метода.
        if (
            not Path(file_path_cars).exists() or
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

            if vin in rows:
                # Сохраняем индекс vin, чтобы использовать его для замены в
                # cars.txt.
                car_index = rows[vin][1]
                car_index_row_num = rows[vin][0]

            else:
                print(f'Ошибка. Автомобиль с vin = {vin} не найден.')
                return car

            # Заменяем vin в индексе
            cifile.seek((car_index_row_num - 1) * (501))
            row = cifile.readline().rstrip().split(',')
            row[0] = new_vin
            updated_row = ','.join(row).ljust(500)
            cifile.seek((car_index_row_num - 1) * (501))
            cifile.write(updated_row)

        # Перестраиваем индекс
        # 1. Читаем строки в список.
        with open(file_path_car_index, 'r') as cifile:
            rows = [row for row in cifile]

            # 2. Т.к. sales_number - строка, можем сортировать список строк,
            # не разбивая их на элементы.
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
            car_new.model = rows[1]
            car_new.price = rows[2]
            car_new.date_start = rows[3]
            car_new.status = rows[4]

            rows[0] = new_vin
            updated_row = ','.join(rows).ljust(500)
            cfile.seek((car_index - 1) * (501))
            cfile.write(updated_row)

        return car_new

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        """Метод revert_sale() принимает на вход идентификатор продажи,
        помечает ее неактуальной (is_deleted = True) и обновляет статус
        автомобиля с sold на available.
        """

        # Создаем пустой объект Car, чтобы было, что возвращать.
        car = Car(
            vin='',
            model=0,
            price=Decimal("0"),
            date_start=datetime(1900, 1, 1),
            status=CarStatus('available')
        )

        # Пути до файлов с данными.
        file_path_sales = f'{self.root_directory_path}/sales.txt'
        file_path_sales_index = f'{self.root_directory_path}/sales_index.txt'
        file_path_cars = f'{self.root_directory_path}/cars.txt'
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt'

        # Если какого-то из файлов нет, возвращаем ошибку и завершаем работу
        # метода.
        if (
            not Path(file_path_sales).exists() or
            not Path(file_path_sales_index).exists() or
            not Path(file_path_cars).exists() or
            not Path(file_path_car_index).exists()
        ):
            print('Ошибка. Не существует один или несколько файлов с данными.')
            return car

        # Проверяем, существует ли продажа с переданным sales_number - ищем
        # значение в sales_index.txt.
        # Если такой записи нет, возвращаем сообщение об ошибке.
        with open(file_path_sales_index, 'r') as sifile:
            rows = {}
            for row in sifile:
                sales_number, sales_index = tuple(row.split(','))
                rows[sales_number] = int(sales_index)

            if sales_number in rows:
                sales_index = rows[sales_number]
            else:
                print(f'Ошибка. Факт продажи {sales_number} не найден.')
                return car

        # Делаем update продажи в sales.txt - проставляем записи флаг
        # is_deleted = True.
        with open(file_path_sales, 'r+') as sfile:
            sfile.seek((sales_index - 1) * (501))
            rows = sfile.readline().rstrip().split(',')
            rows[4] = str(True)
            # Сохраняем vin машины с отмененной продажей.
            reset_sale_vin = rows[1]
            updated_row = ','.join(rows).ljust(500)
            sfile.seek((sales_index - 1) * (501))
            sfile.write(updated_row)

        # Делаем update машины в cars.txt - проставляем статус = available
        # 1. Ищем индекс машины по vin
        with open(file_path_car_index, 'r') as cifile:
            rows = {}
            for row in cifile:
                car_vin, car_index = tuple(row.split(','))
                rows[car_vin] = int(car_index)

            if reset_sale_vin in rows:
                car_index = rows[reset_sale_vin]
            else:
                print(f'Ошибка. Автомобиль с vin = {reset_sale_vin} '
                      f'не найден.')
                return car

        # 2. Ищем машину в cars.txt - номер строки нашли в cars_index.txt.
        # Обновляем объект car.
        # Обновляем поле с vin в файле.
        with open(file_path_cars, 'r+') as cfile:
            cfile.seek((car_index - 1) * (501))
            rows = cfile.readline().rstrip().split(',')
            car.vin = rows[0]
            car.model = rows[1]
            car.price = rows[2]
            car.date_start = rows[3]
            car.status = CarStatus("available")

            rows[4] = CarStatus("available")
            updated_row = ','.join(rows).ljust(500)
            cfile.seek((car_index - 1) * (501))
            cfile.write(updated_row)

        return car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        """Метод top_models_by_sales() возвращает топ-3 моделей,
        отсортированных по: кол-ву продаж, суммарной стоимости продаж,
        все по убыванию.
        """

        # Путь до файла с данными.
        file_path_car_index = f'{self.root_directory_path}/cars_index.txt'

        # Если файла нет, возвращаем ошибку и завершаем работу метода.
        if (
            not Path(file_path_car_index).exists()
        ):
            print('Ошибка. Не существует файла с данными.')
            return

        # Читаем индексный файл в цикле.
        # Для каждого vin вызываем get_car_info() и накапливаем информацию о
        # кол-ве продаж и суммарной стоимости в словаре - ключом будет название
        # модели, считаем, что оно уникально.
        top_models = {}
        with open(file_path_car_index, 'r') as cifile:
            for row in cifile:
                car_vin = tuple(row.split(','))[0]
                info = self.get_car_info(car_vin)

                # Если модель добавляется в словарь первый раз
                if (
                    info.car_model_name not in top_models and
                    info.sales_date is not None
                ):

                    top_models[info.car_model_name] = [
                        info.car_model_brand,
                        1,
                        info.sales_cost]
                # Если модель уже есть в словаре
                elif (
                    info.car_model_name in top_models and
                    info.sales_date is not None
                ):

                    top_models[info.car_model_name][1] += 1
                    top_models[info.car_model_name][2] += info.sales_cost

        # Сортируем словарь по двум параметрам: кол-ву продаж и сумме продаж,
        # все - по убыванию.
        sorted_top = dict(
            sorted(top_models.items(), key=lambda item: (
                -item[1][1], -item[1][2]
                ))
            )

        # Отрезаем лишние элементы словаря - оставляем первые три.
        while len(sorted_top) > 3:
            sorted_top.popitem()

        # Заполняем список объектов ModelSaleStats из отсортированного списка.
        top_models_list = [
            ModelSaleStats(
                car_model_name=key,
                brand=value[0],
                sales_number=value[1]) for key, value in sorted_top.items()
            ]
        return top_models_list
