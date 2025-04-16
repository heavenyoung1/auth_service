from sqlalchemy import create_engine

engine = create_engine("ЗДЕСЬ ВПИШИ СВОЮ БД ПОЗЖЕ", echo=True)
URL = "СТРОКА ДЛЯ ПОДКЛЮЧЕНИЯ БД"
# Позже выбери один из вариантов создания движка
# create_engine.echo = True (регистрация всех инструкций, есть также False/debug)