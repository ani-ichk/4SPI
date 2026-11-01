import argparse
import json
import sys

from rich.console import Console
from rich.table import Table

from grade_report.reader import read_students
from grade_report.statistics import calculate


def main():
    parser = argparse.ArgumentParser(description="Анализатор успеваемости")
    parser.add_argument("csv_path", help="путь к CSV-файлу")
    parser.add_argument("--output", required=True, help="путь к JSON-файлу")
    args = parser.parse_args()

    try:
        students = read_students(args.csv_path)
    except ValueError as error:
        print(f"Ошибка: {error}")
        sys.exit(1)

    if not students:
        print("Нет данных для анализа")
        return

    result = calculate(students)

    table = Table(title="Анализатор успеваемости")
    table.add_column("Показатель")
    table.add_column("Значение", justify="right")
    table.add_row("Число студентов", str(result["count"]))
    table.add_row("Средний балл", f"{result['average']:.2f}")
    table.add_row("Минимальный балл", str(result["min"]))
    table.add_row("Максимальный балл", str(result["max"]))
    for group, avg in result["groups"].items():
        table.add_row(f"Средний балл группы {group}", f"{avg:.2f}")
    Console().print(table)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)