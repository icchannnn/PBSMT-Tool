from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_idiom():
    input_idiom = request.json.get('input_idiom')

    # Run the Moses translation command with the input idiom
    command = f"/mnt/c/smt/smt/mosesdecoder/tools/bin/moses -f /mnt/c/smt/smt/working/train/model/moses.ini <(echo '{input_idiom}')"
    translation = subprocess.check_output(command, shell=True).decode('utf-8').strip()

    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
