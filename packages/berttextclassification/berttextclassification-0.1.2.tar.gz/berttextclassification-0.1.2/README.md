# About
一个用于训练和调用bert模型完成数据分类的python包。

# Install
`$ pip3 install -U berttextclassification`

# Director 
+ bert
    + bert\_lawlaw.py 
    + DataLawlaw.py
    + train.py
    + evaluate.py
    + acc\_and\_f1.py
    + BertModel.py
    + predict.py

## bert\_lawlaw.py
main程序完成训练到评估，默认是只评估不进行训练。

## DataLawlaw.py
定义了一个LawlawProcessor类，封装了一个，完成分类任务中数据相关的操作。
- LawlawProcessor类
  - get\_labels函数
    五个设定好的分类标签
  - load\_train\_examples函数
    加载json格式的训练数据
  - load\_dev\_examples函数
    加载json格式的评估数据

## train.py
对模型进行训练，并保存训练数据。
- train函数
  根据设置的batch\_size和epoch进行训练。将lr和loss写到tensorboard中，根据save\_steps保存不同checkpoint的模型。

## evaluate.py
对验证集进行评估，得到训练结果。
- evaluate函数
  对选择的model进行评估，并给出acc\_and\_f1函数返回的三项分值参数。

## acc\_and\_f1.py
计算bert模型预测后的分值。
- acc\_and\_f1函数
  计算模型预测标签的三项分值参数acc，f1\_score和acc\_and\_f1二者的平均值。

## BertModel.py
对Bert模型的相关操作，包括设置种子、加载模型和保存模型。
- set\_seed函数
  设置种子数值。
- load\_model函数
  从output\_dir加载model和tokenizer
- save\_model函数
  将model和tokenizer保存到output\_dir

## predict.py
对输入的文本进行分类预测。
- predict函数
  使用加载的模型，对输入文本进行分类。

# Usage
对模型进行训练，并保存模型
```python3
from BertModel import set_seed, init_model, load_model, save_model
from DataLawlaw import LawlawProcessor
from train import train

set_seed()
task = 'lawlaw'
processor = LawlawProcessor(task)
label_list = processor.get_labels()
model, tokenizer = init_model(task, len(label_list))
train_dataset = processor.load_train_examples(tokenizer, max_seq_length=128)
global_step, tr_loss = train(
    model,
    train_dataset,
    train_batch_size=8,
    num_train_epochs=5.0,
    save_steps=1000,
    output_dir='./outs'
)
save_model(model, tokenizer, output_dir='./outs')
```
对模型进行测试
```python3
from BertModel import set_seed, init_model, load_model, save_model
from DataLawlaw import LawlawProcessor
from evaluate import evaluate

set_seed()
task = 'lawlaw'
processor = LawlawProcessor(task)
model, tokenizer = load_model(output_dir='./outs')
eval_dataset = processor.load_dev_examples(tokenizer, max_seq_length=128)
result = evaluate(
    model,
    eval_dataset,
    eval_batch_size=16,
    output_dir='./outs'
)
print(result)
```

# Contact us
<may.xiaoya.zhang@gmail.com>
