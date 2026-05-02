import re

from conftest import shot
from pages.admin_pg_page import AdminPgPage


def test_admin_can_execute_sql_query(admin_page):
    page = AdminPgPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_pg_01_home")

    # EX-AG01: Echte DB-Abfrage zeigt, dass die juntagrico_member-Tabelle Daten enthält
    # jpg renders results as an ASCII table: | COUNT(*) | / | 8 |
    result = page.execute_sql("SELECT COUNT(*) FROM juntagrico_member")
    shot(admin_page, "admin_pg_02_result")

    cell_values = re.findall(r'\|\s*(\d+)\s*\|', result)
    assert cell_values, f"SQL-Ergebnis sollte eine Zahl in Tabellenzellen enthalten, war: '{result}'"
    count = int(cell_values[0])
    assert count > 0, f"juntagrico_member-Tabelle sollte mindestens einen Eintrag haben, war: {count}"
