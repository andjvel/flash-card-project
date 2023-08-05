from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
dictionary = {}

# ------------------------------Create New Flash Cards---------------------------------
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    dictionary = original_data.to_dict(orient="records")
else:
    dictionary = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(dictionary)
    text_fr = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=text_fr, fill="black")
    canvas.itemconfig(card_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    text_en = current_card["English"]
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=text_en, fill="white")


def right():
    dictionary.remove(current_card)
    print(len(dictionary))
    d = pandas.DataFrame(dictionary)
    d.to_csv("data/words_to_learn.csv", index=False)
    next_card()

def wrong():
    next_card()


# ------------------------------UI---------------------------------
window = Tk()
window.title("Flash card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"), text="")
card_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"), text="")
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=right)
right_button.grid(row=1, column=1)
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=wrong)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
