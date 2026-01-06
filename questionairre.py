import tkinter as tk
from tkinter import messagebox

# ---------- ISAA QUESTIONS (Example Wording Placeholders) ----------
questions = [
    "1. Does the child have difficulty maintaining attention?",
    "2. Does the child avoid eye contact frequently?",
    "3. Does the child repeat words or phrases?",
    "4. Does the child like to line up objects repeatedly?",
    "5. Does the child show limited interest in playing with others?",
    "6. Does the child resist changes in routine?",
    "7. Does the child become upset by loud sounds?",
    "8. Does the child respond slowly to their name?",
    "9. Does the child get fixated on certain topics?",
    "10. Does the child struggle to understand instructions?",
    "11. Does the child display unusual facial expressions?",
    "12. Does the child avoid group activities?",
    "13. Does the child show repetitive hand movements?",
    "14. Does the child rarely share interests with others?",
    "15. Does the child take things literally?",
    "16. Does the child have difficulty making friends?",
    "17. Does the child react strongly to touch?",
    "18. Does the child have difficulty expressing emotions?",
    "19. Does the child struggle with pretend play?",
    "20. Does the child become distressed in busy places?",
    "21. Does the child insist on doing things the same way?",
    "22. Does the child have limited gestures?",
    "23. Does the child avoid physical contact?",
    "24. Does the child prefer being alone?",
    "25. Does the child have difficulty copying actions?",
    "26. Does the child show repetitive behaviors?",
    "27. Does the child find it hard to follow social rules?",
    "28. Does the child misunderstand jokes?",
    "29. Does the child speak in a flat tone?",
    "30. Does the child show intense interest in certain objects?",
    "31. Does the child struggle with turn-taking?",
    "32. Does the child become rigid in thinking?",
    "33. Does the child have difficulty in group conversations?",
    "34. Does the child show delayed language?",
    "35. Does the child focus on details rather than the whole?",
    "36. Does the child have difficulty recognizing emotions?",
    "37. Does the child repeat actions frequently?",
    "38. Does the child react strongly to textures?",
    "39. Does the child find transitions difficult?",
    "40. Does the child get overwhelmed by sensory input?",
    "41. Does the child avoid imaginative games?",
    "42. Does the child prefer predictable environments?",
    "43. Does the child show unusual body posture or movement?",
    "44. Does the child take time to form social bonds?",
    "45. Does the child misunderstand social cues?",
    "46. Does the child rely on routines for comfort?",
    "47. Does the child show repetitive speech?",
    "48. Does the child find communication confusing?",
    "49. Does the child have difficulty adjusting to new places?",
    "50. Does the child often seem socially distant?"
]

# ---------- OPTIONS (ISAA-style: 0–3 scoring) ----------
options = [
    ("Rarely / Never", 0),
    ("Sometimes", 1),
    ("Often", 2),
    ("Very Often", 3)
]

answers = [-1] * len(questions)

current_q = 0

# ---------- GUI ----------
root = tk.Tk()
root.title("Indian Scale for Assessment — Screening Tool")
root.geometry("800x500")
root.configure(bg="#e8f0ff")

title = tk.Label(root, text="Indian Scale for Assessment — Screening Tool",
                 font=("Arial", 20, "bold"), bg="#4a6cf7", fg="white", pady=15)
title.pack(fill="x")

frame = tk.Frame(root, bg="#e8f0ff")
frame.pack(expand=True)

question_label = tk.Label(frame, text="", font=("Arial", 14), bg="#e8f0ff", wraplength=700)
question_label.pack(pady=20)

var = tk.IntVar()

radio_buttons = []
for text, val in options:
    rb = tk.Radiobutton(frame, text=text, variable=var, value=val, font=("Arial", 12),
                        bg="#e8f0ff", activebackground="#d6e0ff")
    rb.pack(anchor="w", padx=40, pady=5)
    radio_buttons.append(rb)

nav = tk.Frame(root, bg="#e8f0ff")
nav.pack(pady=10)

back_btn = tk.Button(nav, text="⬅ Back", font=("Arial", 12), command=lambda: change_q(-1))
next_btn = tk.Button(nav, text="Next ➡", font=("Arial", 12), command=lambda: change_q(1))

back_btn.grid(row=0, column=0, padx=10)
next_btn.grid(row=0, column=1, padx=10)

progress = tk.Label(root, text="", font=("Arial", 12), bg="#e8f0ff")
progress.pack(pady=5)


# ---------- FUNCTIONS ----------
def load_q():
    question_label.config(text=questions[current_q])
    progress.config(text=f"Question {current_q + 1} of {len(questions)}")

    if answers[current_q] != -1:
        var.set(answers[current_q])
    else:
        var.set(-1)


def change_q(direction):
    global current_q

    if var.get() == -1:
        messagebox.showwarning("Select an answer", "Please select an option before continuing.")
        return

    answers[current_q] = var.get()
    current_q += direction

    if current_q == len(questions):
        show_result()
        return

    if current_q < 0:
        current_q = 0

    load_q()


def show_result():
    total = sum(a for a in answers if a != -1)

    if total < 40:
        txt = "Low indicator score. This does not generally suggest elevated concern."
    elif total < 80:
        txt = "Mild indicator score. Monitoring and supportive guidance may be helpful."
    elif total < 120:
        txt = "Moderate indicator score. Consider discussing observations with a qualified professional."
    else:
        txt = "High indicator score. A professional developmental assessment may be beneficial."

    messagebox.showinfo("Screening Summary",
                        f"Total Score: {total}\n\nThis screening tool is not a diagnosis.\n\n{txt}")

    root.destroy()


load_q()

root.mainloop()
