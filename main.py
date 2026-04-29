import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

books = []
tree = None
title_entry = None
author_entry = None
genre_entry = None
pages_entry = None
genre_filter = None
pages_filter = None

def validate_input():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()
    
    if not title:
        messagebox.showerror("Ошибка", "Название книги не может быть пустым!")
        return False
    if not author:
        messagebox.showerror("Ошибка", "Автор не может быть пустым!")
        return False
    if not genre:
        messagebox.showerror("Ошибка", "Жанр не может быть пустым!")
        return False
    if not pages:
        messagebox.showerror("Ошибка", "Количество страниц не может быть пустым!")
        return False
    try:
        pages_int = int(pages)
        if pages_int <= 0:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return False
    except ValueError:
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return False
    
    return True

def add_book():
    if not validate_input():
        return
    
    book = {
        "title": title_entry.get().strip(),
        "author": author_entry.get().strip(),
        "genre": genre_entry.get().strip(),
        "pages": int(pages_entry.get().strip())
    }
    
    books.append(book)
    clear_input_fields()
    refresh_table()
    messagebox.showinfo("Успех", "Книга успешно добавлена!")

def clear_input_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)

def apply_filter():
    genre_filter_text = genre_filter.get().strip().lower()
    pages_filter_text = pages_filter.get().strip()
    
    filtered_books = books.copy()
    
    if genre_filter_text:
        filtered_books = [book for book in filtered_books 
                         if genre_filter_text in book["genre"].lower()]
    
    if pages_filter_text:
        try:
            pages_min = int(pages_filter_text)
            filtered_books = [book for book in filtered_books 
                             if book["pages"] > pages_min]
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return
    
    display_books(filtered_books)

def reset_filter():
    genre_filter.delete(0, tk.END)
    pages_filter.delete(0, tk.END)
    refresh_table()

def refresh_table():
    display_books(books)

def display_books(books_to_display):
    for item in tree.get_children():
        tree.delete(item)
    
    for book in books_to_display:
        tree.insert("", "end", values=(
            book["title"],
            book["author"],
            book["genre"],
            book["pages"]
        ))

def delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите книгу для удаления!")
        return
    
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту книгу?"):
        values = tree.item(selected[0])["values"]
        title_to_delete = values[0]
        
        global books
        books = [book for book in books if book["title"] != title_to_delete]
        refresh_table()
        messagebox.showinfo("Успех", "Книга удалена!")

def save_data():
    try:
        filename = f"books.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", f"Данные сохранены в файл {filename}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

def load_data():
    filename = filedialog.askopenfilename(
        title="Выберите JSON файл",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    
    if filename:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                loaded_books = json.load(f)
            
            if isinstance(loaded_books, list):
                global books
                books = loaded_books
                refresh_table()
                messagebox.showinfo("Успех", f"Загружено {len(books)} книг")
            else:
                messagebox.showerror("Ошибка", "Неверный формат файла")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

def create_input_frame(parent):
    global title_entry, author_entry, genre_entry, pages_entry
    
    input_frame = tk.LabelFrame(parent, text="Добавление книги", padx=10, pady=10)
    input_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(input_frame, text="Название книги:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    title_entry = tk.Entry(input_frame, width=30)
    title_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    author_entry = tk.Entry(input_frame, width=25)
    author_entry.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    genre_entry = tk.Entry(input_frame, width=30)
    genre_entry.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(input_frame, text="Кол-во страниц:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    pages_entry = tk.Entry(input_frame, width=25)
    pages_entry.grid(row=1, column=3, padx=5, pady=5)
    
    add_button = tk.Button(input_frame, text="Добавить книгу", bg="green", fg="white",
                           command=add_book)
    add_button.grid(row=2, column=0, columnspan=4, pady=10)
    
    return input_frame

def create_filter_frame(parent):
    global genre_filter, pages_filter
    
    filter_frame = tk.LabelFrame(parent, text="Фильтрация", padx=10, pady=10)
    filter_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    genre_filter = tk.Entry(filter_frame, width=25)
    genre_filter.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(filter_frame, text="Страниц больше:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    pages_filter = tk.Entry(filter_frame, width=15)
    pages_filter.grid(row=0, column=3, padx=5, pady=5)
    
    filter_button = tk.Button(filter_frame, text="Применить фильтр", bg="blue", fg="white",
                              command=apply_filter)
    filter_button.grid(row=0, column=4, padx=10, pady=5)
    
    reset_button = tk.Button(filter_frame, text="Сбросить фильтр", bg="gray", fg="white",
                             command=reset_filter)
    reset_button.grid(row=0, column=5, padx=10, pady=5)
    
    return filter_frame

def create_table(parent):
    global tree
    
    table_frame = tk.Frame(parent)
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    columns = ("Название", "Автор", "Жанр", "Страницы")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)
    
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return tree

def create_button_frame(parent):
    button_frame = tk.Frame(parent)
    button_frame.pack(fill="x", padx=10, pady=10)
    
    delete_button = tk.Button(button_frame, text="Удалить выбранную книгу", bg="red", fg="white",
                              command=delete_book)
    delete_button.pack(side="left", padx=5)
    
    save_button = tk.Button(button_frame, text="Сохранить в JSON", bg="green", fg="white",
                            command=save_data)
    save_button.pack(side="left", padx=5)
    
    load_button = tk.Button(button_frame, text="Загрузить из JSON", bg="blue", fg="white",
                            command=load_data)
    load_button.pack(side="left", padx=5)
    
    return button_frame

def main():
    root = tk.Tk()
    root.title("Book Tracker - Трекер прочитанных книг")
    root.geometry("900x600")
    
    create_input_frame(root)
    create_filter_frame(root)
    create_table(root)
    create_button_frame(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
