import argparse
import tensorflow as tf
import model
from dataset import get_dataset, preprocess_sentence


def inference(hparams, chatbot, tokenizer, sentence):
    sentence = preprocess_sentence(sentence)

    sentence = tf.expand_dims(
        hparams.start_token + tokenizer.encode(sentence) + hparams.end_token, axis=0
    )

    output = tf.expand_dims(hparams.start_token, 0)

    for _ in range(hparams.max_length):
        predictions = chatbot(inputs=[sentence, output], training=False)

        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

        if tf.equal(predicted_id, hparams.end_token[0]):
            break

        output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0)


def predict(hparams, chatbot, tokenizer, sentence):
    prediction = inference(hparams, chatbot, tokenizer, sentence)
    predicted_sentence = tokenizer.decode(
        [i for i in prediction if i < tokenizer.vocab_size]
    )
    return predicted_sentence

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def append_to_file(file_path, line):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{line}\n")
        
def get_last_ids(lines_file, conversations_file):
    lines = read_file(lines_file)
    conversations = read_file(conversations_file)

    last_line = lines[-1]
    last_conversation = conversations[-1]

    last_line_id = int(last_line.split(" +++$+++ ")[0][1:])
    last_user_id = int(last_conversation.split(" +++$+++ ")[1][1:])
    last_movie_id = int(last_conversation.split(" +++$+++ ")[2][1:])

    return last_line_id, last_user_id, last_movie_id

def update_data_files(user_input, bot_response, lines_file='data/lines.txt', conversations_file='data/conversations.txt'):
    last_line_id, last_user_id, last_movie_id = get_last_ids(lines_file, conversations_file)

    new_line_id = f"L{last_line_id + 1}"
    new_bot_line_id = f"L{last_line_id + 2}"
    new_user_id = f"u{last_user_id + 1}"
    new_bot_user_id = f"u{last_user_id + 2}"
    new_movie_id = f"m{last_movie_id + 1}"

    append_to_file(lines_file, f"{new_line_id} +++$+++ {new_user_id} +++$+++ {new_movie_id} +++$+++ Ben +++$+++ {user_input}")
    append_to_file(lines_file, f"{new_bot_line_id} +++$+++ {new_bot_user_id} +++$+++ {new_movie_id} +++$+++ Bot +++$+++ {bot_response}")

    new_conversation = f"{new_user_id} +++$+++ {new_bot_user_id} +++$+++ {new_movie_id} +++$+++ ['{new_line_id}', '{new_bot_line_id}']"
    append_to_file(conversations_file, new_conversation)

def get_feedback():
    feedback = input("Bu cevap yardımcı oldu mu? (Evet/Hayır):  ").lower()
    return feedback == "Evet"

def chat(hparams, chatbot, tokenizer):
    print("\nCHATBOT")

    for _ in range(5):
        sentence = input("Sen: ")
        output = predict(hparams, chatbot, tokenizer, sentence)
        print(f"\nBOT: {output}")
        
        
        user_input = sentence
        bot_response = output
        
        feedback = get_feedback()
        
        if feedback:
            update_data_files(user_input, bot_response)
        else:
            pass
        
        
def main(hparams):
    
    _, token = get_dataset(hparams)
    
    tf.keras.backend.clear_session()
    chatbot = tf.keras.models.load_model(
        hparams.save_model,
        custom_objects={
            "PositionalEncoding": model.PositionalEncoding,
            "MultiHeadAttention": model.MultiHeadAttention,
        },
        compile=False,
    )
    
    
    chat(hparams, chatbot, token)
    
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--save_model", default="model.h5", type=str, help="path save the model"
    )
    parser.add_argument(
        "--max_samples",
        default=25000,
        type=int,
        help="maximum number of conversation pairs to use",
    )
    parser.add_argument(
        "--max_length", default=40, type=int, help="maximum sentence length"
    )
    parser.add_argument("--batch_size", default=64, type=int)
    parser.add_argument("--num_layers", default=2, type=int)
    parser.add_argument("--num_units", default=512, type=int)
    parser.add_argument("--d_model", default=256, type=int)
    parser.add_argument("--num_heads", default=8, type=int)
    parser.add_argument("--dropout", default=0.1, type=float)
    parser.add_argument("--activation", default="relu", type=str)
    parser.add_argument("--epochs", default=80, type=int)
    
    main(parser.parse_args())
        
