from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
from datetime import datetime
import markdown
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTAS_DIR = os.path.join(BASE_DIR, 'geral', 'Notas')
CATEGORIAS_DIR = os.path.join(BASE_DIR, 'geral', 'Categorias')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

# Garantir que os diretórios existam
os.makedirs(NOTAS_DIR, exist_ok=True)
os.makedirs(CATEGORIAS_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def contar_palavras(texto):
    return len(texto.split()) if texto else 0

def salvar_nota(dados):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"nota_{timestamp}.json"
    caminho_arquivo = os.path.join(NOTAS_DIR, nome_arquivo)
    
    dados['id'] = nome_arquivo.replace('.json', '')
    dados['data_criacao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
    dados['data_modificacao'] = dados['data_criacao']
    dados['palavras'] = contar_palavras(dados.get('conteudo', '')) + contar_palavras(dados.get('metodologia', ''))
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    return nome_arquivo

def carregar_notas():
    notas = []
    for arquivo in os.listdir(NOTAS_DIR):
        if arquivo.endswith('.json'):
            caminho = os.path.join(NOTAS_DIR, arquivo)
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    nota = json.load(f)
                    nota['id'] = arquivo.replace('.json', '')
                    # Garantir campos essenciais
                    nota.setdefault('favorita', False)
                    nota.setdefault('tags', [])
                    nota.setdefault('palavras', 0)
                    notas.append(nota)
            except Exception as e:
                print(f"Erro ao carregar nota {arquivo}: {e}")
    
    # Ordenar por data de criação (mais recente primeiro)
    return sorted(notas, key=lambda x: x.get('data_criacao', ''), reverse=True)

def carregar_nota(nota_id):
    caminho = os.path.join(NOTAS_DIR, f"{nota_id}.json")
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def atualizar_nota(nota_id, dados):
    caminho = os.path.join(NOTAS_DIR, f"{nota_id}.json")
    if os.path.exists(caminho):
        dados['data_modificacao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        dados['palavras'] = contar_palavras(dados.get('conteudo', '')) + contar_palavras(dados.get('metodologia', ''))
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    return False

def deletar_nota(nota_id):
    caminho = os.path.join(NOTAS_DIR, f"{nota_id}.json")
    if os.path.exists(caminho):
        os.remove(caminho)
        return True
    return False

def salvar_categorias(categorias):
    caminho = os.path.join(CATEGORIAS_DIR, 'categorias.json')
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(categorias, f, ensure_ascii=False, indent=2)

def carregar_categorias():
    caminho = os.path.join(CATEGORIAS_DIR, 'categorias.json')
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Categorias padrão para pesquisa científica
    categorias_padrao = [
        "Bioquímica", "Metodologia", "Neurociência", "Estatística", 
        "Laboratório", "Genética", "Farmacologia", "Imunologia",
        "Bioinformática", "Epidemiologia", "Biologia Molecular"
    ]
    salvar_categorias(categorias_padrao)
    return categorias_padrao

def toggle_favorito(nota_id):
    nota = carregar_nota(nota_id)
    if nota:
        nota['favorita'] = not nota.get('favorita', False)
        atualizar_nota(nota_id, nota)
        return True
    return False

@app.route('/')
def index():
    notas = carregar_notas()
    categorias = carregar_categorias()
    return render_template('index.html', notas=notas, categorias=categorias)

@app.route('/nota/criar', methods=['GET', 'POST'])
def criar_nota():
    if request.method == 'POST':
        try:
            dados = {
                'titulo': request.form.get('titulo', '').strip(),
                'metodologia': request.form.get('metodologia', '').strip(),
                'resultados': request.form.get('resultados', '').strip(),
                'formulas': request.form.get('formulas', '').strip(),
                'referencias': request.form.get('referencias', '').strip(),
                'nivel': request.form.get('nivel', ''),
                'conteudo': request.form.get('conteudo', '').strip(),
                'tags': [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()],
                'categoria': request.form.get('categoria', ''),
                'favorita': request.form.get('favorita') == 'on',
                'tipo_pesquisa': request.form.get('tipo_pesquisa', '')
            }
            
            if not dados['titulo']:
                flash('O título é obrigatório!', 'error')
                return render_template('notas/criar.html', categorias=carregar_categorias(), dados=dados)
            
            salvar_nota(dados)
            flash('Anotação criada com sucesso!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Erro ao criar anotação: {str(e)}', 'error')
    
    categorias = carregar_categorias()
    return render_template('notas/criar.html', categorias=categorias)

@app.route('/nota/editar/<nota_id>', methods=['GET', 'POST'])
def editar_nota(nota_id):
    nota = carregar_nota(nota_id)
    if not nota:
        flash('Nota não encontrada!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            dados = {
                'titulo': request.form.get('titulo', '').strip(),
                'metodologia': request.form.get('metodologia', '').strip(),
                'resultados': request.form.get('resultados', '').strip(),
                'formulas': request.form.get('formulas', '').strip(),
                'referencias': request.form.get('referencias', '').strip(),
                'nivel': request.form.get('nivel', ''),
                'conteudo': request.form.get('conteudo', '').strip(),
                'tags': [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()],
                'categoria': request.form.get('categoria', ''),
                'favorita': request.form.get('favorita') == 'on',
                'tipo_pesquisa': request.form.get('tipo_pesquisa', '')
            }
            
            if not dados['titulo']:
                flash('O título é obrigatório!', 'error')
                return render_template('notas/editar.html', nota=nota, categorias=carregar_categorias())
            
            if atualizar_nota(nota_id, dados):
                flash('Anotação atualizada com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Erro ao atualizar anotação!', 'error')
                
        except Exception as e:
            flash(f'Erro ao atualizar anotação: {str(e)}', 'error')
    
    categorias = carregar_categorias()
    return render_template('notas/editar.html', nota=nota, categorias=categorias)

@app.route('/nota/deletar/<nota_id>', methods=['POST'])
def deletar_nota_route(nota_id):
    if deletar_nota(nota_id):
        return jsonify({'success': True, 'message': 'Nota deletada com sucesso!'})
    return jsonify({'success': False, 'message': 'Nota não encontrada!'}), 404

@app.route('/nota/favorito/<nota_id>', methods=['POST'])
def toggle_favorito_route(nota_id):
    if toggle_favorito(nota_id):
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/nota/<nota_id>')
def ver_nota(nota_id):
    nota = carregar_nota(nota_id)
    if not nota:
        flash('Nota não encontrada!', 'error')
        return redirect(url_for('index'))
    
    # Converter markdown para HTML se necessário
    if 'conteudo' in nota and nota['conteudo']:
        try:
            nota['conteudo_html'] = markdown.markdown(nota['conteudo'])
        except:
            nota['conteudo_html'] = nota['conteudo']
    
    return render_template('notas/ver.html', nota=nota)

@app.route('/api/notas', methods=['GET'])
def api_notas():
    notas = carregar_notas()
    return jsonify(notas)

@app.route('/api/categorias', methods=['GET', 'POST'])
def api_categorias():
    if request.method == 'POST':
        nova_categoria = request.json.get('categoria', '').strip()
        if nova_categoria:
            categorias = carregar_categorias()
            if nova_categoria not in categorias:
                categorias.append(nova_categoria)
                salvar_categorias(categorias)
                return jsonify({'success': True, 'message': 'Categoria adicionada!'})
            return jsonify({'success': False, 'message': 'Categoria já existe!'})
    
    categorias = carregar_categorias()
    return jsonify(categorias)

@app.route('/api/estatisticas')
def api_estatisticas():
    notas = carregar_notas()
    total_notas = len(notas)
    total_favoritas = sum(1 for nota in notas if nota.get('favorita', False))
    total_palavras = sum(nota.get('palavras', 0) for nota in notas)
    
    categorias_count = {}
    for nota in notas:
        categoria = nota.get('categoria', 'Sem Categoria')
        categorias_count[categoria] = categorias_count.get(categoria, 0) + 1
    
    return jsonify({
        'total_notas': total_notas,
        'total_favoritas': total_favoritas,
        'total_palavras': total_palavras,
        'categorias': categorias_count
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)