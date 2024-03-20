import re
import tensorflow as tf
import tensorflow_datasets as tfds
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('punkt')

lemmatizer = WordNetLemmatizer()


def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()
    
    sentence = re.sub(r"([?.!¿])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)
    sentence = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", sentence)

    sentence = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ?.!,¿]+", " ", sentence)
    sentence = sentence.strip()  
    
    sentence = ' '.join([lemmatizer.lemmatize(w) for w in nltk.word_tokenize(sentence)])
    
    return sentence

def load_conversations(hparams, lines_file, conversations_file):
    id2line = {}
    
    with open(lines_file, encoding = "utf-8", errors="ignore") as file:
        lines = file.readlines()
    
    for line in lines:
        parts = line.replace("\n", "").split(" +++$+++ ")
        id2line[parts[0]] = parts[4]
        
    questions = []
    answers = []
    
    with open(conversations_file, "r") as file:
        lines = file.readlines()
    for line in lines:
        parts = line.replace("\n", "").split(" +++$+++ ")
        conversation = [line[1:-1] for line in parts[3][1:-1].split(", ")]
        for i in range(len(conversation) - 1):
            questions.append(preprocess_sentence(id2line[conversation[i]]))
            answers.append(preprocess_sentence(id2line[conversation[i + 1]]))
            if len(questions) >= hparams.max_samples:
                return questions, answers
            
    return questions, answers


def tokenize(hparams, tokenizer, questions, answers):
    tokenized_inputs, tokenized_outputs = [], []
    
    for (question, answer) in zip(questions, answers):
        sentence1 = hparams.start_token + tokenizer.encode(question) + hparams.end_token
        sentence2 = hparams.start_token + tokenizer.encode(answer) + hparams.end_token
        
        if (len(sentence1) <= hparams.max_length and len(sentence2) <= hparams.max_length):
            tokenized_inputs.append(sentence1)
            tokenized_outputs.append(sentence2)
    
    tokenized_inputs = tf.keras.preprocessing.sequence.pad_sequences(
        tokenized_inputs, maxlen=hparams.max_length, padding="post")
    tokenized_outputs = tf.keras.preprocessing.sequence.pad_sequences(
        tokenized_outputs, maxlen=hparams.max_length, padding="post")

    return tokenized_inputs, tokenized_outputs


def get_dataset(hparams):
    lines_file ="data/lines.txt"
    conversations_file = "data/conversations.txt"
    
    questions, answers = load_conversations(hparams, lines_file, conversations_file)
    
    tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(questions + answers, target_vocab_size=2**13)
    
    tokenizer.save_to_file('tokenizer')
    
    hparams.start_token = [tokenizer.vocab_size]
    hparams.end_token = [tokenizer.vocab_size + 1]
    hparams.vocab_size = tokenizer.vocab_size + 2
    
    questions, answers = tokenize(hparams, tokenizer, questions, answers)
    
    dataset = tf.data.Dataset.from_tensor_slices(
        ({"inputs": questions, "dec_inputs": answers[:, :-1]}, answers[:, 1:])
    )
    
    dataset = dataset.cache()
    dataset = dataset.shuffle(len(questions))
    dataset = dataset.batch(hparams.batch_size)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    
    return dataset, tokenizer



