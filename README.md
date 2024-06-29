
# Sistema de Agendamento e Cadastro de Vacinas

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

* [Introdução](#introdução)
* [Instalação de Dependências](#instalação-de-dependências)
* [Estrutura do Código](#estrutura-do-código)
* [Importações](#importações)
* [Variáveis](#variáveis)
* [Funções](#funções)
* [Rotas da Aplicação](#rotas-da-aplicação)
* [Execução da Aplicação](#execução-da-aplicação)
* [Conclusão](#conclusão)

# Introdução

O projeto Sistema de Agendamento e Cadastro de Vacinas foi desenvolvido para facilitar a administração de vacinas, permitindo o cadastro de vacinas, pacientes, unidades de saúde e agendamentos. O sistema também inclui um chatbot para responder perguntas frequentes dos usuários.

# Instalação de Dependências

> pip install -r requirements.txt

# Estrutura do Código

O código está organizado da seguinte forma:

- `app.py`: Contém a aplicação Flask e define as rotas e modelos do banco de dados.
- `chatbot.py`: Define o chatbot e suas respostas.

## Importações

- `datetime`: Para manipulação de datas e horários.
- `Flask`: Biblioteca principal do Flask para criação de aplicações web.
- `jsonify`, `redirect`, `render_template`, `request`, `url_for`: Funções do Flask para manipulação de respostas JSON, redirecionamentos, renderização de templates, manipulação de requisições e geração de URLs.
- `SQLAlchemy`: ORM para manipulação do banco de dados.
- `chatbot`: Importação do chatbot definido em `chatbot.py`.

## Variáveis

- `app`: Instância da aplicação Flask.
- `db`: Instância do SQLAlchemy para manipulação do banco de dados.

## Funções

### Chatbot

- `get_response(user_input)`: Retorna a resposta do chatbot com base na entrada do usuário, utilizando correspondência aproximada para tolerar erros de escrita.

### Rotas da Aplicação

- `/`: Rota principal que renderiza a página inicial.
- `/chat`: Rota para interação com o chatbot, recebendo mensagens do usuário e retornando respostas.
- `/cadastro_vacina`: Rota para cadastro de novas vacinas.
- `/cadastro_paciente`: Rota para cadastro de novos pacientes.
- `/cadastro_unidade`: Rota para cadastro de novas unidades de saúde.
- `/agendamento`: Rota para agendamento de vacinas.
- `/registros`: Rota que exibe todos os agendamentos registrados.
- `/relatorios`: Rota que gera e exibe relatórios detalhados sobre os agendamentos de vacinas.

# Execução da Aplicação

> python app.py

A aplicação será executada em `http://0.0.0.0:8080` com o modo de debug ativado.

# Conclusão

O Sistema de Agendamento e Cadastro de Vacinas oferece uma solução prática e eficiente para o gerenciamento de vacinas, pacientes e agendamentos. A integração com um chatbot melhora a interatividade e a acessibilidade do sistema. Futuras melhorias podem incluir a integração com sistemas de saúde maiores e a adição de novas funcionalidades baseadas no feedback dos usuários.
Link para acessar o código: `https://projeto-integrado-unidombosco-1.onrender.com/`
