import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_quality_validator import DataQualityValidator

@pytest.fixture
def validator():
    """Fixture do inicjalizacji validatora"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_database.db')
    validator = DataQualityValidator(db_path)
    validator.connect()
    yield validator
    validator.disconnect()

class TestDataQualityMonitoring:
    
    def test_monitor_duplicates(self, validator):
        """Monitoruje duplikaty - zawsze przechodzi, tylko raportuje"""
        duplicates = validator.check_duplicates()
        
        if len(duplicates) > 0:
            print(f"\n⚠️  WARNING: Znaleziono {len(duplicates)} duplikatów:")
            for dup in duplicates:
                print(f"   - {dup[0]} {dup[1]} ({dup[2]} razy)")
        else:
            print(f"\n✅ OK: Brak duplikatów")
            
        # Zawsze przechodzi - tylko monitoruje
        assert True
    
    def test_monitor_nulls(self, validator):
        """Monitoruje NULL wartości - zawsze przechodzi, tylko raportuje"""
        nulls = validator.check_nulls_employees()
        
        if len(nulls) > 0:
            print(f"\n⚠️  WARNING: Znaleziono {len(nulls)} rekordów z NULL:")
            for null_record in nulls:
                print(f"   - ID {null_record[0]}: {null_record[1]} {null_record[2]}")
        else:
            print(f"\n✅ OK: Brak NULL wartości")
            
        assert True
    
    def test_monitor_foreign_keys(self, validator):
        """Monitoruje naruszenia kluczy obcych - zawsze przechodzi, tylko raportuje"""
        violations = validator.check_foreign_key_violations()
        
        if len(violations) > 0:
            print(f"\n🚨 CRITICAL: Znaleziono {len(violations)} naruszeń FK:")
            for violation in violations:
                print(f"   - {violation[1]} {violation[2]} ma nieistniejący dept_id={violation[4]}")
        else:
            print(f"\n✅ OK: Wszystkie klucze obce są poprawne")
            
        assert True
    
    def test_monitor_budget_violations(self, validator):
        """Monitoruje przekroczenia budżetu - zawsze przechodzi, tylko raportuje"""
        violations = validator.check_salary_budget_violations()
        
        if len(violations) > 0:
            print(f"\n💰 WARNING: Znaleziono {len(violations)} przekroczeń budżetu:")
            for violation in violations:
                print(f"   - {violation[0]}: budżet {violation[1]}, suma pensji {violation[2]}")
        else:
            print(f"\n✅ OK: Wszystkie działy mieszczą się w budżecie")
            
        assert True
    
    def test_monitor_salary_ranges(self, validator):
        """Monitoruje nierozsądne pensje - zawsze przechodzi, tylko raportuje"""
        unreasonable = validator.check_unreasonable_salaries()
        
        if len(unreasonable) > 0:
            print(f"\n💸 WARNING: Znaleziono {len(unreasonable)} podejrzanych pensji:")
            for salary_issue in unreasonable:
                print(f"   - {salary_issue[0]} {salary_issue[1]}: {salary_issue[2]} PLN")
        else:
            print(f"\n✅ OK: Wszystkie pensje w rozsądnym zakresie")
            
        assert True
    
    def test_monitor_future_dates(self, validator):
        """Monitoruje daty z przyszłości - zawsze przechodzi, tylko raportuje"""
        future_dates = validator.check_future_hire_dates()
        
        if len(future_dates) > 0:
            print(f"\n📅 WARNING: Znaleziono {len(future_dates)} dat z przyszłości:")
            for future_date in future_dates:
                print(f"   - {future_date[0]} {future_date[1]}: {future_date[2]}")
        else:
            print(f"\n✅ OK: Wszystkie daty zatrudnienia są prawidłowe")
            
        assert True
    
    def test_data_quality_dashboard(self, validator):
        """Generuje kompletny dashboard jakości danych"""
        summary = validator.get_data_quality_summary()
        total_issues = sum(summary.values())
        
        print(f"\n" + "="*50)
        print(f"📊 DATA QUALITY DASHBOARD")
        print(f"="*50)
        
        for check, count in summary.items():
            status = "🚨" if count > 0 else "✅"
            print(f"{status} {check.replace('_', ' ').title()}: {count}")
        
        print(f"-"*50)
        if total_issues == 0:
            print(f"🎉 EXCELLENT: Baza danych jest w idealnym stanie!")
        elif total_issues <= 5:
            print(f"⚠️  GOOD: {total_issues} drobnych problemów do naprawienia")
        else:
            print(f"🚨 NEEDS ATTENTION: {total_issues} problemów wymaga uwagi")
        print(f"="*50)
        
        # Zawsze przechodzi - to tylko dashboard
        assert True