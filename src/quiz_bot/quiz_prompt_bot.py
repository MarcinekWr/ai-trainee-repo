import hashlib
import os
import random
import re

from dotenv import load_dotenv
from openai import AzureOpenAI


load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("API_BASE"),
)

deployment = "gpt-4o"

rewards = {"łatwy": 100, "średni": 500, "trudny": 1000}

asked_questions = set()


chat_history = [
    {
        "role": "system",
        "content": (
            "Jesteś kreatywnym botem quizowym. Generuj unikalne, ciekawe i wymagające pytania wielokrotnego wyboru w języku polskim. "
            "Nigdy nie powtarzaj pytania, które już pojawiło się w tej historii czatu. Każde pytanie powinno mieć cztery odpowiedzi (A–D) "
            "i kończyć się wskazaniem poprawnej odpowiedzi w formacie: Odpowiedź: X"
        ),
    }
]


def get_question_hash(question_text: str):
    words = re.findall(r"\b\w+\b", question_text.lower())
    key_words = " ".join(words[:8]) if len(words) >= 8 else " ".join(words)
    return hashlib.md5(key_words.encode()).hexdigest()


def generate_question(difficulty: str, attempt: int = 1):
    topics = [
        "historia",
        "geografia",
        "nauka",
        "sport",
        "literatura",
        "sztuka",
        "muzyka",
        "filmy",
        "natura",
        "technologia",
        "astronomia",
        "medycyna",
        "kultura",
        "polityka",
        "ekonomia",
    ]

    topic = random.choice(topics)

    prompt = (
        f"Wygeneruj 1 pytanie wiedzy ogólnej w języku polskim na poziomie {difficulty} na temat {topic}. "
        f"To jest próba #{attempt}. Pytanie powinno być unikalne i interesujące. Unikaj pytań, które już padły. "
        "Powinno mieć 4 możliwe odpowiedzi (A do D), z jedną poprawną i trzema błędnymi. "
        "Na końcu wskaż poprawną odpowiedź w formacie: Odpowiedź: X"
    )

    chat_history.append({"role": "user", "content": prompt})

    # with open("prompts/best.txt", "w", encoding="utf-8") as f:
    #     f.write(prompt)

    response = client.chat.completions.create(
        model=deployment, messages=chat_history, temperature=0.9, max_tokens=500
    )

    content = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": content})

    match = re.search(r"Odpowiedź:\s*([A-D])", content)
    if not match:
        raise ValueError("Błąd w szukaniu odpowiedzi w wygenerowanym promptcie.")

    answer = match.group(1)
    question_text = re.sub(r"Odpowiedź:\s*[A-D]", "", content).strip()
    return question_text, answer


def get_unique_question(difficulty: str):
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            question, answer = generate_question(difficulty, attempt)
            question_hash = get_question_hash(question)
            if question_hash not in asked_questions:
                asked_questions.add(question_hash)
                print(asked_questions)
                return question, answer
            else:
                print(
                    f"Pytanie podobne do wcześniejszego, próba {attempt}/{max_attempts}..."
                )
        except Exception as e:
            print(f"Błąd w próbie {attempt}: {e}")
    print("Czyszczę historię pytań i próbuję ponownie...")
    asked_questions.clear()
    reset_chat_history()
    return generate_question(difficulty, 1)


def reset_chat_history():
    chat_history.clear()
    chat_history.append(
        {
            "role": "system",
            "content": (
                "Jesteś kreatywnym botem quizowym. Generuj unikalne, ciekawe i wymagające pytania wielokrotnego wyboru w języku polskim. "
                "Nigdy nie powtarzaj pytania, które już pojawiło się w tej historii czatu. Każde pytanie powinno mieć cztery odpowiedzi (A–D) "
                "i kończyć się wskazaniem poprawnej odpowiedzi w formacie: Odpowiedź: X"
            ),
        }
    )


def main():
    print("🎉 Witaj w MarcinoQuizjom! 🎉")

    total = 0
    question_number = 1

    while True:
        print(
            "\nWybierz poziom trudności (łatwy / średni / trudny), 'Q' aby zakończyć."
        )
        choice = input("Twój wybór: ").strip().lower()

        if choice == "q":
            print(f"\nKoniec gry! Zdobyłeś: {total} zł. Dzięki za grę!")
            break

        if choice not in rewards:
            print("Nieprawidłowy poziom trudności.")
            continue

        try:
            print(f"\nGeneruję unikalne pytanie ({choice})...")
            question, correct = get_unique_question(choice)
        except Exception as e:
            print(f"Błąd generowania pytania: {e}")
            continue

        print(f"\nPytanie {question_number} ({choice}):\n")
        print(question)
        answer = input("Twoja odpowiedź (A/B/C/D): ").strip().upper()

        if answer == correct:
            earned = rewards[choice]
            total += earned
            print(f"Poprawnie :D! Zdobywasz {earned} zł. Łącznie: {total} zł.")
        else:
            print(
                f"Zła odpowiedź. Poprawna to: {correct}. Przegrałeś kwote: {total} zł."
            )
            print(f"\nKoniec gry! :C Dzięki za grę!")
            break

        question_number += 1


if __name__ == "__main__":
    main()
