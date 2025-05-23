# Sprint 1 - User Stories

## Kontekst Projektu

    Kontekst Projektu
    1. Typ aplikacji: E-commerce B2C - sklep internetowy z odzieżą
    2. Użytkownicy: Klienci kupujący online (18-45 lat), administratorzy sklepu
    3. Cele biznesowe: Zwiększenie konwersji o 15%, poprawa UX, zmniejszenie porzucania koszyka
    4. Obszary funkcjonalne: Rejestracja/logowanie, wyszukiwanie produktów, koszyk zakupowy, płatności
    5. Dodatkowe wymagania: Integracja z PayPal i BLIK, responsywność mobilna
    

## Wygenerowane User Stories
### Historia 1: Rejestracja i logowanie z opcją "Zapamiętaj mnie"

**Tytuł:** Rejestracja i logowanie użytkownika z opcją "Zapamiętaj mnie"

**User story:**  
Jako klient sklepu, chcę mieć możliwość rejestracji i logowania z opcją "Zapamiętaj mnie", aby szybciej uzyskać dostęp do swojego konta bez konieczności każdorazowego wpisywania danych.

**Kryteria akceptacji:**  
- [ ] Użytkownik ma możliwość rejestracji z podaniem imienia, nazwiska, adresu e-mail, hasła oraz opcjonalnie numeru telefonu.  
- [ ] Formularz rejestracji waliduje dane (np. poprawność adresu e-mail, minimalna długość hasła: 8 znaków).  
- [ ] Użytkownik może zalogować się, wprowadzając adres e-mail i hasło.  
- [ ] Podczas logowania dostępna jest opcja "Zapamiętaj mnie", która zapisuje sesję użytkownika na urządzeniu przez 30 dni.  
- [ ] W przypadku błędnych danych logowania wyświetlany jest komunikat "Nieprawidłowy e-mail lub hasło".  
- [ ] Użytkownik może zresetować hasło za pomocą linku wysyłanego na podany adres e-mail.  
- [ ] Aplikacja działa responsywnie na urządzeniach mobilnych i desktopowych.  
- [ ] QA może przetestować funkcję rejestracji, logowania i "Zapamiętaj mnie" poprzez symulację poprawnych i błędnych danych oraz różne rozmiary ekranów.

**Punkty:** 5  
**Priorytet:** Wysoki  

---

### Historia 2: Wyszukiwanie produktów z filtrowaniem

**Tytuł:** Funkcjonalność wyszukiwania produktów z możliwością filtrowania

**User story:**  
Jako klient sklepu, chcę wyszukiwać produkty według nazwy, kategorii, ceny i dostępności, aby szybko znaleźć odzież spełniającą moje wymagania.

**Kryteria akceptacji:**  
- [ ] Użytkownik ma możliwość wpisania nazwy produktu w pole wyszukiwania (autouzupełnianie działa dla najbardziej popularnych produktów).  
- [ ] Wyniki wyszukiwania wyświetlają się w czasie rzeczywistym, bez konieczności odświeżania strony.  
- [ ] Użytkownik może filtrować wyniki według kategorii (np. "Męskie", "Damskie"), zakresu cenowego i dostępności w magazynie.  
- [ ] W przypadku braku wyników wyświetlany jest komunikat: "Brak produktów spełniających kryteria wyszukiwania".  
- [ ] Funkcja wyszukiwania działa poprawnie na urządzeniach mobilnych i desktopowych.  
- [ ] QA może przetestować wyszukiwanie z różnymi kombinacjami filtrów, w tym skrajne wartości (np. brak wyników, maksymalne ceny).  
- [ ] Wszystkie elementy interfejsu są zgodne z zasadami UX (przejrzystość, intuicyjność).  

**Punkty:** 8  
**Priorytet:** Wysoki  

---

### Historia 3: Integracja płatności z PayPal i BLIK

**Tytuł:** Integracja płatności z PayPal i BLIK

**User story:**  
Jako klient sklepu, chcę mieć możliwość dokonania płatności za zakupy za pomocą PayPal i BLIK, aby wybrać najbardziej wygodną dla mnie metodę płatności.

**Kryteria akceptacji:**  
- [ ] Użytkownik ma możliwość wyboru metody płatności podczas składania zamówienia (PayPal, BLIK, karta płatnicza).  
- [ ] System poprawnie przekierowuje użytkownika na stronę PayPal w przypadku wyboru tej metody płatności.  
- [ ] W przypadku BLIK użytkownik wprowadza kod BLIK, który jest walidowany w czasie rzeczywistym.  
- [ ] W przypadku nieudanej płatności wyświetlany jest komunikat: "Nie udało się zrealizować płatności. Spróbuj ponownie lub wybierz inną metodę".  
- [ ] Po pomyślnym zakończeniu płatności użytkownik otrzymuje e-mail z potwierdzeniem zamówienia.  
- [ ] QA może przetestować poprawność działania płatności na urządzeniach mobilnych i desktopowych, w tym symulację błędnych danych.  
- [ ] Aplikacja obsługuje sytuacje wyjątkowe (np. brak połączenia z bramką płatności).  
- [ ] Wszystkie metody płatności są zgodne z zasadami bezpieczeństwa (np. szyfrowanie danych).  

**Punkty:** 8  
**Priorytet:** Wysoki  

---

## Walidacja AI
## OCENA OGÓLNA  
**Ocena: 8/10**  
Historie są dobrze sformułowane i spełniają większość kryteriów INVEST oraz najlepszych praktyk Agile/Scrum. Mają jasne kryteria akceptacji, są wartościowe dla użytkownika i zrozumiałe dla zespołu. Jednak można wprowadzić pewne poprawki, aby zwiększyć ich niezależność oraz doprecyzować niektóre aspekty kryteriów akceptacji.

---

## ANALIZA INVEST  

### Independent  
- **Historia 1:** +/-  
  Historia rejestracji i logowania jest częściowo zależna od innych funkcji aplikacji, takich jak zarządzanie kontem użytkownika. Można ją jednak realizować niezależnie w większości przypadków.  
- **Historia 2:** +  
  Wyszukiwanie produktów jest w pełni niezależne od innych funkcji aplikacji.  
- **Historia 3:** +/-  
  Integracja płatności zależy od funkcji składania zamówienia, co czyni ją częściowo zależną.  

### Negotiable  
- **Historia 1:** +  
  Szczegóły, takie jak długość sesji "Zapamiętaj mnie" czy walidacja danych, można negocjować.  
- **Historia 2:** +  
  Można doprecyzować zakres filtrów i sposób działania autouzupełniania.  
- **Historia 3:** +  
  Szczegóły dotyczące obsługi błędów i metod płatności są otwarte na negocjacje.  

### Valuable  
- **Historia 1:** +  
  Dostarcza wartość użytkownikowi, ułatwiając dostęp do konta.  
- **Historia 2:** +  
  Wyszukiwanie i filtrowanie produktów znacząco poprawia doświadczenie użytkownika.  
- **Historia 3:** +  
  Integracja różnych metod płatności zwiększa wygodę użytkownika.  

### Estimable  
- **Historia 1:** +  
  Wysiłek jest łatwy do oszacowania, ponieważ funkcjonalność jest dobrze zdefiniowana.  
- **Historia 2:** +  
  Historia jest szczegółowa, co pozwala na precyzyjne oszacowanie.  
- **Historia 3:** +  
  Integracja płatności jest jasno opisana, co ułatwia oszacowanie.  

### Small  
- **Historia 1:** +/-  
  Historia może być zbyt duża, jeśli uwzględnimy wszystkie kryteria akceptacji w jednym sprincie. Można ją podzielić na mniejsze części, np. osobno rejestracja i logowanie.  
- **Historia 2:** +  
  Historia jest odpowiednio mała i możliwa do realizacji w jednym sprincie.  
- **Historia 3:** +/-  
  Historia może być zbyt duża, jeśli uwzględnimy wszystkie metody płatności i obsługę błędów w jednym sprincie. Można ją podzielić na integrację PayPal i BLIK jako osobne zadania.  

### Testable  
- **Historia 1:** +  
  Kryteria akceptacji są jasne i obejmują zarówno pozytywne, jak i negatywne scenariusze.  
- **Historia 2:** +  
  Kryteria akceptacji są dobrze zdefiniowane i uwzględniają różne kombinacje filtrów.  
- **Historia 3:** +  
  Kryteria akceptacji są konkretne i obejmują testowanie błędów oraz sytuacji wyjątkowych.  

---

## SZCZEGÓŁOWA ANALIZA KAŻDEJ HISTORII  

### Historia 1: Rejestracja i logowanie z opcją "Zapamiętaj mnie"  
**Mocne strony:**  
- Jasna wartość dla użytkownika (szybszy dostęp do konta).  
- Kryteria akceptacji są szczegółowe i obejmują zarówno pozytywne, jak i negatywne scenariusze.  
- Uwzględniono responsywność aplikacji.  

**Słabe strony:**  
- Historia może być zbyt obszerna, ponieważ obejmuje zarówno rejestrację, logowanie, jak i opcję "Zapamiętaj mnie".  
- Nie uwzględniono szczegółów dotyczących bezpieczeństwa (np. szyfrowanie danych logowania).  

**Sugestie poprawek:**  
- Podziel historię na mniejsze części: rejestracja, logowanie i opcja "Zapamiętaj mnie".  
- Doprecyzuj wymagania dotyczące bezpieczeństwa danych użytkownika.  

---

### Historia 2: Wyszukiwanie produktów z filtrowaniem  
**Mocne strony:**  
- Historia jest niezależna i dobrze zdefiniowana.  
- Kryteria akceptacji są konkretne, mierzalne i uwzględniają różne scenariusze (np. brak wyników).  
- Uwzględniono zasady UX oraz responsywność aplikacji.  

**Słabe strony:**  
- Brakuje szczegółów dotyczących wydajności (np. maksymalna liczba wyników wyszukiwania).  

**Sugestie poprawek:**  
- Dodaj wymagania dotyczące wydajności, np. ograniczenie liczby wyników na stronie.  
- Doprecyzuj sposób działania autouzupełniania (np. czy działa dla wszystkich produktów czy tylko popularnych).  

---

### Historia 3: Integracja płatności z PayPal i BLIK  
**Mocne strony:**  
- Historia dostarcza dużą wartość użytkownikowi, umożliwiając wybór wygodnej metody płatności.  
- Kryteria akceptacji są szczegółowe i uwzględniają obsługę błędów oraz sytuacji wyjątkowych.  
- Uwzględniono wymagania dotyczące bezpieczeństwa.  

**Słabe strony:**  
- Historia może być zbyt obszerna, jeśli uwzględnimy wszystkie metody płatności w jednym sprincie.  
- Brakuje szczegółów dotyczących integracji z bramkami płatności (np. wymagania techniczne).  

**Sugestie poprawek:**  
- Podziel historię na mniejsze części: osobno integracja PayPal i BLIK.  
- Doprecyzuj wymagania techniczne dotyczące integracji z bramkami płatności.  

---

## REKOMENDACJE  
1. Podziel większe historie (Historia 1 i Historia 3) na mniejsze, bardziej niezależne zadania.  
2. Doprecyzuj wymagania dotyczące bezpieczeństwa (Historia 1 i Historia 3).  
3. Dodaj wymagania dotyczące wydajności i szczegóły działania autouzupełniania (Historia 2).  
4. Upewnij się, że wszystkie historie są możliwe do realizacji w jednym sprincie.  

---

## PODSUMOWANIE  
Historie są dobrze przygotowane i mogą być realizowane, jednak wymagają drobnych poprawek, aby zwiększyć ich niezależność, doprecyzować szczegóły oraz podzielić większe zadania na mniejsze. Po wprowadzeniu tych zmian historie będą w pełni zgodne z kryteriami INVEST i gotowe do realizacji.
