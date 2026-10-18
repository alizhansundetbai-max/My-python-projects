import json
import random
import os

DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"cards": [], "notes": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def manage_cards(data):
    while True:
        print("\n--- ФЛЕШ-КАРТОЧКИ ---")
        print("1. Добавить карточку")
        print("2. Просмотреть все карточки")
        print("3. Учить карточки (интерактив)")
        print("0. Назад в меню")
        choice = input("Выберите действие: ")

        if choice == "1":
            term = input("Введите термин/вопрос: ").strip()
            definition = input("Введите определение/ответ: ").strip()
            if term and definition:
                data["cards"].append({"term": term, "def": definition})
                save_data(data)
                print("Карточка добавлена!")
        elif choice == "2":
            if not data["cards"]:
                print("Список карточек пуст.")
            else:
                for i, card in enumerate(data["cards"], 1):
                    print(f"{i}. {card['term']} — {card['def']}")
        elif choice == "3":
            if not data["cards"]:
                print("Сначала добавьте карточки!")
                continue
            for card in data["cards"]:
                print(f"\nВопрос: {card['term']}")
                input("Нажмите Enter, чтобы увидеть ответ...")
                print(f"Ответ: {card['def']}")
        elif choice == "0":
            break

def run_quiz(data):
    cards = data["cards"]
    if len(cards) < 2:
        print("\nДля викторины нужно минимум 2 карточки!")
        return

    print("\n--- ВИКТОРИНА ---")
    score = 0
    questions = random.sample(cards, len(cards))

    for card in questions:
        print(f"\nЧто означает: '{card['term']}'?")
        
        wrong_answers = [c["def"] for c in cards if c["def"] != card["def"]]
        options = random.sample(wrong_answers, min(len(wrong_answers), 3)) + [card["def"]]
        random.shuffle(options)

        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")

        try:
            ans_idx = int(input("Ваш ответ (номер): ")) - 1
            if options[ans_idx] == card["def"]:
                print("Верно! 🎉")
                score += 1
            else:
                print(f"Неверно. Правильный ответ: {card['def']}")
        except (ValueError, IndexError):
            print("Некорректный ввод, вопрос пропущен.")

    print(f"\nВикторина завершена! Ваш результат: {score}/{len(questions)}")

def manage_notes(data):
    while True:
        print("\n--- ЗАМЕТКИ ---")
        print("1. Добавить заметку")
        print("2. Посмотреть заметки")
        print("0. Назад в меню")
        choice = input("Выберите действие: ")

        if choice == "1":
            text = input("Введите текст заметки: ").strip()
            if text:
                data["notes"].append(text)
                save_data(data)
                print("Заметка сохранена!")
        elif choice == "2":
            if not data["notes"]:
                print("Заметок пока нет.")
            else:
                for i, note in enumerate(data["notes"], 1):
                    print(f"{i}. {note}")
        elif choice == "0":
            break

def main():
    data = load_data()
    while True:
        print("\n=== ГЛАВНОЕ МЕНЮ ===")
        print("1. Карточки")
        print("2. Викторина")
        print("3. Заметки")
        print("0. Выход")
        choice = input("Выберите раздел: ")

        if choice == "1":
            manage_cards(data)
        elif choice == "2":
            run_quiz(data)
        elif choice == "3":
            manage_notes(data)
        elif choice == "0":
            print("До свидания!")
            break

if __name__ == "__main__":
    main()