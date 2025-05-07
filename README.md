Команда для запуска тестов (можно добавить еще один флаг -s для отображения всей информации, например print)
pytest tests\test_auth.py -v

запуск pytest-cov
# С подробным выводом непокрытых строк
pytest --cov=app --cov-report=term-missing tests/