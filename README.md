# envText

[English](README-en.md)


**首款**中文环境领域文本分析工具。仍然在内测中，敬请期待。

特性：  
1. :one:支持中文环境领域大规模预训练模型**envBert**！

2. :two:支持中文环境领域大规模预训练**词向量**!

3. :three:支持中文环境领域专家过滤的**词表**!

4. :four: **一且设计均为领域专家研究服务**：
    - 为神经网络模型精简了接口，只保留了必要的batch_size, learning_rate等参数
    - 进一步优化huggingface transformers输入输出接口，支持20余种数据集格式
    - 一键使用模型，让领域专家精力集中在分析问题上

5. :five: 使用transformers接口，支持轻松自定义模型

下一步计划：  
- [ ] 数据集支持：支持常用**标注工具**数据集  
    - [ ] 精灵标注助手  
    - [ ] Doccano  
    - [ ] universal data annotator
- [ ] **专题支持**  
    - [ ] 无监督实体/短语/固定搭配挖掘  
    - [ ] 气候变化文本分析工具箱  
    - [ ] 环境领域实体  
- [ ] 更新文档和案例  
        

如果您觉得本项目有用或是有帮助到您，麻烦您点击一下右上角的star :star:。您的支持是我们维护项目的最大动力:metal:！


# 使用方法

### 1. 安装

python环境配置

```bash
pip install envtext

#国内用户使用清华镜像加速
pip install envtext -i https://pypi.tuna.tsinghua.edu.cn/simple 
```
由于envtext库依赖于transformers和pytorch，故安装时间比较长，建议等待时喝一杯咖啡:coffee:。


### 2. 推理

目前支持的模型有：

| 任务名称 | Bert模型 | RNNs模型 | 其他模型 |
| ------ | ------ | ------ | ------ |
| 完型填空 | BertMLM  |  ------  |  ------  |
|  分类   | BertCLS  |  RNNCLS  |  ------  |
| 情感分析（回归） | BertSA  |  RNNSA  |  ------  |
|  多选   |BertMultiChoice | RNNMultiChoice | ----- |
| 实体识别 | BertNER  | RNNNER  | -----    |
| 词向量  |  -----  |  -----   | Word2Vec |

除文本生成任务外，基本支持绝大部分NLP任务。

Bert 支持环境领域大规模预训练模型`envBert`，也支持其他huggingface transformer的Bert模型。

RNNs模型包括`LSTM`,`GRU`,`RNN`三种，可以选择使用环境领域预训练的词向量初始化，也可以使用Onehot编码初始化。


#### 2.1 使用Bert

由于bert模型较大，建议从huggingface transformer上预先下载模型权重，
或者从我们提供的百度网盘链接上下载权重，保存到本地，方便使用。

百度网盘链接：  
链接：[百度网盘 envBert 模型](https://pan.baidu.com/s/1KNE5JnUoulLgVK9yW5WtAw)
提取码：lfwm 

```python
#导入完形填空模型(masked language model)
from envtext.models import BertMLM
model = BertMLM('celtics1863/env-bert-chinese')

#进行预测
model('[MASK][MASK][MASK][MASK]是各国政府都关心的话题')


#导出结果
model.save_result('result.csv')
```
#### 2.2 使用RNN

```python
from envtext.models import RNNCLS

model = RNNCLS('本地pytorch_model.bin所在文件夹')

#进行预测
model('气候变化是各国政府都关心的话题')

#导出结果
model.save_result('result.csv')
```

#### 2.3 使用word2vec

envtext自带长度为64的预训练词向量。
```python
from envtext.models import load_word2vec

model = load_word2vec()

model.most_similar('环境保护')
```

### 3. 训练

##### 3.1 Bert训练

```python
#导入分类模型(classification)
from envtext.models import BertCLS
model = BertCLS('celtics1863/env-bert-chinese')

# # 使用自定义数据集
# model.load_dataset('数据集位置',task = 'cls',format = '数据集格式')
# #使用自带的二分类数据集：
model.load_dataset('isclimate')

#模型训练
model.train()


#模型保存
model.save_model('classification') #输入待保存的文件夹
```

或者：

```python
#导入分类模型(classification)
from envtext.models import BertCLS
from envtext.data.utils import load_dataset

# # 使用自定义数据集
# datasets,config = load_dataset('数据集位置',task = 'cls',format = '数据集格式')
# #使用自带的二分类数据集：
datasets,config = load_dataset('isclimate')

model = BertCLS('celtics1863/env-bert-chinese',config)

#模型训练
model.train(datasets)

#模型保存
model.save_model('classification') #输入待保存的文件夹
```

##### 3.2 RNN训练

```python
#导入分类模型(classification)
from envtext.models import RNNCLS
model = RNNCLS()

# # 使用自定义数据集
# model.load_dataset('数据集位置',task = 'cls',format = '数据集格式')
# # 使用自带的二分类数据集：
model.load_dataset('isclimate')

#模型训练
model.train()


#模型保存
model.save_model('classification') #输入待保存的文件夹
```
或者

```python
#导入分类模型(classification)
from envtext.models import RNNCLS
from envtext.data.utils import load_dataset

# # 使用自定义数据集
# datasets,config = load_dataset('数据集位置',task = 'cls',format = '数据集格式')
# #使用自带的二分类数据集：
datasets,config = load_dataset('isclimate')

model = RNNCLS(config=config)

#模型训练
model.train(datasets)

#模型保存
model.save_model('classification') #输入待保存的文件夹
```


### 4. 自定义模型

##### 4.1 自定义Bert模型
首先自定义一个回归任务的Bert模型
```python
from envtext.models.bert_base import BertBase
import torch
from transformers import BertPreTrainedModel,BertModel

class MyBert(BertPreTrainedModel):
    def __init__(self, config):
        super(MyBert, self).__init__(config)
        self.bert = BertModel(config) #bert模型
        self.regressor = torch.nn.Linear(config.hidden_size, 1) #回归器
        self.loss = torch.nn.MSELoss() #损失函数
        
    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None,
              position_ids=None, inputs_embeds=None, head_mask=None):
        outputs = self.bert(input_ids,
                            attention_mask=attention_mask,
                            token_type_ids=token_type_ids,
                            position_ids=position_ids,
                            head_mask=head_mask,
                            inputs_embeds=inputs_embeds)
        #使用[CLS] token
        cls_output = outputs[0][:,0,:] 

        # 得到判别值
        logits = self.regressor(cls_output)

        outputs = (logits,)
        
        #这里需要与bert的接口保持一致，在有labels输入的情况下，返回(loss,logits)，否则返回(logits,)
        if labels is not None: 
            loss = self.loss(logits.squeeze(),labels)
            outputs = (loss,) + outputs
        return outputs

```
将模型与envtext的接口对接

```python
class MyBertModel(BertBase):
    #重写初始化函数
    def initialize_bert(self,path = None,config = None,**kwargs):
        super().initialize_bert(path,config,**kwargs)
        self.model = MyBert.from_pretrained(self.model_path)

    #[Optional] 可选 重写后处理预测结果的函数
    def postprocess(self,text, logits, print_result = True ,save_result = True):     
        logits = logits.squeeze()
        if print_result:
            #打印结果
            print(logits)
        
        if save_result:
            #保存结果
            self.result[text] = logits
            
     #[Optional] 可选 重新计算判别值函数，用于训练时提供除loss外的metrics信息
     def compute_metrics(eval_pred)
         from envtext.utils.metrics import metrics_for_reg
         return metrics_for_reg(eval_pred)
     
     #[Optional] 可选 用于对齐config中的参数，
     #因为有的时候需要接受多种参数的输入，例如分类任务时可以接受类别数量，也可以接受类别的列表，这时候可以通过这个接口对齐。
     def align_config(self):
         super().align_config()
         ##可以使用self.update_config() 或 self.set_attribute() 接口重新设置config
         pass
```

##### 4.1 自定义RNN模型

定义RNN模型也是类似的。  
先实现一个LSTM分类模型如下：

```python
from torch import nn
import torch
class MyRNN(nn.Module):
    def __init__(self,config):
        self.rnn = nn.LSTM(config.embed_size, config.hidden_size ,config.num_layers,batch_first = True)
        self.classifier = nn.Linear(config.hidden_size,config.num_labels)
    
    def forward(self,X,labels = None):
        X,_ = self.rnn(X)
        logits = self.classifier(X)
        
        #对齐接口，仍然需要在labels存在的情况下输出(loss,logits)，不存在的情况下输出(logits,)
        if labels is not None:
            loss = self.loss_fn(logits,labels)
            return (loss,logits) 
        return (logits,)
```

再将模型与envtext接口对接，
```python
import numpy as np
class MyRNNModel(BertBase):
    #重写初始化函数
    def initialize_bert(self,path = None,config = None,**kwargs):
        super().initialize_bert(path,config,**kwargs) #保持不变
        self.model = MyRNN.from_pretrained(self.model_path) 

    #[Optional] 可选 重写后处理预测结果的函数
    def postprocess(self,text, logits, print_result = True ,save_result = True):     
        pred = np.argmax(logits,axis = -1)
        if print_result:
            #打印结果
            print(pred)
        
        if save_result:
            #保存结果
            self.result[text] = pred
            
    #[Optional] 可选 重写metrics，增加loss以外的metric, 用于训练
    def compute_metrics(eval_pred):
        return {} #返回一个dict
        
    #[Optional] 可选 重写align_config，对齐config参数
    def align_config(self):
        super().align_config()
        pass
```

更详细的教程，请参见我们的案例 [jupyter notebooks]('jupyter_notebooks')

### 5. 使用建议

1. Bert模型比较大，如果只有cpu的情况下，建议先用RNN模型，跑出一个结果，观察数据集的数量/质量是否达标，再考虑是否用Bert模型。一般envbert模型要比RNN模型领先10个点左右，尤其在数据集越小的情况下，envbert的优势越明显。
2. 神经网络模型受到初始化权重影响，每一次训练的情况不一样，建议多跑几次，取最好的结果。
3. Learning rate, Epoch, Batchsize是三个最关键的超参数，需要对不同数据集小心调整。默认的参数可以在大多数情况下达到较优的值，但是一定不会达到最好的结果。

# LISENCE
Apache Lisence


