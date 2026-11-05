"""Rotas HTTP: página, API JSON e download do PDF."""
from flask import Blueprint, jsonify, request, send_file, render_template
from .matematica import decompose, verify, terms, run_tests, table_2n, parse, ser
from .relatorio import build_pdf

bp = Blueprint("egipcias", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/api/decompose")
def api_decompose():
    try: p, q = parse(request.args)
    except ValueError as e: return jsonify(error=str(e) if "Use" in str(e) else "Digite inteiros válidos.")
    st = decompose(p, q)
    return jsonify(steps=ser(st), checks=verify(p, q, st), p=p, q=q, sum=terms(st))

@bp.get("/api/test")
def api_test():
    N = max(3, min(int(request.args.get("n", 60)), 300))
    r = run_tests(N); r["n"] = N; r["t2n"] = table_2n()
    return jsonify(r)


@bp.get("/relatorio.pdf")
def report():
    try: p, q = parse(request.args)
    except ValueError: p, q = 5, 7
    N = max(3, min(int(request.args.get("n", 60)), 150))
    return send_file(build_pdf(p, q, N), mimetype="application/pdf",
                     download_name="relatorio_fracoes_egipcias.pdf", as_attachment=True)
