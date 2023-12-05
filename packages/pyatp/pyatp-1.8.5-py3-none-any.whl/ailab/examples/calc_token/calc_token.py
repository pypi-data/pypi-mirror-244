from flask import Flask, request, jsonify

app = Flask(__name__)

def calc_tokens(dataset_path:str, token_path:str):
    from datasets import load_dataset
    from transformers import AutoTokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(token_path, trust_remote_code=True)
    except Exception as e:
        from transformers import LlamaTokenizer
        tokenizer = LlamaTokenizer.from_pretrained(token_path)
    hf_dataset = load_dataset(path='json', data_files=dataset_path)

    def count_tokens(example):
        full_prompt = example['instruction'] + example['input'] + example['output']
        token_cnt = tokenizer.tokenize(full_prompt)
        len_token_cnt = len(token_cnt)
        return {'total_tokens':len_token_cnt}
    
    token_dict = hf_dataset.map(count_tokens,remove_columns=['instruction', 'input', 'output'])
    col_token = token_dict['train']['total_tokens']
    print(f'sum {sum(col_token)}')
    return sum(col_token)

@app.route('/calc_tokens', methods=['POST'])
def post_request():
    data = request.get_json()
    dataset_path = data['dataset_path']
    token_path = data['token_path']
    tokens_num = calc_tokens(dataset_path, token_path)
    result = {"tokens": tokens_num}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)