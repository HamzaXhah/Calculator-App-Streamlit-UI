import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from calculator import Calculator

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Page ── */
.stApp { background: #f0f4ff; font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 3rem; max-width: 720px; }
.stMainBlockContainer { padding-top: 0.5rem; }

/* ── Columns: zero inner padding so buttons sit flush ── */
[data-testid="column"] { padding: 0 4px !important; }
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── ALL buttons base (number keys) ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    height: 54px !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.12s ease !important;
    letter-spacing: 0.2px !important;
    background: #ffffff !important;
    color: #1e3a5f !important;
    box-shadow: 0 1px 3px rgba(30,58,95,0.10), 0 1px 2px rgba(30,58,95,0.06) !important;
}
[data-testid="stButton"] > button:hover {
    background: #e8f0fe !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.15) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: scale(0.95) translateY(0) !important;
    box-shadow: none !important;
}

/* ── Primary buttons (operators + equals) → blue ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: #2563eb !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.35) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Sci buttons ── */
.sci-btn [data-testid="stButton"] > button {
    height: 44px !important;
    font-size: 13px !important;
    background: #dbeafe !important;
    color: #1e40af !important;
    box-shadow: 0 1px 2px rgba(30,64,175,0.08) !important;
    font-weight: 600 !important;
}
.sci-btn [data-testid="stButton"] > button:hover {
    background: #bfdbfe !important;
    box-shadow: 0 3px 8px rgba(30,64,175,0.18) !important;
}

/* ── Memory buttons ── */
.mem-btn [data-testid="stButton"] > button {
    height: 38px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    background: #eff6ff !important;
    color: #3b82f6 !important;
    border: 1.5px solid #bfdbfe !important;
    box-shadow: none !important;
    letter-spacing: 0.5px !important;
}
.mem-btn [data-testid="stButton"] > button:hover {
    background: #dbeafe !important;
    border-color: #93c5fd !important;
}

/* ── Header ── */
.calc-title {
    text-align: center;
    padding: 4px 0 24px;
}
.calc-title h1 {
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: 5px;
    color: #1e3a5f;
    margin: 0;
}
.calc-title h1 span { color: #2563eb; }
.calc-title p {
    color: #94a3b8;
    font-size: 11px;
    letter-spacing: 2.5px;
    margin-top: 5px;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── Calculator card ── */
.calc-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 20px 20px 20px;
    box-shadow: 0 4px 24px rgba(30,58,95,0.10), 0 1px 4px rgba(30,58,95,0.06);
    border: 1px solid #e2e8f0;
    margin-bottom: 16px;
}

/* ── Screen ── */
.calc-screen {
    background: #f8faff;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px 20px 12px;
    text-align: right;
    margin-bottom: 16px;
    min-height: 86px;
    box-shadow: inset 0 2px 6px rgba(30,58,95,0.04);
}
.calc-expr {
    color: #94a3b8;
    font-size: 13px;
    font-family: 'Inter', monospace;
    min-height: 20px;
    font-weight: 500;
}
.calc-val {
    color: #1e3a5f;
    font-size: 38px;
    font-weight: 700;
    font-family: 'Inter', monospace;
    word-break: break-all;
    line-height: 1.15;
    margin-top: 2px;
}
.calc-val.err { color: #ef4444; font-size: 20px; }

/* ── Section label ── */
.sec-label {
    color: #94a3b8;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin: 8px 0 6px 2px;
}

/* ── Divider ── */
.divider { border: none; border-top: 1.5px solid #e2e8f0; margin: 16px 0; }

/* ── Memory bar ── */
.mem-bar {
    background: #f8faff;
    border: 1.5px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}
.mem-lbl { color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
.mem-val { color: #2563eb; font-family: 'Inter', monospace; font-size: 15px; font-weight: 700; }

/* ── History ── */
.hist-wrap {
    background: #f8faff;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    padding: 14px 16px;
}
.hist-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px 14px;
    margin-bottom: 6px;
    font-family: 'Inter', monospace;
    font-size: 12px;
    color: #64748b;
    font-weight: 500;
}
.hist-item:last-child { margin-bottom: 0; }
.hist-empty { color: #cbd5e1; text-align: center; padding: 12px; font-size: 13px; font-style: italic; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #ffffff !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1.5px solid #e2e8f0 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 1px 4px rgba(30,58,95,0.06) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    padding: 8px 20px !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #2563eb !important;
    color: #ffffff !important;
}

/* ── Graph panel ── */
.graph-hint {
    color: #94a3b8;
    font-size: 11px;
    margin-top: 4px;
    font-family: 'Inter', monospace;
    text-align: center;
}
.graph-hint code {
    background: #eff6ff;
    color: #2563eb;
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 11px;
}

/* ── Streamlit element spacing ── */
.stButton { margin-bottom: 8px !important; }
div[data-testid="stHorizontalBlock"] { gap: 8px !important; }

/* ── Input fields ── */
[data-testid="stTextInput"] input {
    background: #f8faff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1e3a5f !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
[data-testid="stNumberInput"] input {
    background: #f8faff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1e3a5f !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] {
    background: #f8faff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
}
label { color: #64748b !important; font-weight: 600 !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
def _init():
    defaults = dict(calc=Calculator(), display="0", expression="",
                    operand1=None, operator=None,
                    awaiting_op2=False, just_eval=False, error=False)
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt(v):
    if isinstance(v, float) and v == int(v) and abs(v) < 1e15:
        return str(int(v))
    return f"{v:.10g}"

def cur():
    try: return float(st.session_state.display)
    except: return 0.0

OP_SYM = {"add":"+","subtract":"−","multiply":"×","divide":"÷","power":"^","modulo":"mod"}

def _eval(a, op, b):
    c = st.session_state.calc
    return {"add":c.add,"subtract":c.subtract,"multiply":c.multiply,
            "divide":c.divide,"power":c.power,"modulo":c.modulo}[op](a, b)

# ── Action handlers ───────────────────────────────────────────────────────────
def digit(d):
    s = st.session_state
    if s.error: s.display,s.expression,s.error,s.just_eval = d,"",False,False; return
    if s.just_eval: s.display,s.just_eval = d,False
    elif s.awaiting_op2: s.display,s.awaiting_op2 = d,False
    else: s.display = d if s.display=="0" else (s.display+d if len(s.display)<20 else s.display)

def dot():
    s = st.session_state
    if s.error: s.display,s.error = "0.",False; return
    if s.just_eval or s.awaiting_op2: s.display,s.just_eval,s.awaiting_op2 = "0.",False,False
    elif "." not in s.display: s.display += "."

def clear():
    s = st.session_state
    s.display,s.expression,s.operand1,s.operator = "0","",None,None
    s.awaiting_op2,s.just_eval,s.error = False,False,False

def negate():
    s = st.session_state
    if s.error: return
    try: s.display = fmt(-cur())
    except Exception as e: s.display,s.error = str(e),True

def percent():
    s = st.session_state
    if s.error: return
    try:
        v = cur(); r = v/100
        s.expression,s.display,s.just_eval = f"{fmt(v)} % =",fmt(r),True
    except Exception as e: s.display,s.error = str(e),True

def operator(op):
    s = st.session_state
    if s.error: return
    try:
        c = cur()
        if s.operand1 is not None and s.operator and not s.awaiting_op2:
            c = _eval(s.operand1, s.operator, c); s.display = fmt(c)
        s.operand1,s.operator = c,op
        s.expression = f"{fmt(c)} {OP_SYM[op]}"
        s.awaiting_op2,s.just_eval = True,False
    except Exception as e: s.display,s.error = str(e),True

def equals():
    s = st.session_state
    if s.error: return
    if s.operand1 is None or s.operator is None: s.just_eval = True; return
    try:
        b = cur()
        s.expression = f"{fmt(s.operand1)} {OP_SYM[s.operator]} {fmt(b)} ="
        r = _eval(s.operand1, s.operator, b)
        s.display = fmt(r)
        s.operand1,s.operator,s.awaiting_op2,s.just_eval,s.error = None,None,False,True,False
    except Exception as e:
        s.display,s.expression,s.error,s.operand1,s.operator = str(e),"",True,None,None

def sci(fn):
    s = st.session_state
    c = s.calc
    if s.error: return
    try:
        v = cur()
        if fn in ("power","modulo"):
            s.operand1,s.operator = v,fn
            s.expression,s.awaiting_op2,s.just_eval = f"{fmt(v)} {OP_SYM[fn]}",True,False
            return
        consts = {"pi":(c.PI,"π"),"e_c":(c.E,"e"),"phi":(c.PHI,"φ")}
        if fn in consts:
            r,lbl = consts[fn]; s.expression,s.display,s.just_eval = f"{lbl} =",fmt(r),True; return
        ops = {"sin":(c.sin,"sin"),"cos":(c.cos,"cos"),"tan":(c.tan,"tan"),
               "asin":(c.asin,"asin"),"acos":(c.acos,"acos"),"atan":(c.atan,"atan"),
               "sqrt":(c.sqrt,"√"),"sq":(lambda x:c.power(x,2),"x²"),
               "log":(c.log10,"log"),"ln":(c.ln,"ln"),"fact":(c.factorial,"n!"),
               "rec":(c.reciprocal,"1/x"),"abs":(c.absolute_value,"|x|"),
               "d2r":(c.to_radians,"°→rad"),"r2d":(c.to_degrees,"rad→°")}
        f,lbl = ops[fn]; r = f(v)
        s.expression,s.display,s.just_eval,s.error = f"{lbl}({fmt(v)}) =",fmt(r),True,False
    except Exception as e: s.display,s.expression,s.error = str(e),"",True

def mem(action):
    s = st.session_state; c = s.calc
    try:
        v = cur()
        if action=="ms": c.memory_store(v)
        elif action=="mr": s.display,s.just_eval = fmt(c.memory_recall()),True
        elif action=="mc": c.memory_clear()
        elif action=="m+": c.memory_add(v)
    except Exception as e: s.display,s.error = str(e),True

# ── Render helpers ────────────────────────────────────────────────────────────
def B(label, fn, *args, primary=False, key=None):
    """Render a button and call fn(*args) on click."""
    k = key or f"_btn_{label}_{fn.__name__}"
    if st.button(label, key=k, use_container_width=True,
                 type="primary" if primary else "secondary"):
        fn(*args); st.rerun()

def SCI(label, fn_key, key=None):
    st.markdown('<div class="sci-btn">', unsafe_allow_html=True)
    k = key or f"_sci_{fn_key}"
    if st.button(label, key=k, use_container_width=True):
        sci(fn_key); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def MEM(label, action):
    st.markdown('<div class="mem-btn">', unsafe_allow_html=True)
    if st.button(label, key=f"_mem_{action}", use_container_width=True):
        mem(action); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="calc-title">
  <h1>SCIENTIFIC <span>CALCULATOR</span></h1>
  <p>Precision arithmetic &amp; scientific functions</p>
</div>
""", unsafe_allow_html=True)

tab_calc, tab_graph = st.tabs(["🧮  Calculator", "📈  Function Grapher"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Calculator
# ══════════════════════════════════════════════════════════════════════════════
with tab_calc:
    # Screen
    s = st.session_state
    expr_html = s.expression if s.expression else "&nbsp;"
    val_class = "calc-val err" if s.error else "calc-val"
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="calc-screen">
      <div class="calc-expr">{expr_html}</div>
      <div class="{val_class}">{s.display}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Main grid: left (numpad) | right (scientific) ────────────────────────
    left, right = st.columns([1.15, 1], gap="medium")

    with left:
        c1,c2,c3,c4 = st.columns(4, gap="small")
        with c1: B("AC", clear, key="_ac")
        with c2: B("+/−", negate, key="_neg")
        with c3: B("%", percent, key="_pct")
        with c4: B("÷", operator, "divide", primary=True, key="_div")
        c1,c2,c3,c4 = st.columns(4, gap="small")
        with c1: B("7", digit, "7")
        with c2: B("8", digit, "8")
        with c3: B("9", digit, "9")
        with c4: B("×", operator, "multiply", primary=True, key="_mul")
        c1,c2,c3,c4 = st.columns(4, gap="small")
        with c1: B("4", digit, "4")
        with c2: B("5", digit, "5")
        with c3: B("6", digit, "6")
        with c4: B("−", operator, "subtract", primary=True, key="_sub")
        c1,c2,c3,c4 = st.columns(4, gap="small")
        with c1: B("1", digit, "1")
        with c2: B("2", digit, "2")
        with c3: B("3", digit, "3")
        with c4: B("+", operator, "add", primary=True, key="_add")
        c1,c2,c3 = st.columns([2,1,1], gap="small")
        with c1: B("0", digit, "0", key="_0")
        with c2: B(".", dot, key="_dot")
        with c3: B("=", equals, primary=True, key="_eq")

    with right:
        st.markdown('<div class="sec-label">Trigonometry</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3, gap="small")
        with c1: SCI("sin","sin")
        with c2: SCI("cos","cos")
        with c3: SCI("tan","tan")
        c1,c2,c3 = st.columns(3, gap="small")
        with c1: SCI("asin","asin")
        with c2: SCI("acos","acos")
        with c3: SCI("atan","atan")

        st.markdown('<div class="sec-label" style="margin-top:8px;">Math</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3, gap="small")
        with c1: SCI("√","sqrt")
        with c2: SCI("x²","sq")
        with c3: SCI("xⁿ","power")
        c1,c2,c3 = st.columns(3, gap="small")
        with c1: SCI("log","log")
        with c2: SCI("ln","ln")
        with c3: SCI("n!","fact")
        c1,c2,c3 = st.columns(3, gap="small")
        with c1: SCI("1/x","rec")
        with c2: SCI("|x|","abs")
        with c3: SCI("mod","modulo")

        st.markdown('<div class="sec-label" style="margin-top:8px;">Constants</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3, gap="small")
        with c1: SCI("π","pi",key="_pi")
        with c2: SCI("e","e_c",key="_ec")
        with c3: SCI("φ","phi",key="_phi")

        st.markdown('<div class="sec-label" style="margin-top:8px;">Angles</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2, gap="small")
        with c1: SCI("°→rad","d2r")
        with c2: SCI("rad→°","r2d")

    st.markdown('</div>', unsafe_allow_html=True)  # close calc-card

    # ── Memory ────────────────────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    mem_val = fmt(st.session_state.calc.memory_recall())
    st.markdown(f"""
    <div class="mem-bar">
      <span class="mem-lbl">MEMORY</span>
      <span class="mem-val">{mem_val}</span>
    </div>
    """, unsafe_allow_html=True)

    mc1,mc2,mc3,mc4,_ = st.columns([1,1,1,1,3], gap="small")
    for col, lbl, act in [(mc1,"MS","ms"),(mc2,"MR","mr"),(mc3,"MC","mc"),(mc4,"M+","m+")]:
        with col:
            st.markdown('<div class="mem-btn">', unsafe_allow_html=True)
            if st.button(lbl, key=f"_mem_{act}", use_container_width=True):
                mem(act); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── History ───────────────────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    hcol1, hcol2 = st.columns([4,1])
    with hcol1:
        st.markdown('<div class="sec-label" style="font-size:10px;margin:6px 0 4px;">CALCULATION HISTORY</div>', unsafe_allow_html=True)
    with hcol2:
        if st.button("Clear", key="_clrhist", use_container_width=True):
            st.session_state.calc.clear_history(); st.rerun()

    history = st.session_state.calc.get_history()
    if history:
        items = "".join(f'<div class="hist-item">{e.expression}</div>' for e in reversed(history[-15:]))
        st.markdown(f'<div class="hist-wrap">{items}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hist-wrap"><div class="hist-empty">No calculations yet</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Function Grapher
# ══════════════════════════════════════════════════════════════════════════════
with tab_graph:
    st.markdown('<div class="sec-label" style="font-size:10px;margin-bottom:12px;">PLOT UP TO 3 FUNCTIONS SIMULTANEOUSLY</div>', unsafe_allow_html=True)

    # Preset examples
    PRESETS = {
        "None": ("", "", ""),
        "sin & cos": ("sin(x)", "cos(x)", ""),
        "Quadratic & Linear": ("x**2 - 4", "2*x + 1", ""),
        "Trig Combo": ("sin(x)", "cos(x)", "tan(x)"),
        "Exponential": ("exp(x/3)", "log(abs(x)+0.1)", ""),
        "Polynomials": ("x**3 - 3*x", "x**2 - 2", "x"),
    }

    preset = st.selectbox("Quick presets", list(PRESETS.keys()), key="_preset")
    p1, p2, p3 = PRESETS[preset]

    st.markdown('<div class="sec-label" style="margin-top:4px;">Functions (use x as variable)</div>', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3, gap="small")
    with fc1:
        f1 = st.text_input("f₁(x)", value=p1, placeholder="sin(x)", key="_f1", label_visibility="collapsed")
        st.markdown("<div class='graph-hint' style='color:#2563eb'>● f₁(x)</div>", unsafe_allow_html=True)
    with fc2:
        f2 = st.text_input("f₂(x)", value=p2, placeholder="x**2", key="_f2", label_visibility="collapsed")
        st.markdown("<div class='graph-hint' style='color:#f97316'>● f₂(x)</div>", unsafe_allow_html=True)
    with fc3:
        f3 = st.text_input("f₃(x)", value=p3, placeholder="cos(x)", key="_f3", label_visibility="collapsed")
        st.markdown("<div class='graph-hint' style='color:#16a34a'>● f₃(x)</div>", unsafe_allow_html=True)

    rc1, rc2 = st.columns(2, gap="small")
    with rc1:
        x_min = st.number_input("x min", value=-10.0, step=1.0, key="_xmin")
    with rc2:
        x_max = st.number_input("x max", value=10.0, step=1.0, key="_xmax")

    # Safe eval namespace
    SAFE_NS = {k: getattr(np, k) for k in dir(np) if not k.startswith("_")}
    SAFE_NS.update({"pi": np.pi, "e": np.e, "abs": np.abs})

    def safe_eval_func(expr, x_vals):
        """Evaluate a math expression string over an array of x values."""
        ns = {**SAFE_NS, "x": x_vals}
        return np.array(eval(compile(expr.strip(), "<string>", "eval"), {"__builtins__": {}}, ns), dtype=float)

    if st.button("Plot", key="_plot", type="primary", use_container_width=False):
        funcs = [(f1, "#2563eb", "f₁"), (f2, "#f97316", "f₂"), (f3, "#16a34a", "f₃")]
        entries = [(expr.strip(), col, lbl) for expr, col, lbl in funcs if expr.strip()]

        if not entries:
            st.warning("Enter at least one function to plot.")
        elif x_min >= x_max:
            st.error("x min must be less than x max.")
        else:
            x = np.linspace(x_min, x_max, 800)

            fig, ax = plt.subplots(figsize=(8, 4.5))
            fig.patch.set_facecolor("#ffffff")
            ax.set_facecolor("#f8faff")
            ax.tick_params(colors="#64748b", labelsize=9)
            for spine in ax.spines.values():
                spine.set_color("#e2e8f0")
                spine.set_linewidth(1.5)
            ax.xaxis.label.set_color("#64748b")
            ax.yaxis.label.set_color("#64748b")
            ax.grid(True, color="#e2e8f0", linewidth=1.0, linestyle="--")
            ax.axhline(0, color="#cbd5e1", linewidth=1.0)
            ax.axvline(0, color="#cbd5e1", linewidth=1.0)

            any_plotted = False
            for expr, color, label in entries:
                try:
                    y = safe_eval_func(expr, x)
                    # Clip extreme values to keep plot readable
                    y_clipped = np.where(np.abs(y) > 1e6, np.nan, y)
                    ax.plot(x, y_clipped, color=color, linewidth=2,
                            label=f"{label}(x) = {expr}")
                    any_plotted = True
                except Exception as err:
                    st.error(f"Error in **{label}(x) = {expr}**: {err}")

            if any_plotted:
                legend = ax.legend(facecolor="#ffffff", edgecolor="#e2e8f0",
                                   labelcolor="#1e3a5f", fontsize=9)
                ax.set_xlabel("x", color="#444466")
                ax.set_ylabel("y", color="#444466")
                st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    st.markdown("""
    <div class="graph-hint" style="margin-top:12px; line-height:2;">
    Supported syntax: &nbsp;
    <code>sin(x)</code> &nbsp; <code>cos(x)</code> &nbsp; <code>tan(x)</code> &nbsp;
    <code>exp(x)</code> &nbsp; <code>log(x)</code> &nbsp; <code>sqrt(x)</code> &nbsp;
    <code>x**2</code> &nbsp; <code>abs(x)</code> &nbsp; <code>pi</code> &nbsp; <code>e</code>
    </div>
    """, unsafe_allow_html=True)
