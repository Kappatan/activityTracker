import tkinter as tk
from tkinter import messagebox
import time
import threading
from datetime import datetime
import psycopg2
from psycopg2 import sql
import os

class BackgroundTracker:
    def __init__(self):
        # Создаем главное окно, но пока скрываем его
        self.root = tk.Tk()
        self.root.title("Трекер активности")
        self.root.geometry("500x400")

        # Сразу центрируем
        self.center_window()

        # Настраиваем интерфейс
        self.setup_ui()

        # Скрываем окно при запуске
        self.root.withdraw()

        # Запускаем таймер в фоне
        self.start_background_timer()

    def init_postgres_database(self):
        """Подключаемся к PostgreSQL и создаем таблицу"""
        try:
            # ↓↓↓ ДОБАВЛЕНО: Подключение к PostgreSQL ↓↓↓
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                port=os.getenv('DB_PORT')
            )
            self.cursor = self.conn.cursor()

            # ↓↓↓ ДОБАВЛЕНО: Создание таблицы в PostgreSQL ↓↓↓
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL,
                    activity TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            print("✅ PostgreSQL подключена!")

        except Exception as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
            messagebox.showerror("Ошибка БД", f"Не удалось подключиться к PostgreSQL:\n{e}")
    def center_window(self):
        """Центрируем окно на экране"""
        self.root.update_idletasks()
        width = 500
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Настраиваем интерфейс"""
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Что вы делали последние 30 минут?",
            font=("Arial", 16, "bold"),
            fg="#C71585",
            bg='#FFE4E1'
        )
        title_label.pack(pady=20)

        # Поле для ввода текста
        self.text_area = tk.Text(
            self.root,
            height=10,
            width=50,
            font=("Arial", 12),
            wrap=tk.WORD,
            bg='white',
            fg='#333333'
        )
        self.text_area.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Кнопка сохранения
        button_frame = tk.Frame(self.root, bg='#FFE4E1')
        button_frame.pack(pady=10)

        self.save_btn = tk.Button(
            button_frame,
            text="💾 Сохранить",
            command=self.save_activity,
            font=("Arial", 14),
            bg="#FF69B4",
            fg="white",
            padx=20,
            pady=10
        )
        self.save_btn.pack(side=tk.LEFT, padx=10)

    def start_background_timer(self):
        """Запускаем таймер в отдельном потоке"""
        timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        timer_thread.start()
        print("🚀 Трекер запущен в фоновом режиме! Окно появится через 30 минут.")

    def timer_loop(self):
        """Основной цикл таймера"""
        while True:
            # Ждем 30 минут (1800 секунд)
            # Для теста можно поставить 10 секунд: time.sleep(10)
            time.sleep(1800)
            # time.sleep(10)
            # Показываем окно в основном потоке
            self.root.after(0, self.show_reminder)

    def show_reminder(self):
        """Показываем всплывающее окно"""
        # Сначала показываем уведомление
        messagebox.showwarning(
            "Время отчета!",
            "Прошло 30 минут! Запишите, что вы делали."
        )

        # Показываем основное окно
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.text_area.focus()

    def save_activity(self):
        """Сохраняем активность и скрываем окно"""
        activity = self.text_area.get("1.0", tk.END).strip()

        if activity:
            # Сохраняем в файл
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("activities.txt", "a", encoding="utf-8") as f:
                f.write(f"{timestamp}: {activity}\n")

            # Очищаем поле и скрываем окно
            self.text_area.delete("1.0", tk.END)
            self.root.withdraw()

            messagebox.showinfo("Сохранено", "✅ Активность записана!")
        else:
            messagebox.showwarning("Ошибка", "📝 Введите описание активности!")

    def run(self):
        """Запускаем приложение"""
        self.root.mainloop()


# Запуск приложения
if __name__ == "__main__":
    app = BackgroundTracker()
    app.run()