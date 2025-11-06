import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Загружаем настройки из .env
load_dotenv()


def view_all_records():
    """Просмотр всех записей из базы данных"""
    try:
        # Подключаемся к базе
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        cursor = conn.cursor()

        # Получаем все записи
        cursor.execute("""
            SELECT id, timestamp, activity, created_at 
            FROM activities 
            ORDER BY timestamp DESC
        """)

        records = cursor.fetchall()

        print("=" * 80)
        print("📊 ВСЕ ЗАПИСИ ИЗ БАЗЫ ДАННЫХ")
        print("=" * 80)

        if not records:
            print("❌ Записей пока нет")
            return

        for record in records:
            id, timestamp, activity, created_at = record
            print(f"🆔 ID: {id}")
            print(f"📅 Время активности: {timestamp}")
            print(f"📝 Деятельность: {activity}")
            print(f"⏰ Записано в БД: {created_at}")
            print("-" * 80)

        print(f"📈 Всего записей: {len(records)}")

        # Закрываем соединение
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Ошибка: {e}")


def view_today_records():
    """Просмотр записей за сегодня"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        cursor = conn.cursor()

        # Записи за сегодня
        cursor.execute("""
            SELECT id, timestamp, activity 
            FROM activities 
            WHERE DATE(timestamp) = CURRENT_DATE
            ORDER BY timestamp DESC
        """)

        records = cursor.fetchall()

        print("=" * 60)
        print("📅 ЗАПИСИ ЗА СЕГОДНЯ")
        print("=" * 60)

        for record in records:
            id, timestamp, activity = record
            time_str = timestamp.strftime("%H:%M")
            print(f"⏰ {time_str}: {activity}")

        print(f"📊 Сегодняшних записей: {len(records)}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    print("Выберите действие:")
    print("1 - Все записи")
    print("2 - Записи за сегодня")

    choice = input("Ваш выбор (1 или 2): ")

    if choice == "1":
        view_all_records()
    elif choice == "2":
        view_today_records()
    else:
        print("❌ Неверный выбор")