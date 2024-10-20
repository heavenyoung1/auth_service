from sqlalchemy.orm import DeclarativeBase

# Помещен сюда для решения проблемы циклических импортов
# Base - это базовый класс для управления схемами и таблицами БД
class Base(DeclarativeBase):
    pass