"""
Seed script — dados fictícios para a Plataforma de Ensino
=========================================================
Como executar (a partir da pasta raiz do projeto):

    python seed/seed.py

O script é idempotente: se os cursos já existirem (mesmo nome),
eles não serão duplicados.
"""

import os
import sys
import django

# Garante que o manage.py está no path independente de onde o script é chamado
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plataforma_ensino.settings")
django.setup()

from courses.models import Aula, Curso, Modulo  # noqa: E402 (import após setup)

# ---------------------------------------------------------------------------
# Dados dos cursos
# ---------------------------------------------------------------------------

CURSOS = [
    {
        "nome": "Python para Iniciantes",
        "carga_horaria": 40,
        "modulos": [
            {
                "nome": "Primeiros Passos com Python",
                "aulas": [
                    ("Instalação e configuração do ambiente", 20),
                    ("Variáveis, tipos e operadores", 35),
                    ("Entrada e saída de dados", 25),
                    ("Condicionais: if, elif e else", 30),
                ],
            },
            {
                "nome": "Estruturas de Repetição",
                "aulas": [
                    ("Loop for e range()", 30),
                    ("Loop while e controle de fluxo", 30),
                    ("List comprehensions", 25),
                    ("Exercícios práticos de repetição", 40),
                ],
            },
            {
                "nome": "Estruturas de Dados",
                "aulas": [
                    ("Listas: criação e manipulação", 35),
                    ("Tuplas e sets", 25),
                    ("Dicionários", 35),
                    ("Quando usar cada estrutura", 20),
                ],
            },
            {
                "nome": "Funções e Módulos",
                "aulas": [
                    ("Definindo e chamando funções", 30),
                    ("Parâmetros, *args e **kwargs", 35),
                    ("Escopo de variáveis", 20),
                    ("Importando e criando módulos", 30),
                ],
            },
        ],
    },
    {
        "nome": "Desenvolvimento Web com Django",
        "carga_horaria": 60,
        "modulos": [
            {
                "nome": "Configurando o Projeto",
                "aulas": [
                    ("Instalando Django e criando o projeto", 20),
                    ("Estrutura de diretórios do Django", 25),
                    ("Settings, INSTALLED_APPS e banco de dados", 30),
                ],
            },
            {
                "nome": "Models e ORM",
                "aulas": [
                    ("Criando models e campos", 40),
                    ("Migrations: makemigrations e migrate", 25),
                    ("QuerySets e operações CRUD", 45),
                    ("Relacionamentos ForeignKey e ManyToMany", 40),
                ],
            },
            {
                "nome": "Views e URLs",
                "aulas": [
                    ("Function-based views (FBVs)", 35),
                    ("Mapeando URLs com path() e include()", 25),
                    ("Context e passagem de dados para templates", 30),
                    ("Class-based views (CBVs) essenciais", 40),
                ],
            },
            {
                "nome": "Templates e Formulários",
                "aulas": [
                    ("Template language: tags e filtros", 35),
                    ("Herança de templates com {% block %}", 30),
                    ("Criando e validando Forms", 40),
                    ("ModelForms e salvando dados", 35),
                ],
            },
            {
                "nome": "Autenticação e Deploy",
                "aulas": [
                    ("Sistema de login e logout nativo", 30),
                    ("Protegendo views com @login_required", 20),
                    ("Preparando para produção (DEBUG, ALLOWED_HOSTS)", 30),
                    ("Deploy básico com Gunicorn e Nginx", 45),
                ],
            },
        ],
    },
    {
        "nome": "JavaScript Moderno (ES6+)",
        "carga_horaria": 35,
        "modulos": [
            {
                "nome": "Fundamentos do JavaScript",
                "aulas": [
                    ("Variáveis: var, let e const", 20),
                    ("Tipos primitivos e coerção de tipos", 25),
                    ("Funções tradicionais vs arrow functions", 30),
                    ("Arrays e métodos essenciais", 35),
                ],
            },
            {
                "nome": "ES6+ na Prática",
                "aulas": [
                    ("Destructuring de objetos e arrays", 25),
                    ("Spread operator e rest params", 20),
                    ("Template literals", 15),
                    ("Promises e async/await", 45),
                    ("Módulos: import e export", 25),
                ],
            },
            {
                "nome": "DOM e Eventos",
                "aulas": [
                    ("Selecionando e manipulando elementos", 30),
                    ("Eventos: addEventListener e event delegation", 35),
                    ("Fetch API e consumo de JSON", 40),
                ],
            },
        ],
    },
    {
        "nome": "Banco de Dados com PostgreSQL",
        "carga_horaria": 25,
        "modulos": [
            {
                "nome": "Introdução ao SQL",
                "aulas": [
                    ("Instalação e ferramentas (psql, DBeaver)", 20),
                    ("CREATE TABLE, tipos de dados e constraints", 35),
                    ("INSERT, SELECT, UPDATE e DELETE", 40),
                    ("Filtros com WHERE e ordenação com ORDER BY", 25),
                ],
            },
            {
                "nome": "Consultas Avançadas",
                "aulas": [
                    ("JOINs: INNER, LEFT, RIGHT e FULL", 45),
                    ("Agregações: COUNT, SUM, AVG, GROUP BY", 35),
                    ("Subqueries e CTEs (WITH)", 40),
                    ("Índices e otimização de consultas", 30),
                ],
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Funções de seed
# ---------------------------------------------------------------------------


def seed():
    criados = 0
    ignorados = 0

    for dados_curso in CURSOS:
        curso, novo = Curso.objects.get_or_create(
            nome=dados_curso["nome"],
            defaults={"carga_horaria": dados_curso["carga_horaria"]},
        )

        if not novo:
            print(f"  [ignorado] Curso já existe: {curso.nome}")
            ignorados += 1
            continue

        for ordem_modulo, dados_modulo in enumerate(dados_curso["modulos"], start=1):
            modulo = Modulo.objects.create(
                curso=curso,
                nome=dados_modulo["nome"],
                ordem=ordem_modulo,
            )

            for ordem_aula, (titulo, duracao) in enumerate(dados_modulo["aulas"], start=1):
                Aula.objects.create(
                    modulo=modulo,
                    titulo=titulo,
                    duracao=duracao,
                    ordem=ordem_aula,
                    conteudo="",
                )

        total_modulos = len(dados_curso["modulos"])
        total_aulas = sum(len(m["aulas"]) for m in dados_curso["modulos"])
        print(f"  [criado]  {curso.nome} — {total_modulos} módulos, {total_aulas} aulas")
        criados += 1

    print(f"\nConcluído: {criados} curso(s) criado(s), {ignorados} ignorado(s).")


if __name__ == "__main__":
    print("Populando banco de dados com dados fictícios...\n")
    seed()
