import csv
import os


REQUIRED = ["student", "group", "score"]


def read_students(path):
    if not os.path.isfile(path):
        raise ValueError(f"Файл не найден: {path}")

    students = []

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("Нет обязательных столбцов: " + ", ".join(missing))

        for number, row in enumerate(reader, start=2):
            student = (row["student"] or "").strip()
            group = (row["group"] or "").strip()
            text = (row["score"] or "").strip()

            if not student or not group or not text:
                raise ValueError(f"Строка {number}: пустое поле")

            try:
                score = int(text)
            except ValueError:
                raise ValueError(f"Строка {number}: некорректный балл '{text}'")

            if score < 0 or score > 100:
                raise ValueError(f"Строка {number}: балл {score} вне диапазона 0-100")

            students.append({"student": student, "group": group, "score": score})

    return students