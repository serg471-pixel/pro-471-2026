import json
import os
from datetime import datetime

FILE_NAME = "finance_data.json"


def load_data():
    if not os.path.exists(FILE_NAME):
        return {"budget": 0, "expenses": []}

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)



def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



def show_help():
    print("\nДоступні команди:")
    print("допомога – показати список команд")
    print("встановити бюджет – задати бюджет")
    print("додати витрату – додати нову витрату")
    print("показати витрати – список усіх витрат")
    print("витрати за дату – показати витрати за конкретну дату")
    print("витрати за період – витрати між двома датами")
    print("витрати за категорією – витрати певної категорії")
    print("залишок – показати залишок бюджету")
    print("звіт за категоріями – підсумок витрат по категоріях")
    print("вийти – завершити програму\n")



def set_budget(data):
    amount = float(input("Введіть суму бюджету: "))
    data["budget"] = amount
    save_data(data)
    print("Бюджет встановлено.")



def add_expense(data):
    amount = float(input("Сума: "))
    category = input("Категорія: ")
    date = input("Дата (YYYY-MM-DD): ")
    comment = input("Коментар (необов'язково): ")

    expense = {
        "amount": amount,
        "category": category,
        "date": date,
        "comment": comment
    }

    data["expenses"].append(expense)
    save_data(data)

    print("Витрату додано.")

    check_budget(data)



def show_expenses(data):
    if not data["expenses"]:
        print("Витрат немає.")
        return

    for e in data["expenses"]:
        print(f"{e['date']} | {e['category']} | {e['amount']} грн | {e['comment']}")



def expenses_by_date(data):
    date = input("Введіть дату (YYYY-MM-DD): ")

    for e in data["expenses"]:
        if e["date"] == date:
            print(f"{e['category']} | {e['amount']} грн | {e['comment']}")



def expenses_by_period(data):
    start = input("Початкова дата (YYYY-MM-DD): ")
    end = input("Кінцева дата (YYYY-MM-DD): ")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    for e in data["expenses"]:
        exp_date = datetime.strptime(e["date"], "%Y-%m-%d")

        if start_date <= exp_date <= end_date:
            print(f"{e['date']} | {e['category']} | {e['amount']} грн")



def expenses_by_category(data):
    category = input("Введіть категорію: ")

    for e in data["expenses"]:
        if e["category"].lower() == category.lower():
            print(f"{e['date']} | {e['amount']} грн | {e['comment']}")



def show_balance(data):
    total = sum(e["amount"] for e in data["expenses"])
    balance = data["budget"] - total

    print(f"Витрачено: {total} грн")
    print(f"Залишок бюджету: {balance} грн")



def check_budget(data):
    total = sum(e["amount"] for e in data["expenses"])

    if total > data["budget"]:
        print("УВАГА! Ви перевищили бюджет!")



def report_by_category(data):
    report = {}

    for e in data["expenses"]:
        category = e["category"]
        report[category] = report.get(category, 0) + e["amount"]

    for cat, amount in report.items():
        print(f"{cat}: {amount} грн")



def main():
    data = load_data()

    print("Вітаю! Це фінансовий трекер студента.")

    while True:
        command = input("\nВведіть команду: ").lower()

        if command == "допомога":
            show_help()

        elif command == "встановити бюджет":
            set_budget(data)

        elif command == "додати витрату":
            add_expense(data)

        elif command == "показати витрати":
            show_expenses(data)

        elif command == "витрати за дату":
            expenses_by_date(data)

        elif command == "витрати за період":
            expenses_by_period(data)

        elif command == "витрати за категорією":
            expenses_by_category(data)

        elif command == "залишок":
            show_balance(data)

        elif command == "звіт за категоріями":
            report_by_category(data)

        elif command == "вийти":
            print("До побачення!")
            break

        else:
            print("Невідома команда. Введіть 'допомога'.")


main()