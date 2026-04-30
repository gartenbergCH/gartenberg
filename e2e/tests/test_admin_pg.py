from conftest import shot
from pages.admin_pg_page import AdminPgPage


def test_admin_can_execute_sql_query(admin_page):
    page = AdminPgPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_pg_01_home")

    result = page.execute_sql("SELECT 42 AS answer")
    shot(admin_page, "admin_pg_02_result")

    assert "42" in result, f"SQL-Ergebnis sollte '42' enthalten, war: '{result}'"
