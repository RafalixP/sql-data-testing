# SQL Data Testing

Projekt do nauki testowania jakości danych przy użyciu SQL - uzupełnienie portfolio Data QA.

## 🎯 Cel projektu

- SQL dla testowania danych (data reconciliation)
- Wykrywanie duplikatów i nulli
- Porównywanie tabel (staging vs target)
- Automatyzacja testów SQL z pytest
- CI/CD pipeline dla testów danych

## 📁 Struktura projektu

```
sql-data-testing/
├── data/                    # SQLite bazy + przykładowe CSV
├── sql_queries/            # Zapytania testowe SQL
├── src/                    # Python klasy do testów
├── tests/                  # pytest testy
├── .github/workflows/      # CI/CD pipeline
├── reports/               # Raporty HTML
└── README.md
```

## 🚀 Instalacja

```bash
pip install -r requirements.txt
```

## 🧪 Uruchomienie testów

```bash
pytest tests/ -v --html=reports/test_report.html
```

## 📊 Funkcjonalności

- ✅ Data reconciliation między tabelami
- ✅ Wykrywanie duplikatów w SQL
- ✅ Sprawdzanie nulli i typów danych
- ✅ Testy spójności sum i agregacji
- ✅ Automatyczne raporty HTML

## 👤 Autor

Rafał Pieczka - Data QA Engineer