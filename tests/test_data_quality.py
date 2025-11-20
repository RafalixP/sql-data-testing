import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_quality_tester import DataQualityTester

@pytest.fixture
def tester():
    """Fixture do inicjalizacji testera"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_database.db')
    tester = DataQualityTester(db_path)
    tester.connect()
    yield tester
    tester.disconnect()

class TestDataQuality:
    
    def test_no_duplicates(self, tester):
        """Test sprawdza czy nie ma duplikatów"""
        duplicates = tester.check_duplicates()
        assert len(duplicates) == 0, f"Znaleziono {len(duplicates)} duplikatów: {duplicates}"
    
    def test_no_nulls_in_employees(self, tester):
        """Test sprawdza czy nie ma NULL wartości w krytycznych kolumnach"""
        nulls = tester.check_nulls_employees()
        assert len(nulls) == 0, f"Znaleziono {len(nulls)} rekordów z NULL: {nulls}"
    
    def test_no_foreign_key_violations(self, tester):
        """Test sprawdza czy nie ma naruszeń kluczy obcych"""
        violations = tester.check_foreign_key_violations()
        assert len(violations) == 0, f"Znaleziono {len(violations)} naruszeń FK: {violations}"
    
    def test_salary_within_budget(self, tester):
        """Test sprawdza czy pensje nie przekraczają budżetu działu"""
        violations = tester.check_salary_budget_violations()
        assert len(violations) == 0, f"Znaleziono {len(violations)} przekroczeń budżetu: {violations}"
    
    def test_reasonable_salaries(self, tester):
        """Test sprawdza czy pensje są w rozsądnym zakresie"""
        unreasonable = tester.check_unreasonable_salaries()
        assert len(unreasonable) == 0, f"Znaleziono {len(unreasonable)} nierozsądnych pensji: {unreasonable}"
    
    def test_no_future_hire_dates(self, tester):
        """Test sprawdza czy nie ma dat zatrudnienia z przyszłości"""
        future_dates = tester.check_future_hire_dates()
        assert len(future_dates) == 0, f"Znaleziono {len(future_dates)} dat z przyszłości: {future_dates}"
    
    def test_data_quality_summary(self, tester):
        """Test generuje raport z wszystkimi problemami"""
        summary = tester.get_data_quality_summary()
        total_issues = sum(summary.values())
        
        print(f"\n=== RAPORT JAKOŚCI DANYCH ===")
        for check, count in summary.items():
            print(f"{check}: {count} problemów")
        print(f"TOTAL: {total_issues} problemów")
        
        # Ten test zawsze przechodzi - służy tylko do raportowania
        assert True