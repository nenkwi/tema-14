from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Employee:
    name: str
    role: str


class Employer:


    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Кількість робочих місць має бути більшою за 0.")
        self._slots: list[Optional[Employee]] = [None] * capacity

    @property
    def capacity(self) -> int:
        return len(self._slots)

    def has_vacancies(self) -> bool:
        return any(slot is None for slot in self._slots)

    def hire(self, name: str, role: str) -> bool:

        name = name.strip()
        role = role.strip()

        if not name or not role:
            print("❌ Помилка: ім'я працівника та посада не можуть бути порожніми.")
            return False

        for idx, slot in enumerate(self._slots):
            if slot is None:
                self._slots[idx] = Employee(name=name, role=role)
                print(f"✅ Успіх: {name} ({role}) прийнятий(-а) на робоче місце №{idx}.")
                return True

        print("❌ Помилка: немає вакантних посад! Усі робочі місця зайняті.")
        return False

    def fire(self, i: int) -> bool:

        if i < 0 or i >= len(self._slots):
            print(
                f"❌ Помилка: індекс робочого місця {i} виходить за межі "
                f"(допустимий діапазон: 0..{len(self._slots) - 1})."
            )
            return False

        slot = self._slots[i]
        if slot is None:
            print(f"❌ Помилка: робоче місце №{i} уже вільне (немає кого звільняти).")
            return False

        print(f"ℹ️ Робоче місце №{i} звільнено (працівник {slot.name}, посада: {slot.role}).")
        self._slots[i] = None
        return True

    def show_status(self) -> None:
        print(f"\n--- Стан робочих місць (всього: {self.capacity}) ---")
        for idx, slot in enumerate(self._slots):
            if slot is None:
                print(f"  [{idx}] Вільне місце")
            else:
                print(f"  [{idx}] {slot.name} — {slot.role}")
        print("--------------------------------------------\n")


class AccumulatorCalculator:


    def __init__(self, initial_value: float = 0.0) -> None:
        self.acc: float = float(initial_value)
        self._operations: dict[str, Callable[[float, float], float]] = {
            "+": self._add,
            "-": self._sub,
            "*": self._mul,
            "/": self._div,
            "//": self._floordiv,
            "%": self._mod,
            "**": self._pow,
            "=": self._load,
        }

    @staticmethod
    def _add(acc: float, operand: float) -> float:
        return acc + operand

    @staticmethod
    def _sub(acc: float, operand: float) -> float:
        return acc - operand

    @staticmethod
    def _mul(acc: float, operand: float) -> float:
        return acc * operand

    @staticmethod
    def _div(acc: float, operand: float) -> float:
        if operand == 0:
            raise ZeroDivisionError("Ділення на нуль неможливе.")
        return acc / operand

    @staticmethod
    def _floordiv(acc: float, operand: float) -> float:
        if operand == 0:
            raise ZeroDivisionError("Цілочисельне ділення на нуль неможливе.")
        return acc // operand

    @staticmethod
    def _mod(acc: float, operand: float) -> float:
        if operand == 0:
            raise ZeroDivisionError("Остача від ділення на нуль неможлива.")
        return acc % operand

    @staticmethod
    def _pow(acc: float, operand: float) -> float:
        return acc**operand

    @staticmethod
    def _load(_acc: float, operand: float) -> float:
        return operand

    def exe(self, op: str, operand: float) -> bool:


        op = op.strip()
        func = self._operations.get(op)
        if func is None:
            supported = ", ".join(self._operations.keys())
            print(f"❌ Помилка: невідома операція '{op}'. Доступні: {supported}")
            return False

        try:
            prev = self.acc
            self.acc = func(self.acc, operand)
            print(f"✅ Операція '{op}' з операндом {operand}: {prev} -> Акумулятор = {self.acc}")
            return True
        except ZeroDivisionError as exc:
            print(f"❌ Математична помилка: {exc} Акумулятор залишився без змін ({self.acc}).")
            return False
        except OverflowError:
            print(f"❌ Помилка переповнення числа! Акумулятор залишився без змін ({self.acc}).")
            return False


def read_int(prompt: str) -> Optional[int]:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print(f"❌ Помилка вводу: '{raw}' не є коректним цілим числом.")
        return None


def read_float(prompt: str) -> Optional[float]:
    raw = input(prompt).strip().replace(",", ".")
    try:
        val = float(raw)
        if val != val or val in (float("inf"), float("-inf")):
            print("❌ Помилка вводу: число має бути скінченним.")
            return None
        return val
    except ValueError:
        print(f"❌ Помилка вводу: '{raw}' не є коректним числом.")
        return None


def main() -> None:
    print("=== Ініціалізація системи Employer ===")
    while True:
        cap = read_int("Введіть кількість робочих місць (наприклад, 3): ")
        if cap is None:
            continue
        if cap <= 0:
            print("❌ Помилка: кількість робочих місць має бути більше 0.")
            continue
        employer = Employer(capacity=cap)
        break

    calc = AccumulatorCalculator(initial_value=0.0)

    while True:
        print("\n=== ГОЛОВНЕ МЕНЮ ===")
        print("1. Найняти працівника (hire)")
        print("2. Звільнити робоче місце за індексом (fire)")
        print("3. Показати стан робочих місць")
        print("4. Виконати операцію акумуляторного калькулятора (exe)")
        print("5. Скинути акумулятор у 0")
        print("0. Вихід")

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            name = input("Введіть ім'я працівника: ")
            role = input("Введіть посаду: ")
            employer.hire(name=name, role=role)

        elif choice == "2":
            idx = read_int("Введіть індекс робочого місця для звільнення: ")
            if idx is not None:
                employer.fire(idx)

        elif choice == "3":
            employer.show_status()

        elif choice == "4":
            print(f"Поточне значення акумулятора: {calc.acc}")
            print("Операції: + , - , * , / , // , % , ** , = (записати в акумулятор)")
            op = input("Введіть символ операції: ")
            operand = read_float("Введіть число (операнд): ")
            if operand is not None:
                calc.exe(op=op, operand=operand)

        elif choice == "5":
            calc.acc = 0.0
            print("ℹ️ Акумулятор скинуто до 0.0.")

        elif choice == "0":
            print("Роботу завершено.")
            break

        else:
            print(f"❌ Помилка: невідомий пункт меню '{choice}'. Оберіть число від 0 до 5.")


if __name__ == "__main__":
    main()
