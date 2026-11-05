"""Geração do relatório técnico em PDF (ReportLab)."""
import io, datetime
from .matematica import decompose, verify, terms, run_tests, table_2n


def build_pdf(p, q, N):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    NAVY, ELEC, CLASSIC, TURQ, GOLD = (colors.HexColor(c) for c in
        ("#0A1F44", "#1F51FF", "#0F4C81", "#30D5C8", "#D4AF37"))
    S = lambda n, **k: ParagraphStyle(n, fontName=k.pop("f", "Helvetica"), **k)
    body = S("b", fontSize=10, leading=14.5, textColor=NAVY, spaceAfter=6)
    h1 = S("h1", f="Helvetica-Bold", fontSize=16, leading=20, textColor=CLASSIC, spaceBefore=12, spaceAfter=6)
    h2 = S("h2", f="Helvetica-Bold", fontSize=12, leading=15, textColor=ELEC, spaceBefore=8, spaceAfter=4)
    cell = S("c", fontSize=7.5, leading=9.5, textColor=NAVY)
    cellh = S("ch", f="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white)
    box = S("bx", fontSize=10, leading=14.5, textColor=NAVY, backColor=colors.HexColor("#E8FBF9"),
            borderColor=TURQ, borderWidth=1, borderPadding=7, spaceBefore=6, spaceAfter=12)
    MAP = {"⌈": "ceil(", "⌉": ")", "⌊": "floor(", "⌋": ")", "≤": "&lt;=", "≥": "&gt;=", "→": "->", "∈": "em",
           "∎": "(c.q.d.)", "−": "-", "√": "raiz de ", "π": "pi"}                     # Helvetica não tem estes glifos
    def fx(t):
        for a, b in MAP.items(): t = t.replace(a, b)
        return t
    P = lambda t, s=body: Paragraph(fx(t), s)
    W = A4[0] - 4 * cm

    def tbl(rows, widths):
        data = [[Paragraph(fx(str(c)), cellh) for c in rows[0]]] + [[Paragraph(fx(str(c)), cell) for c in r] for r in rows[1:]]
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("LINEBELOW", (0, 0), (-1, 0), 2, GOLD),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF4FB")]),
            ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#9DB4D0")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        return t

    def steps_table(a, b):
        st = decompose(a, b)
        rows = [["Passo", "Fração atual", "k = ceil(q/p)", "1/k", "Resto = (pk − q)/(qk)", "Resto simplificado"]]
        for i, s in enumerate(st, 1):
            rows.append([i, f"{s['p']}/{s['q']}", f"ceil({s['q']}/{s['p']}) = {s['k']}", f"1/{s['k']}",
                         f"{s['p1']}/{s['q1']}", f"{s['rest']}" if s["p1"] else "0 (acabou)"])
        return st, tbl(rows, [1.4*cm, 2.5*cm, 3.2*cm, 2.1*cm, 4.1*cm, W - 13.3*cm])

    def footer(c, d):
        c.saveState(); c.setFillColor(NAVY); c.rect(0, 0, A4[0], 1.1*cm, fill=1, stroke=0)
        c.setFillColor(GOLD); c.rect(0, 1.1*cm, A4[0], .08*cm, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica", 8)
        c.drawString(2*cm, .42*cm, "Frações Egípcias - Relatório técnico"); c.drawRightString(A4[0]-2*cm, .42*cm, f"Página {d.page}")
        c.restoreState()

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm,
                            title="Relatório - Frações Egípcias", author="Programa Frações Egípcias")
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    cover = Table([[P("RELATÓRIO TÉCNICO", S("k", f="Helvetica-Bold", fontSize=10, textColor=TURQ))],
                   [P("Frações Egípcias", S("t", f="Helvetica-Bold", fontSize=34, leading=38, textColor=colors.white))],
                   [P("Proposição 12 e o algoritmo voraz de Fibonacci-Sylvester: pesquisa, demonstração, implementação e testes",
                      S("s", fontSize=13, leading=17, textColor=colors.white))],
                   [P(f"Gerado em {now}", S("d", fontSize=9, textColor=GOLD))]], colWidths=[W])
    cover.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 20),
                               ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                               ("LINEBELOW", (0, -1), (-1, -1), 5, GOLD)]))
    E = [cover, Spacer(1, 14)]

    E += [P("1. Objetivo e resumo", h1),
          P("Este relatório documenta o estudo da seção <b>1.2.6 - Frações egípcias</b> (imagens fornecidas): "
            "<i>Definições 10, 11 e 12</i>, o <i>Exemplo 16</i> e a <i>Proposição 12</i>, segundo a qual <b>toda fração racional p/q, com "
            "0 &lt; p &lt; q inteiros, é soma de frações unitárias distintas</b>. O trabalho consistiu em (a) formalizar o enunciado, "
            "(b) entender e reescrever a demonstração por indução, (c) implementar o algoritmo em Python, (d) verificar computacionalmente "
            "cada passo da prova e (e) construir uma interface web (modo claro/escuro) que demonstra, testa e explica o resultado."),
          P(f"<b>Resultado principal:</b> o algoritmo voraz decompôs corretamente <b>todas</b> as frações irredutíveis com denominador até {N} "
            "(detalhes na seção 6), confirmando a Proposição 12 e cada desigualdade usada na prova.", box)]

    E += [P("2. Definições estudadas", h1),
          P("<b>Definição 10 - Fração unitária:</b> fração da forma 1/n, com n inteiro positivo."),
          P("<b>Definição 11 - Fração egípcia:</b> soma de frações unitárias <i>distintas</i>. Exemplos do texto: 11/12 = 1/2 + 1/4 + 1/6 e "
            "5/17 = 1/4 + 1/23 + 1/1564. Os egípcios (papiro de Rhind, c. 1650 a.C.) tabelaram 2/n para n ímpar de 5 a 101; "
            "a única fração para a qual não usavam unitárias era 2/3."),
          P("<b>Definição 12 - Piso, teto e parte fracionária:</b> ⌊x⌋ é o único inteiro k com k ≤ x &lt; k+1; ⌈x⌉ é o único inteiro k com "
            "k−1 &lt; x ≤ k; {x} = x − ⌊x⌋ ∈ [0,1). Ex.: ⌊√2⌋=1, ⌈√2⌉=2, ⌊−π⌋=−4, ⌈−π⌉=−3. "
            "Em Python, o teto de a/b com inteiros é calculado sem erro de ponto flutuante por <font face='Courier'>-(-a // b)</font>.")]

    E += [P("3. O algoritmo voraz (método de Fibonacci-Sylvester)", h1),
          P("Dada p/q com 0 &lt; p &lt; q: <b>(1)</b> calcule k = ⌈q/p⌉, isto é, o menor k tal que 1/k ≤ p/q; <b>(2)</b> subtraia a maior "
            "unitária possível: p/q − 1/k = (pk − q)/(qk); <b>(3)</b> se o resto for 0, termine; <b>(4)</b> senão repita com o resto (simplificado). "
            "Cada resto é um novo problema da mesma natureza, porém com numerador estritamente menor - é isso que garante o término."),
          P("Exemplo 16 (5/7): ⌈7/5⌉ = 2 → 5/7 − 1/2 = 3/14; ⌈14/3⌉ = 5 → 3/14 − 1/5 = 1/70. Logo <b>5/7 = 1/2 + 1/5 + 1/70</b>.")]

    E += [P("4. Demonstração da Proposição 12 (indução forte no numerador)", h1),
          P("<b>Hipótese:</b> o resultado vale para toda fração de numerador menor que p. <b>Passo:</b> seja k = ⌈q/p⌉. Como k−1 &lt; q/p ≤ k, "
            "tem-se 1/k ≤ p/q &lt; 1/(k−1). (Como p &lt; q, q/p &gt; 1 e portanto k ≥ 2.)"),
          P("<b>Caso (i) 1/k = p/q:</b> a própria fração é unitária; acabou.", body),
          P("<b>Caso (ii) 1/k &lt; p/q &lt; 1/(k−1):</b> defina p/q = 1/k + p1/q1, com p1 = pk − q e q1 = qk. "
            "<b>Afirmação 1 - p1 &lt; p:</b> de k−1 &lt; q/p obtém-se p(k−1) &lt; q, ou seja pk − q &lt; p. "
            "<b>Afirmação 2 - p1 &gt; 0 e p1 &lt; q1:</b> p1 &gt; 0 porque 1/k &lt; p/q; e p1 &lt; p &lt; q &lt; qk = q1. "
            "Pela hipótese de indução, p1/q1 é soma de unitárias distintas. <b>Afirmação 3 - essas unitárias são todas menores que 1/k:</b> "
            "cada uma é ≤ p1/q1 = p/q − 1/k &lt; 1/(k−1) − 1/k = 1/(k(k−1)) ≤ 1/k, e portanto diferente de 1/k. "
            "Somando 1/k a elas obtém-se uma soma de unitárias distintas igual a p/q. ∎"),
          P("<b>Observação sobre o texto original:</b> na imagem 2 a cadeia de igualdades aparece como p1 = pk − p = pq − p + p − q &lt; ...; "
            "parece haver uma gralha de digitação. O cálculo correto é p1 = pk − q, e a desigualdade p1 &lt; p decorre de p(k−1) &lt; q, "
            "como mostrado acima. O programa verifica numericamente essa desigualdade em todos os passos de todos os testes.", box)]

    E += [PageBreak(), P("5. Demonstrações numéricas passo a passo", h1)]
    for a, b in [(5, 7), (11, 12), (5, 17)] + ([(p, q)] if (p, q) not in [(5, 7), (11, 12), (5, 17)] else []):
        st, t = steps_table(a, b)
        tag = " (escolhida pelo usuário)" if (a, b) == (p, q) else ""
        E += [P(f"{a}/{b}{tag} = {terms(st)}", h2), t, Spacer(1, 4),
              P(f"{len(st)} termo(s); o numerador cai a cada passo: " + " → ".join(str(s["p"]) for s in st) + " → 0.")]
        ck = verify(a, b, st)
        E += [P("Verificações: " + "; ".join(f"{'OK' if v else 'FALHOU'} - {k}" for k, v in ck.items()) + ".")]

    r = run_tests(N)
    E += [PageBreak(), P(f"6. Testes computacionais (todas as frações irredutíveis p/q, 0 &lt; p &lt; q ≤ {N})", h1),
          P("Frações não irredutíveis equivalem a uma irredutível, logo bastam as irredutíveis. Para cada uma, o programa executa o algoritmo "
            "e confere 6 propriedades (soma exata com <font face='Courier'>fractions.Fraction</font>, denominadores distintos, desigualdades "
            "1/k ≤ p/q &lt; 1/(k−1), p1 &lt; p, resto &lt; 1/k, nº de termos ≤ p)."),
          tbl([["Indicador", "Resultado"], ["Frações testadas", r["total"]], ["Aprovadas em todas as verificações", r["ok"]],
               ["Falhas", len(r["fails"]) and ", ".join(r["fails"]) or "0"],
               ["Maior nº de termos", f"{r['maxterms'][0]} (em {r['maxterms'][1]}/{r['maxterms'][2]})"],
               ["Maior denominador (nº de dígitos)", f"{r['maxdigits'][0]} dígitos (em {r['maxdigits'][1]}/{r['maxdigits'][2]})"]],
              [7*cm, W - 7*cm]), Spacer(1, 8), P("Distribuição do número de termos:", h2),
          tbl([["Nº de termos"] + list(map(str, r["hist"])), ["Frações"] + list(map(str, r["hist"].values()))],
              [3*cm] + [(W - 3*cm) / len(r["hist"])] * len(r["hist"]))]

    t2 = table_2n(); half = (len(t2) + 1) // 2
    rows = [["n", "2/n pelo algoritmo voraz", "n", "2/n pelo algoritmo voraz"]]
    for i in range(half):
        a = t2[i]; b = t2[i + half] if i + half < len(t2) else ("", "")
        rows.append([a[0], a[1], b[0], b[1]])
    E += [P("7. Tabela 2/n (n ímpar de 5 a 101) - análoga à do papiro de Rhind", h1),
          P("A tabela abaixo é gerada pelo algoritmo voraz. Ela pode diferir da tabela egípcia original, que usava outras escolhas (frequentemente "
            "denominadores menores e mais 'práticos'); ambas são decomposições válidas."),
          tbl(rows, [1*cm, (W - 2*cm) / 2, 1*cm, (W - 2*cm) / 2])]

    E += [P("8. Observações e limitações", h1),
          P("• A decomposição de uma fração <b>não é única</b>; o algoritmo voraz dá uma delas, nem sempre a mais curta nem a de menores denominadores.<br/>"
            f"• Os denominadores podem crescer muito rápido (nos testes até {r['maxdigits'][0]} dígitos para q ≤ {N}), por isso o programa usa inteiros de "
            "precisão arbitrária e envia números como texto à interface (JavaScript perderia precisão).<br/>"
            "• O limite p ≥ número de termos mostra a terminação: o numerador estritamente decrescente leva a 0 em no máximo p passos.<br/>"
            "• Teste não substitui prova: a demonstração da seção 4 vale para todo p/q; os testes confirmam a implementação e a prova em casos concretos."),
          P("9. Como o trabalho foi feito (metodologia)", h1),
          P("<b>1) Leitura:</b> transcrição das duas imagens (definições, exemplos, proposição e prova). <b>2) Formalização:</b> tradução da prova em "
            "afirmações verificáveis (seção 4). <b>3) Implementação:</b> função <font face='Courier'>decompose</font> e <font face='Courier'>verify</font> "
            "em Python, com <font face='Courier'>Fraction</font> para aritmética exata. <b>4) Testes:</b> varredura exaustiva até q ≤ N e comparação com os "
            "exemplos do livro (5/7, 11/12, 5/17). <b>5) Interface:</b> aplicação Flask com páginas Explicar, Demonstrar, Testar e Relatório; paleta azul-marinho, "
            "azul elétrico, azul clássico, turquesa, dourado e branco; temas claro/escuro. <b>6) Relatório:</b> este PDF é gerado com ReportLab a partir "
            "dos mesmos cálculos exibidos na tela, portanto sempre consistente com eles."),
          P("10. Conclusão", h1),
          P("A Proposição 12 foi demonstrada por indução forte sobre o numerador, com o passo-chave p1 = pk − q &lt; p, e confirmada computacionalmente "
            f"em {r['total']} frações. O algoritmo voraz é simples, correto e termina em no máximo p passos.")]
    doc.build(E, onFirstPage=footer, onLaterPages=footer)
    buf.seek(0); return buf
