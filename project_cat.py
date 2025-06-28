# pip install pillow
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import json
import os
import random

SAVE_FILE = "pet_save.json"


class Pet:
    def __init__(self, name, pet_type="Собака", hunger=5, happiness=5):
        self.name = name
        self.pet_type = pet_type  # "Кошка" или "Собака"
        self.hunger = hunger
        self.happiness = happiness

    def feed(self):
        self.hunger = min(self.hunger + 1, 10)

    def play(self):
        self.happiness = min(self.happiness + 1, 10)

    def hunger_decay(self):
        self.hunger = max(self.hunger - 1, 0)

    def happiness_decay(self):
        self.happiness = max(self.happiness - 1, 0)

    def get_status(self):
        mood = "😄" if self.happiness > 5 else "😢"
        hunger_state = "🍗" if self.hunger > 5 else "🥺"
        return f"{self.name} ({self.pet_type}) {mood} {hunger_state}\nСытость: {self.hunger}/10\nСчастье: {self.happiness}/10"

    def to_dict(self):
        return {
            "name": self.name,
            "pet_type": self.pet_type,
            "hunger": self.hunger,
            "happiness": self.happiness
        } 

    @staticmethod
    def from_dict(data):
        return Pet(data["name"], data.get("pet_type", "Собака"), data["hunger"], data["happiness"])


class PetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Виртуальный питомец")

        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.pet = Pet.from_dict(data)
        else:
            name = simpledialog.askstring("Имя", "Как назовем питомца?")
            pet_type = simpledialog.askstring("Выбор", "Кого завести? Кошка или Собака?")
            pet_type = pet_type.capitalize() if pet_type else "Собака"
            if pet_type not in ["Кошка", "Собака"]:
                pet_type = "Собака"
            self.pet = Pet(name if name else "Безымянный", pet_type)

        self.status_label = tk.Label(root, text=self.pet.get_status(), font=("Arial", 16), pady=20)
        self.status_label.pack()

        # Загрузка картинок по типу питомца
        if self.pet.pet_type == "Кошка":
            self.happy_image = ImageTk.PhotoImage(Image.open("cat_happy.png").resize((150, 150)))
            self.sad_image = ImageTk.PhotoImage(Image.open("cat_sad.png").resize((150, 150)))
        else:
            self.happy_image = ImageTk.PhotoImage(Image.open("dog_happy.png").resize((150, 150)))
            self.sad_image = ImageTk.PhotoImage(Image.open("dog_sad.png").resize((150, 150)))

        self.image_label = tk.Label(root, image=self.happy_image)
        self.image_label.pack()

        # Кнопки
        tk.Button(root, text="🍗 Кормить", command=self.feed_pet, width=30).pack(pady=5)
        tk.Button(root, text="🎾 Играть", command=self.play_with_pet, width=30).pack(pady=5)
        tk.Button(root, text="🎲 Угадай число", command=self.mini_game, width=30).pack(pady=5)
        tk.Button(root, text="✊ Камень-ножницы-бумага", command=self.rps_game, width=30).pack(pady=5)
        tk.Button(root, text="⚡ Быстрый клик", command=self.quick_click_game, width=30).pack(pady=5)
        tk.Button(root, text="💾 Сохранить", command=self.save_game, width=30).pack(pady=5)
        tk.Button(root, text="🚪 Выход", command=self.quit_game, width=30).pack(pady=20)

        self.update_gui()
        self.auto_hunger_decay()
        self.auto_happiness_decay()

    def quick_click_game(self):
        # Окно мини-игры
        game_window = tk.Toplevel(self.root)
        game_window.title("⚡ Быстрый клик")
        game_window.geometry("300x200")
        game_window.resizable(False, False)

        info_label = tk.Label(game_window, text="Нажми кнопку за 1 секунду!", font=("Arial", 12))
        info_label.pack(pady=10)

        clicked = {"value": False}

        def on_click():
            clicked["value"] = True
            self.pet.happiness = min(self.pet.happiness + 2, 10)
            messagebox.showinfo("Успех", "Ты успел! Питомец счастлив 😊")
            game_window.destroy()
            self.update_gui()

        def timeout():
            if not clicked["value"]:
                messagebox.showinfo("Упс", "Ты не успел 😢")
                game_window.destroy()
                self.update_gui()


        click_button = tk.Button(game_window, text="ЖМИ!", font=("Arial", 14), command=on_click)
        click_button.pack(pady=20)
        game_window.after(1000, timeout)

    def update_gui(self):
        self.status_label.config(text=self.pet.get_status())
        if self.pet.happiness > 5:
            self.image_label.config(image=self.happy_image)
        else:
            self.image_label.config(image=self.sad_image)

    def auto_hunger_decay(self):
        self.pet.hunger_decay()
        self.update_gui()
        self.root.after(10000, self.auto_hunger_decay)

    def auto_happiness_decay(self):
        self.pet.happiness_decay()
        self.update_gui()
        self.root.after(20000, self.auto_happiness_decay)

    def feed_pet(self):
        self.pet.feed()
        self.update_gui()

    def play_with_pet(self):
        self.pet.play()
        self.update_gui()

    def mini_game(self):
        number = random.randint(1, 5)
        guess = simpledialog.askinteger("Мини-игра", "Угадай число от 1 до 5")
        if guess == number:
            self.pet.happiness = min(self.pet.happiness + 3, 10)
            messagebox.showinfo("Победа!", f"Ты угадал! Это было {number}")
        else:
            messagebox.showinfo("Мимо", f"Нет, это было {number}")
        self.update_gui()

    def save_game(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.pet.to_dict(), f)
        messagebox.showinfo("Сохранено", "Игра сохранена!")

    def quit_game(self):
        self.save_game()
        self.root.quit()

    def rps_game(self):
        options = ["Камень", "Ножницы", "Бумага"]
        user_choice = simpledialog.askstring("Игра", "Выбери: Камень, Ножницы или Бумага")
        if not user_choice:
            return

        user_choice = user_choice.capitalize()
        if user_choice not in options:
            messagebox.showwarning("Ошибка", "Нужно выбрать: Камень, Ножницы или Бумага")
            return

        bot_choice = random.choice(options)
        result = ""

        win_map = {
            "Камень": "Ножницы",
            "Ножницы": "Бумага",
            "Бумага": "Камень"
        }

        if user_choice == bot_choice:
            self.pet.happiness = min(self.pet.happiness + 1, 10)
            result = f"Ничья! Оба выбрали {bot_choice}"
        elif win_map[user_choice] == bot_choice:
            self.pet.happiness = min(self.pet.happiness + 2, 10)
            result = f"Ты победил! {user_choice} бьёт {bot_choice}"
        else:
            self.pet.happiness = max(self.pet.happiness - 1, 0)
            result = f"Ты проиграл. {bot_choice} бьёт {user_choice}"

        messagebox.showinfo("Результат", result)
        self.update_gui()


if __name__ == "__main__":
    root = tk.Tk()
    app = PetApp(root)
    root.mainloop()