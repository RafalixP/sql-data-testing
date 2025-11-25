from src.data_quality_validator import DataQualityValidator

# Stwórz instancję
validator = DataQualityValidator("data/test_database.db")
validator.connect()

# Teraz wpisz tę linię i zobacz co się stanie:
result = validator.check_duplicates()

# Po wpisaniu "result." IDE powinno pokazać podpowiedzi dla listy:
# result.append(), result.count(), result.index(), len(result), etc.

# Sprawdź też:
summary = validator.get_data_quality_summary()
# Po wpisaniu "summary." IDE powinno pokazać metody słownika:
# summary.keys(), summary.values(), summary.get(), etc.

validator.disconnect()