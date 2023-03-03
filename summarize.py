import tkinter as tk
from tkinter import ttk
from transformers import pipeline
from newspaper import Article
import pyperclip

# ініціалізуємо модель для узагальнення текстів
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")

# створюємо UI
root = tk.Tk()
root.title("News Summarizer")
root.geometry("600x700")

notebook = ttk.Notebook()
notebook.pack(expand=True, fill="both")

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

frame1.pack(fill="both", expand=True)
frame2.pack(fill="both", expand=True)

notebook.add(frame1, text="Input Text")
notebook.add(frame2, text="Input URL")

# функція для узагальнення тексту новин
def summarize_news():
    # отримуємо введений текст новин
    news_text = news_input.get("1.0", tk.END)
    # узагальнюємо текст новин
    summarized_text = summarizer(news_text, max_length=300, min_length=30, do_sample=False)[0]["summary_text"]
    # виводимо узагальнений текст новин
    news_output["text"] = summarized_text

def summarize_url():
    url = url_input.get()
    article = Article(url)
    article.download()
    article.parse()
    url_text.insert(tk.END, article.text)
    summarized_text = summarizer(article.text, max_length=300, min_length=30, do_sample=False)[0]["summary_text"]
    url_output["text"] = summarized_text

def copy_text():
    text = news_output["text"]
    pyperclip.copy(text)

def url_copy_text():
    text = url_output["text"]
    pyperclip.copy(text)


# frame1
label = ttk.Label(frame1, text="Input text")
label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

news_input = tk.Text(frame1, height=20, width=70)
news_input.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

summarize_button = ttk.Button(frame1, text="Summarize", command=summarize_news)
summarize_button.grid(row=2, column=0, padx=5, pady=5)

copy_button = ttk.Button(frame1, text="Copy", command=copy_text)
copy_button.grid(row=2, column=1, pady=5)

label = ttk.Label(frame1, text="Generalized text:")
label.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

news_output = ttk.Label(frame1, wraplength=500, cursor="arrow")
news_output.grid(row=4, column=0, padx=0, pady=5, sticky='nw', columnspan=2)

# frame2
label = ttk.Label(frame2, text="Input URL")
label.grid(row=0, column=0, padx=5, pady=5)

url_input = ttk.Entry(frame2, width=50)
url_input.grid(row=1, column=0, padx=5, pady=5)

url_button = ttk.Button(frame2, text="Summarize", command=summarize_url)
url_button.grid(row=2, column=0, padx=5, pady=5)


label = ttk.Label(frame2, text="Output text from Article")
label.grid(row=3, column=0, padx=5, pady=5)

url_text = tk.Text(frame2, height=20, width=70)
url_text.grid(row=4, column=0, padx=5, pady=5, sticky="nw")

url_copy_button = ttk.Button(frame2, text="Copy", command=url_copy_text)
url_copy_button.grid(row=5, column=0, pady=5)

label = ttk.Label(frame2, text="Generalized text:")
label.grid(row=6, column=0, padx=5, pady=5)

url_output = ttk.Label(frame2, wraplength=500)
url_output.grid(row=7, column=0, padx=5, pady=5, sticky="nw")

# запускаємо UI
root.mainloop()
