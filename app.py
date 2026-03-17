import streamlit as st
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
/* Page background */
.stApp { background: #0d0d14; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1rem 2rem; max-width: 700px; }

/* Remove default streamlit top padding */
.stMainBlockContainer { padding-top: 1rem; }

/* ALL buttons base */
[data-testid="stButton"] > button {
    width: 100% !important;
    border-radius: 10px !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    height: 56px !important;
    border: none !important;
    cursor: pointer !important;
    transition: filter 0.1s, transform 0.08s !important;
    letter-spacing: 0.3px !important;
    background: #1c1c2e !important;
    color: #e8e8ff !important;
}
[data-testid="stButton"] > button:hover { filter: brightness(1.2) !important; }
[data-testid="stButton"] > button:active { transform: scale(0.93) !important; }

/* Primary buttons (operators + equals) → amber */
[data-testid="stButton"] > button[kind="primary"] {
    background: #b45309 !important;
    color: #fff !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #d97706 !important;
    filter: none !important;
}

/* Column gap tighter */
[data-testid="column"] { padding: 0 3px !important; }

/* Screen */
.calc-screen {
    background: #12121f;
    border: 1px solid #1e1e38;
    border-radius: 16px;
    padding: 18px 22px 14px;
    text-align: right;
    margin-bottom: 14px;
    min-height: 90px;
    box-shadow: inset 0 2px 16px rgba(0,0,0,0.7);
}
.calc-expr { color: #3a3a5a; font-size: 13px; font-family: monospace; min-height: 20px; }
.calc-val  { color: #ffffff; font-size: 40px; font-weight: 700; font-family: monospace;
             word-break: break-all; line-height: 1.15; margin-top: 2px; }
.calc-val.err { color: #f87171; font-size: 20px; }

/* Section heading */
.sec-label {
    color: #2a2a44;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 4px 0 6px 2px;
}

/* Divider */
.divider { border: none; border-top: 1px solid #1a1a2e; margin: 14px 0; }

/* Memory bar */
.mem-bar {
    background: #12121f;
    border: 1px solid #1e1e38;
    border-radius: 12px;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
.mem-lbl { color: #2a2a44; font-size: 10px; font-weight: 700; letter-spacing: 2px; }
.mem-val { color: #f59e0b; font-family: monospace; font-size: 15px; font-weight: 700; }

/* History */
.hist-wrap {
    background: #12121f;
    border: 1px solid #1e1e38;
    border-radius: 12px;
    padding: 12px 16px;
}
.hist-item {
    background: #0a0a15;
    border: 1px solid #181828;
    border-radius: 7px;
    padding: 7px 12px;
    margin-bottom: 5px;
    font-family: monospace;
    font-size: 12px;
    color: #444466;
}
.hist-empty { color: #222235; text-align: center; padding: 10px; font-size: 13px; font-style: italic; }

/* Header */
.calc-title {
    text-align: center;
    padding: 8px 0 20px;
}
.calc-title h1 {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #f59e0b, #ef4444, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.calc-title p { color: #2a2a44; font-size: 11px; letter-spacing: 2px; margin-top: 4px; text-transform: uppercase; }

/* Make sci buttons smaller */
.sci-btn [data-testid="stButton"] > button {
    height: 46px !important;
    font-size: 13px !important;
    background: #0e1825 !important;
    color: #60a5fa !important;
}
.sci-btn [data-testid="stButton"] > button[kind="primary"] {
    background: #0c2818 !important;
    color: #34d399 !important;
}
.mem-btn [data-testid="stButton"] > button {
    height: 38px !important;
    font-size: 12px !important;
    background: #150a2e !important;
    color: #a78bfa !important;
}
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
  <h1>SCIENTIFIC CALCULATOR</h1>
  <p>Precision arithmetic &amp; scientific functions</p>
</div>
""", unsafe_allow_html=True)

# Screen
s = st.session_state
expr_html = s.expression if s.expression else "&nbsp;"
val_class = "calc-val err" if s.error else "calc-val"
st.markdown(f"""
<div class="calc-screen">
  <div class="calc-expr">{expr_html}</div>
  <div class="{val_class}">{s.display}</div>
</div>
""", unsafe_allow_html=True)

# ── Main grid: left (numpad) | right (scientific) ────────────────────────────
left, right = st.columns([1.15, 1], gap="medium")

with left:
    # Row 1
    c1,c2,c3,c4 = st.columns(4, gap="small")
    with c1: B("AC", clear, key="_ac")
    with c2: B("+/−", negate, key="_neg")
    with c3: B("%", percent, key="_pct")
    with c4: B("÷", operator, "divide", primary=True, key="_div")
    # Row 2
    c1,c2,c3,c4 = st.columns(4, gap="small")
    with c1: B("7", digit, "7")
    with c2: B("8", digit, "8")
    with c3: B("9", digit, "9")
    with c4: B("×", operator, "multiply", primary=True, key="_mul")
    # Row 3
    c1,c2,c3,c4 = st.columns(4, gap="small")
    with c1: B("4", digit, "4")
    with c2: B("5", digit, "5")
    with c3: B("6", digit, "6")
    with c4: B("−", operator, "subtract", primary=True, key="_sub")
    # Row 4
    c1,c2,c3,c4 = st.columns(4, gap="small")
    with c1: B("1", digit, "1")
    with c2: B("2", digit, "2")
    with c3: B("3", digit, "3")
    with c4: B("+", operator, "add", primary=True, key="_add")
    # Row 5
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

# ── Memory ────────────────────────────────────────────────────────────────────
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

# ── History ───────────────────────────────────────────────────────────────────
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
