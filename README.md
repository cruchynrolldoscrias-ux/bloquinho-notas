# Sistema de Anotações Científicas

Um aplicativo web desenvolvido em Flask para organização e gerenciamento de anotações de pesquisa científica. O sistema permite estruturar notas com campos específicos para metodologia, resultados, fórmulas e referências, facilitando o trabalho de pesquisadores e estudantes.

## Visão Geral

Este projeto nasceu da necessidade de uma ferramenta mais focada em anotações científicas, contrastando com aplicativos de notas genéricos. A interface foi projetada para ser limpa e funcional, priorizando a organização do conteúdo acadêmico.

### Características Principais

- **Organização Estruturada**: Sistema de categorias científicas pré-definidas e personalizáveis
- **Campos Especializados**: Metodologia, resultados, fórmulas e referências integrados em cada nota
- **Interface Limpa**: Design responsivo com TailwindCSS, focado na experiência do usuário
- **Flexibilidade de Conteúdo**: Suporte a Markdown para formatação rica de texto
- **Sistema de Favoritos**: Acesso rápido às anotações mais importantes
- **Análise Automática**: Contagem de palavras e cálculo de tempo estimado de leitura

## Tecnologias

### Backend
- **Flask** - Framework web em Python
- **JSON** - Armazenamento de dados local
- **Markdown** - Processamento de texto formatado

### Frontend
- **TailwindCSS** - Framework CSS para interface responsiva
- **JavaScript ES6** - Interatividade e animações
- **Font Awesome** - Ícones da interface
- **Jinja2** - Template engine

### Ferramentas de Desenvolvimento
- **Gunicorn** - Servidor WSGI para produção
- **Werkzeug** - Biblioteca de utilitários Flask

## Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/RyanMarcelinos/bloquinho-notas.git
cd bloquinho-notas
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo:
```bash
python app.py
```

O sistema estará disponível em `http://localhost:5000`

### Deploy em Produção

Para deploy, utilize Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Estrutura do Projeto

```
bloquinho-notas/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   └── notas/            # Templates de anotações
├── static/               # Arquivos estáticos
│   ├── css/             # Folhas de estilo
│   └── js/              # Scripts JavaScript
└── geral/               # Dados da aplicação
    ├── Notas/           # Anotações em JSON
    └── Categorias/      # Categorias científicas
```

## Como Usar

### Criando Anotações

1. Acesse a página inicial
2. Clique em "Nova Anotação"
3. Preencha os campos desejados:
   - **Título**: Nome da anotação
   - **Conteúdo**: Texto principal com suporte a Markdown
   - **Metodologia**: Procedimentos utilizados
   - **Resultados**: Resultados obtidos
   - **Fórmulas**: Expressões matemáticas
   - **Referências**: Fontes e citações
   - **Categoria**: Classificação científica
   - **Tags**: Palavras-chave
   - **Favorito**: Marcar para acesso rápido

### Organizando Anotações

- **Busca**: Use a barra de pesquisa para encontrar anotações específicas
- **Filtros**: Filtre por categoria, status de favorito ou data
- **Ordenação**: Organize por data de criação, modificação ou título
- **Categorias**: Sistema flexível com categorias pré-definidas e personalizáveis

### Campos de Análise

O sistema calcula automaticamente:
- Contagem total de palavras
- Tempo estimado de leitura (baseado em 200 palavras/minuto)
- Estatísticas por categoria

## Características Técnicas

### Armazenamento
- Dados salvos localmente em arquivos JSON
- Estrutura de arquivos por timestamp para evitar conflitos
- Backup automático através da estrutura de arquivos

### Performance
- Carregamento lazy das anotações
- Paginação automática para grandes volumes
- Cache de categorias para melhor responsividade

### Segurança
- Validação de entrada para todos os formulários
- Sanitização de conteúdo Markdown
- Verificação de tipos de arquivo para uploads

## API Endpoints

O sistema expõe alguns endpoints para integração:

- `GET /` - Página principal
- `GET /nota/criar` - Formulário de nova anotação
- `POST /nota/criar` - Criar anotação
- `GET /nota/editar/<id>` - Editar anotação existente
- `POST /nota/editar/<id>` - Salvar alterações
- `GET /nota/<id>` - Visualizar anotação
- `POST /nota/deletar/<id>` - Deletar anotação
- `POST /nota/favorito/<id>` - Toggle favorito
- `GET /api/notas` - API: listar todas as anotações
- `GET /api/categorias` - API: listar categorias
- `POST /api/categorias` - API: adicionar categoria
- `GET /api/estatisticas` - API: estatísticas gerais

## Contribuindo

Contribuições são bem-vindas! Para sugerir melhorias:

1. Abra uma issue descrevendo a funcionalidade desejada
2. Fork o projeto
3. Crie uma branch para sua feature
4. Submeta um pull request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

Desenvolvido por Ryan Marcelinos como uma solução personalizada para organização de anotações científicas.

---

**Nota**: Este projeto foi desenvolvido como uma solução acadêmica e está em constante evolução. Sugestões e feedback são sempre bem-vindos.
