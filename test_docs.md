# Testowanie API Schroniska dla Psów

## Wymagania wstępne

- Python 3.8+
- Baza danych PostgreSQL
- Skonfigurowana aplikacja Flask

## Konfiguracja

1. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

2. Zainstaluj przeglądarki Playwright:
```bash
playwright install
```

3. Skonfiguruj zmienne środowiskowe:
- Utwórz plik `.env` w głównym katalogu projektu
- Dodaj dane logowania do bazy danych:
```
haslo=twoje_haslo_do_bazy_danych
```

## Uruchamianie Testów

### Testy Pytest
Aby uruchomić testy jednostkowe:
```bash
pytest test_app.py
```

### Testy E2E Playwright
Aby uruchomić testy end-to-end:
```bash
pytest playwright_tests.py
```

## Pokrycie Testów

### Testy Jednostkowe (pytest)
- Obsługa połączeń z bazą danych
- Funkcjonalność tras (routingu)
- Metody manipulacji danymi
- Obsługa błędów

### Testy E2E (Playwright)
- Walidacja punktów końcowych API
- Dodawanie i pobieranie danych
- Testowanie podstawowych przepływów

## Rozwiązywanie Problemów
- Upewnij się, że serwer Flask jest uruchomiony przed testami E2E
- Sprawdź ustawienia połączenia z bazą danych
- Zweryfikuj, czy zmienne środowiskowe są poprawnie ustawione

## Dodatkowe Informacje
- Testy mają na celu sprawdzenie poprawności działania API schroniska
- Każdy test jest izolowany i nie wpływa na dane produkcyjne
- W razie problemów sprawdź logi i konfigurację środowiska
