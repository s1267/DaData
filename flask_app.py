from flask import Flask, render_template, request, redirect, url_for, jsonify
from api import Cleaner, Suggester
from crud import get_config, create_config, update_config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    config = get_config()
    if not config:
        create_config('test', 'test', 'ru', 10)
        hello()
    if request.method == 'POST':
        form_data = request.form
        if config.api_key == 'test' or config.api_key == 'test':
            return jsonify({'status': 'error', 'message': 'У вас тестовый профиль конфигурации'})
        else:
            cleaner = Cleaner(config.api_key, config.api_secret)
            suggester = Suggester(config.api_key, config.api_secret)
            cleaned_address = cleaner.clean('address', form_data['address'])
            if cleaned_address:
                cleaned_address = cleaned_address[0]['result']
                suggestion = suggester.suggest('address', cleaned_address, count=config.max_notes,
                                               language=config.response_language)
                if suggestion:
                    suggestion['status'] = 'ok'
                    return jsonify(suggestion)
                else:
                    return jsonify({'status': 'error', 'message': 'Ошибка при отправке запроса'})

            else:
                return jsonify({'status': 'error', 'message': 'Ошибка при отправке запроса'})
    return render_template('index.html', addresses=[])


@app.route('/config', methods=['GET', 'POST'])
def config_page():
    config = get_config()
    if not config:
        create_config('test', 'test', 'ru', 10)
        hello()
    if request.method == 'POST':
        form_data = request.form
        update_config(**form_data)
        return redirect(url_for('config_page'))

    return render_template('config.html', api_key=config.api_key, api_secret=config.api_secret,
                           max_notes=config.max_notes, response_language=config.response_language)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
