from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import torch

# Load pretrained model and classifier
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


def give_answer(question, paragraph):
    """

    :param question: (str) Query to be asked
    :param paragraph: (str) Corpus to find the answer within
    :return: (str) The correct answer of the query asked
    """
    encoding = tokenizer.encode_plus(text=question, text_pair=paragraph, add_special_tokens=True)
    # print("Encoding: ",encoding)
    inputs = encoding['input_ids']  # Token embeddings
    sentence_embedding = encoding['token_type_ids']  # Segment embeddings
    tokens = tokenizer.convert_ids_to_tokens(inputs)  # input tokens
    start_scores, end_scores = model(input_ids=torch.tensor([inputs]),
                                     token_type_ids=torch.tensor([sentence_embedding]))
    # print("Start Scores: ", start_scores)
    # print("End Scores: ", end_scores)
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)
    answer = ' '.join(tokens[start_index:end_index + 1])
    corrected_answer = ''

    for word in answer.split():
        # If it's a subword token
        if word[0:2] == '##':
            corrected_answer += word[2:]
        else:
            corrected_answer += ' ' + word
    return corrected_answer
