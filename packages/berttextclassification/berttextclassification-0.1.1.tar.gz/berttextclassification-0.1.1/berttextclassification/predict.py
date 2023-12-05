# https://www.cnblogs.com/zhangxianrong/p/15066981.html
from berttextclassification.BertModel import load_model
from berttextclassification.DataLawlaw import LawlawProcessor
import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_path, model, tokenizer = None, None, None

def init_model(path):
    global model_path
    model_path = path

def predict(lines):
    if not model:
        global model, tokenizer
        model, tokenizer = load_model(model_path)
        labels = LawlawProcessor('lawlaw', model_path).get_labels()
    model.eval()
    tokenized_text = tokenizer(
        lines,
        max_length=128,
        add_special_tokens=True,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )
    tokenized_text = tokenized_text.to(DEVICE)
    with torch.no_grad():
        logits = model(**tokenized_text, labels=None)
    pred = logits[0].argmax() % len(labels)
    return labels[pred]
