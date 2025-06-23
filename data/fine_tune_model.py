import json
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Load training data
with open('training_data.json', 'r') as f:
    training_data = json.load(f)

# Prepare dataset
questions = [item['question'] for item in training_data]
answers = [item['answer'] for item in training_data]

# Load tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased')

# Tokenize data
def preprocess_function(examples):
    encodings = tokenizer(
        examples['question'],
        examples['context'],
        truncation=True,
        padding='max_length',
        max_length=512,
        return_offsets_mapping=True
    )
    
    start_positions = []
    end_positions = []
    
    for i, (context, answer) in enumerate(zip(examples['context'], examples['answer'])):
        context_tokens = tokenizer(context, truncation=True, max_length=512).tokens
        answer_tokens = tokenizer(answer, truncation=True, max_length=512).tokens
        
        start_idx = context.find(answer)
        if start_idx == -1:
            start_positions.append(0)
            end_positions.append(0)
        else:
            end_idx = start_idx + len(answer)
            start_positions.append(start_idx)
            end_positions.append(end_idx)
    
    encodings['start_positions'] = start_positions
    encodings['end_positions'] = end_positions
    return encodings

# Create dataset
dataset = Dataset.from_dict({
    'question': questions,
    'context': answers,
    'answer': answers
})

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Split dataset
train_dataset = tokenized_dataset.train_test_split(test_size=0.1)['train']
eval_dataset = tokenized_dataset.train_test_split(test_size=0.1)['test']

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy='steps',
    save_steps=100,
    save_total_limit=2,
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')

print("Model fine-tuning complete.")