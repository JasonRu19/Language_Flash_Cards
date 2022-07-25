BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
import pandas as pd
import random
import csv


# ----------- CREATING NEW FLASHCARDS ------------

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    words_to_learn = data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")



current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language, text="French")
    canvas.itemconfig(word, text=current_card["French"])
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language, text="English")
    canvas.itemconfig(word, text=current_card["English"])


def correct():
    words_to_learn.remove(current_card)
    df = pd.DataFrame(words_to_learn)
    df.to_csv("data/words_to_learn.csv", index = False)


# -------------- UI SETUP ------------------------


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


canvas = Canvas(width=800, height=526,bg = BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
language = canvas.create_text((400, 150), text="Text", fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text((400, 263), text="Word", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

flip_timer = window.after(3000, flip_card)

correct_img = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_img, highlightthickness=0, command= lambda: [next_card(), correct()])
correct_button.grid(column=1, row=2)

incorrect_img = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=incorrect_img, highlightthickness=0, command= next_card)
incorrect_button.grid(column=0, row=2)

next_card()


window.mainloop()

