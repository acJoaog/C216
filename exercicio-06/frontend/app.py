import json
import os
import urllib.error
import urllib.request

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')


def fetch_alunos():
    url = f"{BACKEND_URL}/api/v1/alunos/"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {'error': f'Erro HTTP {e.code}: {e.reason}'}
    except urllib.error.URLError as e:
        return {'error': f'Erro de conexão: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}


def fetch_aluno(aluno_id):
    url = f"{BACKEND_URL}/api/v1/alunos/{aluno_id}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {'error': f'Erro HTTP {e.code}: {e.reason}'}
    except urllib.error.URLError as e:
        return {'error': f'Erro de conexão: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}


def send_json_request(url, method, data):
    try:
        payload = json.dumps(data).encode('utf-8')
        request_obj = urllib.request.Request(
            url,
            data=payload,
            headers={'Content-Type': 'application/json'},
            method=method,
        )
        with urllib.request.urlopen(request_obj, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            details = e.read().decode('utf-8')
        except Exception:
            details = e.reason
        return {'error': f'Erro HTTP {e.code}: {details}'}
    except urllib.error.URLError as e:
        return {'error': f'Erro de conexão: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}


def criar_aluno(data):
    url = f"{BACKEND_URL}/api/v1/alunos/"
    return send_json_request(url, 'POST', data)


def atualizar_aluno(aluno_id, data):
    url = f"{BACKEND_URL}/api/v1/alunos/{aluno_id}"
    return send_json_request(url, 'PATCH', data)


def parse_aluno_form(form):
    return {
        'nome': form.get('nome', '').strip(),
        'email': form.get('email', '').strip(),
        'curso': form.get('curso', '').strip(),
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/alunos')
def alunos():
    alunos_data = fetch_alunos()
    error = None
    if isinstance(alunos_data, dict) and 'error' in alunos_data:
        error = alunos_data['error']
        alunos_data = []
    return render_template('alunos.html', alunos=alunos_data, edit_aluno=None, is_edit=False, error=error)


@app.route('/alunos/editar/<aluno_id>')
def editar_aluno(aluno_id):
    aluno = fetch_aluno(aluno_id)
    alunos_data = fetch_alunos()
    error = None
    if isinstance(aluno, dict) and 'error' in aluno:
        error = aluno['error']
        aluno = None
    if isinstance(alunos_data, dict) and 'error' in alunos_data:
        error = error or alunos_data['error']
        alunos_data = []
    return render_template(
        'alunos.html',
        alunos=alunos_data,
        edit_aluno=aluno,
        is_edit=True,
        error=error,
    )


@app.route('/alunos/cadastrar', methods=['POST'])
def cadastrar_aluno():
    aluno_data = parse_aluno_form(request.form)
    if not aluno_data['nome'] or not aluno_data['email'] or not aluno_data['curso']:
        alunos_data = fetch_alunos()
        if isinstance(alunos_data, dict) and 'error' in alunos_data:
            alunos_data = []
        return render_template('alunos.html', alunos=alunos_data, edit_aluno=None, is_edit=False,
                               error='Por favor preencha todos os campos corretamente.')
    result = criar_aluno(aluno_data)
    if isinstance(result, dict) and 'error' in result:
        alunos_data = fetch_alunos()
        if isinstance(alunos_data, dict) and 'error' in alunos_data:
            alunos_data = []
        return render_template('alunos.html', alunos=alunos_data, edit_aluno=None, is_edit=False, error=result['error'])
    return redirect(url_for('alunos'))


@app.route('/alunos/editar/<aluno_id>', methods=['POST'])
def salvar_edicao_aluno(aluno_id):
    aluno_data = parse_aluno_form(request.form)
    if not aluno_data['nome'] or not aluno_data['email'] or not aluno_data['curso']:
        alunos_data = fetch_alunos()
        if isinstance(alunos_data, dict) and 'error' in alunos_data:
            alunos_data = []
        return render_template('alunos.html', alunos=alunos_data, edit_aluno=aluno_data, is_edit=True,
                               error='Por favor preencha todos os campos corretamente.')
    result = atualizar_aluno(aluno_id, aluno_data)
    if isinstance(result, dict) and 'error' in result:
        alunos_data = fetch_alunos()
        if isinstance(alunos_data, dict) and 'error' in alunos_data:
            alunos_data = []
        return render_template('alunos.html', alunos=alunos_data, edit_aluno=aluno_data, is_edit=True, error=result['error'])
    return redirect(url_for('alunos'))


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
