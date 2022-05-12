from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOUR_IN_MINUTE: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Метод или функция еще не реализованы.'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIE_1 * self.get_mean_speed()
             - self.COEFF_CALORIE_2)
            * self.weight / self.M_IN_KM
            * self.duration_h * self.HOUR_IN_MINUTE
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1: float = 0.035
    COEFF_2: float = 0.029
    COEFF_3: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        formula_1 = self.get_mean_speed() ** self.COEFF_3 // self.height
        formula_2 = self.COEFF_1 * self.weight
        + formula_1 * self.COEFF_2 * self.weight
        return formula_2 * self.duration_h * self.HOUR_IN_MINUTE


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration_h
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_SW_1: float = 1.1
        COEFF_SW_2: float = 2
        return (self.get_mean_speed() + COEFF_SW_1) * COEFF_SW_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in train:
        return train.get(workout_type)(*data)
    raise KeyError(
        f'Тренировка с данным ключом "{workout_type}" не найденна.'
    )


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
