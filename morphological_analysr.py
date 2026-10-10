import tkinter as tk
##from tkinter import scrolledtext
##import torch
##import json
##from model import Encoder, Decoder, Seq2Seq
##
### ---------------------
### Vocab class (from JSON)
### ---------------------
##class Vocab:
##    def __init__(self, itos, stoi):
##        self.itos = itos
##        self.stoi = stoi
##    
##    def __len__(self):
##        return len(self.itos)
##    
##    def __getitem__(self, token):
##        return self.stoi.get(token, self.stoi["<unk>"])
##    
##    def lookup_token(self, idx):
##        return self.itos[idx] if idx < len(self.itos) else "<unk>"
##
##def load_vocab(filename):
##    with open(filename, "r", encoding="utf-8") as f:
##        data = json.load(f)
##    return Vocab(data["itos"], data["stoi"])
##
### ---------------------
### Load model + vocab
### ---------------------
##SRC_vocab = load_vocab("SRC_vocab.json")
##TRG_vocab = load_vocab("TRG_vocab.json")
##
##device = torch.device("cpu")
##
##enc = Encoder(len(SRC_vocab), 128, 256, 2, 0.5)
##dec = Decoder(len(TRG_vocab), 128, 256, 2, 0.5)
##model = Seq2Seq(enc, dec, device).to(device)
##model.load_state_dict(torch.load("kannada_morph_model.pt", map_location="cpu"))
##model.eval()
##
### ---------------------
### Load POS Dictionary
### ---------------------
##with open("pos_dict.json", "r", encoding="utf-8") as f:
##    POS_DICT = json.load(f)
##
### ---------------------
### Inference
### ---------------------
##def correct_text_with_model(text):
##    tokens = ["<sos>"] + list(text) + ["<eos>"]
##    src_tensor = torch.tensor([SRC_vocab[token] for token in tokens]).unsqueeze(1)
##
##    hidden, cell = model.encoder(src_tensor)
##    outputs = []
##    input_token = torch.tensor([TRG_vocab["<sos>"]])
##
##    for _ in range(50):
##        prediction, hidden, cell = model.decoder(input_token, hidden, cell)
##        top1 = prediction.argmax(1).item()
##        if top1 == TRG_vocab.stoi["<eos>"]:
##            break
##        outputs.append(TRG_vocab.lookup_token(top1))
##        input_token = torch.tensor([top1])
##
##    return "".join(outputs)
##
### ---------------------
### Analyzer
### ---------------------
##def analyze_text():
##    text = input_text.get("1.0", tk.END).strip()
##    output_analysis.delete("1.0", tk.END)
##
##    if not text:
##        output_analysis.insert(tk.END, "ದಯವಿಟ್ಟು ಕನ್ನಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ.")
##        return
##    
##    corrected = correct_text_with_model(text)
##    mistakes = []
##
##    for i, (ch_in, ch_out) in enumerate(zip(text, corrected)):
##        if ch_in != ch_out:
##            mistakes.append(f"ಸ್ಥಾನ {i+1}: '{ch_in}' → '{ch_out}'")  
##    
##    if len(text) < len(corrected):
##        mistakes.append(f"ಹೆಚ್ಚುವರಿ ಅಕ್ಷರ: '{corrected[len(text):]}' ಸೇರಿಸಲಾಗಿದೆ")
##    elif len(text) > len(corrected):
##        mistakes.append(f"ಅಕ್ಷರ '{text[len(corrected):]}' ತೆಗೆದುಹಾಕಲಾಗಿದೆ")
##
##    if mistakes:
##        result = "ತಪ್ಪುಗಳು ಕಂಡುಬಂದವು:\n" + "\n".join(mistakes)
##    else:
##        result = "✅ ಯಾವುದೇ ತಪ್ಪುಗಳು ಕಂಡುಬಂದಿಲ್ಲ"
##
##    output_analysis.insert(tk.END, f"ಮೂಲ ಪಠ್ಯ: {text}\n")
##    output_analysis.insert(tk.END, result)
##
### ---------------------
### Corrector + POS
### ---------------------
##def correct_text():
##    text = input_text.get("1.0", tk.END).strip()
##    corrected = correct_text_with_model(text)
##
##    output_corrected.delete("1.0", tk.END)
##    output_corrected.insert(tk.END, f"{corrected}\n")
##
##    # Show POS tags below corrected sentence
##    tokens = corrected.split()
##    pos_line = []
##    for tok in tokens:
##        if tok in POS_DICT:
##            pos_line.append(f"{tok}({POS_DICT[tok]})")
##        else:
##            pos_line.append(f"{tok}(?)")
##    output_corrected.insert(tk.END, " ".join(pos_line))
##
### ---------------------
### Kannada Keyboard Popup
### ---------------------
##def open_keyboard():
##    x = root.winfo_rootx() + kb_button.winfo_x()
##    y = root.winfo_rooty() + kb_button.winfo_y() + kb_button.winfo_height()
##
##    kb_window = tk.Toplevel(root)
##    kb_window.title("Kannada Keyboard")
##    kb_window.geometry(f"+{x}+{y}")
##
##    current_layout = tk.StringVar(value="default")
##
##    def insert_char(ch, is_matra=False):
##        content = input_text.get("1.0", tk.END).rstrip("\n")
##        consonants = set("ಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲವಶಷಸಹಳಕ್ಷಜ್ಞ")
##
##        if is_matra and content and content[-1] in consonants:
##            input_text.delete("end-2c")
##            input_text.insert(tk.END, content[-1] + ch)
##        else:
##            input_text.insert(tk.END, ch)
##
##    def backspace():
##        content = input_text.get("1.0", tk.END)
##        if len(content) > 1:
##            input_text.delete("end-2c")
##
##    def space():
##        input_text.insert(tk.END, " ")
##
##    LAYOUTS = {
##        "default": [
##            ["ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ"],
##            ["ಕ", "ಖ", "ಗ", "ಘ", "ಙ", "ಚ", "ಛ", "ಜ", "ಝ", "ಞ"],
##            ["ಟ", "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "ಧ", "ನ"],
##            ["ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ", "ರ", "ಲ", "ವ"],
##            ["ಶ", "ಷ", "ಸ", "ಹ", "ಳ", "ಕ್ಷ", "ಜ್ಞ", "್"]
##        ],
##        "matras": [
##            ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ"],
##            ["ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ"],
##            ["ಂ", "ಃ"]
##        ],
##        "numbers": [
##            ["೦", "೧", "೨", "೩", "೪", "೫", "೬", "೭", "೮", "೯"],
##            ["!", "?", ",", ".", ":", ";", "-", "(", ")", "@"]
##        ]
##    }
##
##    key_frame = tk.Frame(kb_window)
##    key_frame.pack()
##
##    def draw_keys(layout):
##        for widget in key_frame.winfo_children():
##            widget.destroy()
##        for row in LAYOUTS[layout]:
##            row_frame = tk.Frame(key_frame)
##            row_frame.pack()
##            for ch in row:
##                is_matra = (layout == "matras")
##                btn = tk.Button(
##                    row_frame, text=ch, width=6, height=3, font=("Arial", 14),
##                    command=lambda c=ch, m=is_matra: insert_char(c, m)
##                )
##                btn.pack(side=tk.LEFT, padx=3, pady=3)
##
##    draw_keys(current_layout.get())
##
##    control_frame = tk.Frame(kb_window)
##    control_frame.pack(pady=6)
##
##    def switch_layout(new_layout):
##        current_layout.set(new_layout)
##        draw_keys(new_layout)
##
##    tk.Button(control_frame, text="Matras", width=10, height=2, font=("Arial", 12),
##              command=lambda: switch_layout("matras")).pack(side=tk.LEFT, padx=4)
##    tk.Button(control_frame, text="Numbers", width=10, height=2, font=("Arial", 12),
##              command=lambda: switch_layout("numbers")).pack(side=tk.LEFT, padx=4)
##    tk.Button(control_frame, text="Default", width=10, height=2, font=("Arial", 12),
##              command=lambda: switch_layout("default")).pack(side=tk.LEFT, padx=4)
##
##    tk.Button(control_frame, text="Space", width=10, height=2, font=("Arial", 12),
##              command=space).pack(side=tk.LEFT, padx=4)
##    tk.Button(control_frame, text="Backspace", width=12, height=2, font=("Arial", 12),
##              command=backspace).pack(side=tk.LEFT, padx=4)
##    tk.Button(control_frame, text="Close", width=8, height=2, font=("Arial", 12),
##              command=kb_window.destroy).pack(side=tk.LEFT, padx=4)
##
### ---------------------
### Tkinter GUI
### ---------------------
##root = tk.Tk()
##root.title("Kannada Morphological Analyzer & Generator")
##
##screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
##root.geometry(f"{int(screen_w*0.75)}x{int(screen_h*0.75)}")
##
##heading = tk.Label(
##    root, text="Kannada Morphological Analyzer and Generator",
##    font=("Arial", 16, "bold"), fg="blue"
##)
##heading.pack(pady=10)
##
##tk.Label(root, text="Enter Kannada text:").pack()
##input_text = scrolledtext.ScrolledText(root, width=80, height=5, font=("Arial", 14))
##input_text.pack()
##
##kb_button = tk.Button(root, text="Open Kannada Keyboard", command=open_keyboard, font=("Arial", 12))
##kb_button.pack(pady=5)
##
##tk.Button(root, text="Analyze", command=analyze_text, font=("Arial", 12)).pack(pady=5)
##tk.Label(root, text="Analysis Result:").pack()
##output_analysis = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, font=("Arial", 12))
##output_analysis.pack()
##
##tk.Button(root, text="Correct", command=correct_text, font=("Arial", 12)).pack(pady=5)
##tk.Label(root, text="Corrected Text + POS:").pack()
##output_corrected = scrolledtext.ScrolledText(root, width=80, height=5, wrap=tk.WORD, font=("Arial", 12))
##output_corrected.pack()
##
##root.mainloop()


import tkinter as tk
from tkinter import scrolledtext, ttk
import torch
import json
from model import Encoder, Decoder, Seq2Seq

# ---------------------
# Vocab class (from JSON)
# ---------------------
class Vocab:
    def __init__(self, itos, stoi):
        self.itos = itos
        self.stoi = stoi
    
    def __len__(self):
        return len(self.itos)
    
    def __getitem__(self, token):
        return self.stoi.get(token, self.stoi["<unk>"])
    
    def lookup_token(self, idx):
        return self.itos[idx] if idx < len(self.itos) else "<unk>"

def load_vocab(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Vocab(data["itos"], data["stoi"])

# ---------------------
# Load model + vocab
# ---------------------
SRC_vocab = load_vocab("SRC_vocab.json")
TRG_vocab = load_vocab("TRG_vocab.json")

device = torch.device("cpu")

enc = Encoder(len(SRC_vocab), 128, 256, 2, 0.5)
dec = Decoder(len(TRG_vocab), 128, 256, 2, 0.5)
model = Seq2Seq(enc, dec, device).to(device)
model.load_state_dict(torch.load("kannada_morph_model.pt", map_location="cpu"))
model.eval()

# ---------------------
# Load POS Dictionary
# ---------------------
with open("pos_dict.json", "r", encoding="utf-8") as f:
    POS_DICT = json.load(f)

# ---------------------
# Inference
# ---------------------
def correct_text_with_model(text):
    tokens = ["<sos>"] + list(text) + ["<eos>"]
    src_tensor = torch.tensor([SRC_vocab[token] for token in tokens]).unsqueeze(1)

    hidden, cell = model.encoder(src_tensor)
    outputs = []
    input_token = torch.tensor([TRG_vocab["<sos>"]])

    for _ in range(50):
        prediction, hidden, cell = model.decoder(input_token, hidden, cell)
        top1 = prediction.argmax(1).item()
        if top1 == TRG_vocab.stoi["<eos>"]:
            break
        outputs.append(TRG_vocab.lookup_token(top1))
        input_token = torch.tensor([top1])

    return "".join(outputs)

# ---------------------
# Analyzer
# ---------------------
def analyze_text():
    text = input_text.get("1.0", tk.END).strip()
    output_analysis.delete("1.0", tk.END)

    if not text:
        output_analysis.insert(tk.END, "ದಯವಿಟ್ಟು ಕನ್ನಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ.")
        return
    
    corrected = correct_text_with_model(text)
    mistakes = []

    for i, (ch_in, ch_out) in enumerate(zip(text, corrected)):
        if ch_in != ch_out:
            mistakes.append(f"ಸ್ಥಾನ {i+1}: '{ch_in}' → '{ch_out}'")  
    
    if len(text) < len(corrected):
        mistakes.append(f"ಹೆಚ್ಚುವರಿ ಅಕ್ಷರ: '{corrected[len(text):]}' ಸೇರಿಸಲಾಗಿದೆ")
    elif len(text) > len(corrected):
        mistakes.append(f"ಅಕ್ಷರ '{text[len(corrected):]}' ತೆಗೆದುಹಾಕಲಾಗಿದೆ")

    if mistakes:
        result = "ತಪ್ಪುಗಳು ಕಂಡುಬಂದವು:\n" + "\n".join(mistakes)
    else:
        result = "✅ ಯಾವುದೇ ತಪ್ಪುಗಳು ಕಂಡುಬಂದಿಲ್ಲ"

    output_analysis.insert(tk.END, f"ಮೂಲ ಪಠ್ಯ: {text}\n")
    output_analysis.insert(tk.END, result)

# ---------------------
# Corrector + POS → also fills table
# ---------------------
def correct_text():
    text = input_text.get("1.0", tk.END).strip()
    corrected = correct_text_with_model(text)

    output_corrected.delete("1.0", tk.END)
    output_corrected.insert(tk.END, f"{corrected}\n")

    # Clear old table entries
    for row in pos_table.get_children():
        pos_table.delete(row)

    # Show POS tags in table
    tokens = corrected.split()
    pos_line = []
    for tok in tokens:
        if tok in POS_DICT:
            pos = POS_DICT[tok]
        else:
            pos = "?"
        pos_line.append(f"{tok}({pos})")
        pos_table.insert("", "end", values=(tok, pos))

##    # Also show inline below corrected text
##    output_corrected.insert(tk.END, " ".join(pos_line))

# ---------------------
# Kannada Keyboard Popup
# ---------------------
def open_keyboard():
    x = root.winfo_rootx() + kb_button.winfo_x()
    y = root.winfo_rooty() + kb_button.winfo_y() + kb_button.winfo_height()

    kb_window = tk.Toplevel(root)
    kb_window.title("Kannada Keyboard")
    kb_window.geometry(f"+{x}+{y}")

    current_layout = tk.StringVar(value="default")

    def insert_char(ch, is_matra=False):
        content = input_text.get("1.0", tk.END).rstrip("\n")
        consonants = set("ಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲವಶಷಸಹಳಕ್ಷಜ್ಞ")

        if is_matra and content and content[-1] in consonants:
            input_text.delete("end-2c")
            input_text.insert(tk.END, content[-1] + ch)
        else:
            input_text.insert(tk.END, ch)

    def backspace():
        content = input_text.get("1.0", tk.END)
        if len(content) > 1:
            input_text.delete("end-2c")

    def space():
        input_text.insert(tk.END, " ")

    LAYOUTS = {
        "default": [
            ["ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ"],
            ["ಕ", "ಖ", "ಗ", "ಘ", "ಙ", "ಚ", "ಛ", "ಜ", "ಝ", "ಞ"],
            ["ಟ", "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "ಧ", "ನ"],
            ["ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ", "ರ", "ಲ", "ವ"],
            ["ಶ", "ಷ", "ಸ", "ಹ", "ಳ", "ಕ್ಷ", "ಜ್ಞ", "್"]
        ],
        "matras": [
            ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ"],
            ["ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ"],
            ["ಂ", "ಃ"]
        ],
        "numbers": [
            ["೦", "೧", "೨", "೩", "೪", "೫", "೬", "೭", "೮", "೯"],
            ["!", "?", ",", ".", ":", ";", "-", "(", ")", "@"]
        ]
    }

    key_frame = tk.Frame(kb_window)
    key_frame.pack()

    def draw_keys(layout):
        for widget in key_frame.winfo_children():
            widget.destroy()
        for row in LAYOUTS[layout]:
            row_frame = tk.Frame(key_frame)
            row_frame.pack()
            for ch in row:
                is_matra = (layout == "matras")
                btn = tk.Button(
                    row_frame, text=ch, width=6, height=3, font=("Arial", 14),
                    command=lambda c=ch, m=is_matra: insert_char(c, m)
                )
                btn.pack(side=tk.LEFT, padx=3, pady=3)

    draw_keys(current_layout.get())

    control_frame = tk.Frame(kb_window)
    control_frame.pack(pady=6)

    def switch_layout(new_layout):
        current_layout.set(new_layout)
        draw_keys(new_layout)

    tk.Button(control_frame, text="Matras", width=10, height=2, font=("Arial", 12),
              command=lambda: switch_layout("matras")).pack(side=tk.LEFT, padx=4)
    tk.Button(control_frame, text="Numbers", width=10, height=2, font=("Arial", 12),
              command=lambda: switch_layout("numbers")).pack(side=tk.LEFT, padx=4)
    tk.Button(control_frame, text="Default", width=10, height=2, font=("Arial", 12),
              command=lambda: switch_layout("default")).pack(side=tk.LEFT, padx=4)

    tk.Button(control_frame, text="Space", width=10, height=2, font=("Arial", 12),
              command=space).pack(side=tk.LEFT, padx=4)
    tk.Button(control_frame, text="Backspace", width=12, height=2, font=("Arial", 12),
              command=backspace).pack(side=tk.LEFT, padx=4)
    tk.Button(control_frame, text="Close", width=8, height=2, font=("Arial", 12),
              command=kb_window.destroy).pack(side=tk.LEFT, padx=4)

# ---------------------
# Tkinter GUI
# ---------------------
root = tk.Tk()
root.title("Kannada Morphological Analyzer & Generator")

screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{int(screen_w*0.9)}x{int(screen_h*0.9)}")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left frame (text + outputs)
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

heading = tk.Label(
    left_frame, text="Kannada Morphological Analyzer and Generator",
    font=("Arial", 16, "bold"), fg="blue"
)
heading.pack(pady=10)

tk.Label(left_frame, text="Enter Kannada text:").pack()
input_text = scrolledtext.ScrolledText(left_frame, width=80, height=5, font=("Arial", 14))
input_text.pack()

kb_button = tk.Button(left_frame, text="Open Kannada Keyboard", command=open_keyboard, font=("Arial", 12))
kb_button.pack(pady=5)

tk.Button(left_frame, text="Analyze", command=analyze_text, font=("Arial", 12)).pack(pady=5)
tk.Label(left_frame, text="Analysis Result:").pack()
output_analysis = scrolledtext.ScrolledText(left_frame, width=80, height=10, wrap=tk.WORD, font=("Arial", 12))
output_analysis.pack()

tk.Button(left_frame, text="Correct", command=correct_text, font=("Arial", 12)).pack(pady=5)
tk.Label(left_frame, text="Corrected Text + POS:").pack()
output_corrected = scrolledtext.ScrolledText(left_frame, width=80, height=5, wrap=tk.WORD, font=("Arial", 12))
output_corrected.pack()

# Right frame (POS Table)
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

tk.Label(right_frame, text="POS Tags Table", font=("Arial", 14, "bold")).pack(pady=5)

pos_table = ttk.Treeview(right_frame, columns=("Word", "POS"), show="headings", height=25)
pos_table.heading("Word", text="ಪದ (Word)", anchor="center")
pos_table.heading("POS", text="ಪದವರ್ಗ (POS)", anchor="center")
pos_table.column("Word", anchor="center", width=120)
pos_table.column("POS", anchor="center", width=150)
pos_table.pack(fill=tk.Y, expand=True)

# Bold heading style
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

root.mainloop()