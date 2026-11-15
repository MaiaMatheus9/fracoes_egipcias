# Frações Egípcias

Demonstra, testa e explica a Proposição 12 (toda p/q com 0 < p < q é soma de frações unitárias distintas)
e gera um relatório técnico em PDF.

## Executar
    pip install -r requirements.txt
    python app.py        # abre em http://localhost:5000

## Estrutura
    app.py                  ponto de entrada
    egipcias/
      __init__.py           fábrica da aplicação Flask (create_app)
      matematica.py         algoritmo voraz, verificações, testes em lote, tabela 2/n
      rotas.py              página, API JSON (/api/decompose, /api/test) e /relatorio.pdf
      relatorio.py          construção do PDF com ReportLab
    templates/index.html    estrutura da página
    static/css/style.css    paleta azul-marinho/elétrico/clássico, turquesa, dourado, branco + temas claro/escuro
    static/js/app.js        abas, tema, chamadas à API e renderização dos passos

## Exemplo de fração egípcia

Uma fração egípcia representa uma fração positiva como soma de
frações unitárias distintas, ou seja, com numerador igual a 1.

Por exemplo:

5/7 = 1/2 + 1/5 + 1/70

Conferindo com denominador comum:

35/70 + 14/70 + 1/70 = 50/70 = 5/7.
