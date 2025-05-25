import os

from dotenv import load_dotenv
from openai import AzureOpenAI


load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("API_BASE"),
)

deployment = "gpt-4o"


def zbierz_kontekst_od_uzytkownika():
    """
    Interaktywnie zbiera kontekst projektu od użytkownika przez CLI
    """
    print("=== ZBIERANIE KONTEKSTU PROJEKTU ===")
    print("Odpowiedz na poniższe pytania, aby wygenerować dopasowane user stories:\n")

    typ_aplikacji = input(
        "1. Jaki typ aplikacji tworzysz? (np. e-commerce B2C, CRM B2B, aplikacja mobilna): "
    )

    uzytkownicy = input(
        "2. Kim są główni użytkownicy? (np. klienci kupujący online, administratorzy): "
    )

    cele_biznesowe = input(
        "3. Jakie są główne cele biznesowe? (np. zwiększenie konwersji, automatyzacja): "
    )

    obszary_funkcjonalne = input(
        "4. Jakie obszary funkcjonalne pokryć? (oddziel przecinkami): "
    )

    dodatkowe_wymagania = input("5. Dodatkowe wymagania/integracje (opcjonalne): ")

    kontekst = f"""
    **KONTEKST PROJEKTU:**

    **Typ aplikacji:** {typ_aplikacji}

    **Użytkownicy:** {uzytkownicy}

    **Cele biznesowe:** {cele_biznesowe}

    **Obszary funkcjonalne:** {obszary_funkcjonalne}

    **Dodatkowe wymagania:** {dodatkowe_wymagania if dodatkowe_wymagania else "Brak"}
    """

    return kontekst


def generuj_user_stories_z_kontekstem(kontekst_uzytkownika):
    prompt_generowanie = f"""
    Na podstawie poniższego kontekstu projektu, stwórz 3 niezależne historyjki użytkownika zgodne z kryteriami INVEST.

    **KONTEKST PROJEKTU:**
    {kontekst_uzytkownika}

    **ZADANIE:**
    Stwórz 3 user stories, które najlepiej odpowiadają na potrzeby opisane w kontekście.

    **Wymagania dla każdej historii:**
    - Format: "Jako..., chcę..., aby..."
    - Lista 5–8 kryteriów akceptacji (checklista w Markdown)
    - Punkty za historię (skala Fibonacciego: 1, 2, 3, 5, 8, 13)
    - Priorytet: Wysoki / Średni / Niski
    - Uwzględnij walidację danych i obsługę błędów
    - Możliwość testowania przez QA

    **Format wyjściowy:**
    Dla każdej historii:
    - **Tytuł**
    - **User story** (format „Jako… chcę… aby…")
    - **Kryteria akceptacji** (lista checkboxów)
    - **Punkty i priorytet**

    **Przypomnienie INVEST:**
    - Independent: Niezależna od innych
    - Negotiable: Negocjowalna
    - Valuable: Wartościowa dla użytkownika
    - Estimable: Możliwa do oszacowania
    - Small: Wystarczająco mała na 1 sprint (2 tyg.)
    - Testable: Posiada mierzalne kryteria akceptacji

    **WAŻNE:** 
    - Dostosuj historie do specyfiki projektu opisanej w kontekście
    - Skup się na najważniejszych funkcjonalnościach dla określonych użytkowników
    - Pamiętaj o celach biznesowych przy priorytetyzacji
    
    Pisząc, pamiętaj o zachowaniu przejrzystej struktury oraz realnej wartości biznesowej.
    """

    try:
        print("Generowanie user stories na podstawie kontekstu...")
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "Jesteś doświadczonym Product Ownerem i Scrum Masterem. Tworzysz wysokiej jakości historie użytkownika zgodne z najlepszymi praktykami Agile i Scrum, dopasowane do konkretnego kontekstu biznesowego. Odpowiadasz w języku polskim.",
                },
                {"role": "user", "content": prompt_generowanie},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Błąd podczas generowania user stories: {str(e)}")
        return None


def waliduj_historie_ai(content):
    prompt_walidacja = f"""
    Jesteś ekspertem od metodyki Agile i Scrum. Twoim zadaniem jest ocena jakości poniższych user stories pod kątem zgodności z kryteriami INVEST i najlepszymi praktykami.

    **Historie do oceny:**
    {content}

    **Kryteria oceny:**
    1. **INVEST sprawdzenie:**
       - Independent: Czy historie są niezależne od siebie?
       - Negotiable: Czy szczegóły można negocjować/doprecyzować?
       - Valuable: Czy każda historia dostarcza wartość użytkownikowi?
       - Estimable: Czy można oszacować wysiłek potrzebny do realizacji?
       - Small: Czy historie są na tyle małe, by zmieścić się w sprincie?
       - Testable: Czy każda historia ma jasne kryteria testowania?

    2. **Jakość kryteriów akceptacji:**
       - Czy są konkretne i mierzalne?
       - Czy pokrywają pozytywne i negatywne scenariusze?
       - Czy uwzględniają walidację i obsługę błędów?

    3. **Format i struktura:**
       - Czy format "Jako.../Chcę.../Aby..." jest poprawny?
       - Czy punkty za historie są realistyczne?
       - Czy priorytety są uzasadnione?

    4. **Kompletność:**
       - Czy wszystkie wymagane obszary funkcjonalne zostały pokryte?
       - Czy historie są zrozumiałe dla zespołu deweloperskiego?

    **Odpowiedź w formacie:**
    
    ## OCENA OGÓLNA
    [Oceń w skali 1-10 i uzasadnij]

    ## ANALIZA INVEST
    - Independent: [+/- oraz komentarz]
    - Negotiable: [+/- oraz komentarz]
    - Valuable: [+/- oraz komentarz] 
    - Estimable: [+/- oraz komentarz]
    - Small: [+/- oraz komentarz]
    - Testable: [+/- oraz komentarz]

    ## SZCZEGÓŁOWA ANALIZA KAŻDEJ HISTORII
    [Dla każdej historii: mocne strony, słabe strony, sugestie poprawek]

    ## REKOMENDACJE
    [Konkretne sugestie ulepszeń]

    ## PODSUMOWANIE
    [Czy historie są gotowe do realizacji? Co wymaga poprawy?]
    """

    try:
        response_walidacja = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "Jesteś doświadczonym ekspertem Agile/Scrum ze specjalizacją w ocenie jakości user stories. Twoja analiza jest precyzyjna, konstruktywna i skupiona na praktycznych aspektach realizacji. Odpowiadasz w języku polskim.",
                },
                {"role": "user", "content": prompt_walidacja},
            ],
            temperature=0.3,
        )

        return response_walidacja.choices[0].message.content

    except Exception as e:
        return f"Błąd podczas walidacji: {str(e)}"


def main():
    print("=== GENERATOR USER STORIES Z KONTEKSTEM ===\n")

    print("KROK 1: Zbieranie kontekstu projektu")
    print("-" * 40)

    # kontekst_uzytkownika = """
    # Kontekst Projektu
    # 1. Typ aplikacji: E-commerce B2C - sklep internetowy z odzieżą
    # 2. Użytkownicy: Klienci kupujący online (18-45 lat), administratorzy sklepu
    # 3. Cele biznesowe: Zwiększenie konwersji o 15%, poprawa UX, zmniejszenie porzucania koszyka
    # 4. Obszary funkcjonalne: Rejestracja/logowanie, wyszukiwanie produktów, koszyk zakupowy, płatności
    # 5. Dodatkowe wymagania: Integracja z PayPal i BLIK, responsywność mobilna
    # """

    kontekst_uzytkownika = zbierz_kontekst_od_uzytkownika()
    if not kontekst_uzytkownika:
        print("Błąd podczas zbierania kontekstu. Przerywam wykonanie.")
        return

    print("\nZebrany kontekst:")
    print(kontekst_uzytkownika)
    print("\n" + "=" * 50)

    print("KROK 2: Generowanie user stories")
    print("-" * 40)

    wygenerowane_stories = generuj_user_stories_z_kontekstem(kontekst_uzytkownika)
    if not wygenerowane_stories:
        print("Błąd podczas generowania user stories. Przerywam wykonanie.")
        return

    print("=== WYGENEROWANE HISTORIE UŻYTKOWNIKA ===")
    print(wygenerowane_stories)

    print("\n" + "=" * 50)
    print("KROK 3: Walidacja AI")
    print("-" * 40)
    print("Trwa analiza przez AI eksperta...")

    walidacja_ai = waliduj_historie_ai(wygenerowane_stories)
    print(walidacja_ai)
    print("Wygenerowano walidację AI")

    full_content = f"""# Sprint 1 - User Stories

    ## Kontekst Projektu
    {kontekst_uzytkownika}

    ## Wygenerowane User Stories
    {wygenerowane_stories}

    ---

    ## Walidacja AI
    {walidacja_ai}
    """

    save_path = "backlog/sprint1.md"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Historie zapisane")


if __name__ == "__main__":
    main()
