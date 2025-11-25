impor t streamlit as st
impor t plotly.graph_objects as go
impor t pandas as pd
impor t json
from datetime impor t datetime
# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_ page_config(
page_title="CIBC Databricks AI Dashboard",
page_ icon=" ",
layout="wide"
)
# ============================================================================
# THEME SETTINGS
# ============================================================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    if st.session_state.theme == 'dark':
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'

with st.sidebar:
    st.markdown("## Theme")
    st.toggle("Light Mode", value=(st.session_state.theme == 'light'), on_change=toggle_theme)

# ============================================================================
# CIBC COLORS
# ============================================================================
if st.session_state.theme == 'light':
    RED_PRIMARY = "#ED1B2E"
    RED_DARK = "#C8102E"
    RED_LIGHT = "#FF5252"
    ORANGE = "#FF6B35"
    GOLD = "#FFB800"
    GRAY_DARK = "#FFFFFF"
    GRAY_MED = "#F0F2F6"
    GRAY_LIGHT = "#31333F"
    WHITE = "#000000"
    PLOTLY_TEMPLATE = 'plotly_white'
else:
    RED_PRIMARY = "#ED1B2E"
    RED_DARK = "#C8102E"
    RED_LIGHT = "#FF5252"
    ORANGE = "#FF6B35"
    GOLD = "#FFB800"
    GRAY_DARK = "#1A1A1A"
    GRAY_MED = "#2D2D2D"
    GRAY_LIGHT = "#CCCCCC"
    WHITE = "#FFFFFF"
    PLOTLY_TEMPLATE = 'plotly_dark'
# ============================================================================
# SESSION STATE
# ============================================================================
if 'models' not in st.session_state:
st.session_state.models = {
'databricks_assistant': {
'name': 'Databricks Assistant',
'provider': 'Databricks',
'params': 'Optimized',
'context': 32000,
'output_ max': 4096,
'thinking _ max': 0,
'cost_ in': 0.0,
'cost_out': 0.0,
'coding': 9.0,
'speed': 9,
'value': 10,
'response_time': 1.5,
'best': ['Quick notebook queries', 'Notebook context-aware', 'SQL optimization', 'Free with workspace'],
'avoid': ['Complex reasoning', 'Outside notebook context']
},
'llama_405b': {
'name': 'Llama 3.1 405B Instruct',
'provider': 'Meta',
'params': '405B',
'context': 128000,
'output_ max': 4096,
'thinking _ max': 4000,
'cost_ in': 0.003,
'cost_out': 0.003,
'coding': 9.5,
'speed': 3,
'value': 3,
'response_time': 8.0,
'best': ['Complex system design', 'Critical architecture', 'Deep reasoning'],
'avoid': ['Simple tasks', 'Budget projects', 'Speed-critical']
},
'llama_70b': {
'name': 'Llama 3.3 70B Instruct',
'provider': 'Meta',
'params': '70B',
'context': 128000,
'output_ max': 4096,
'thinking _ max': 2000,
'cost_ in': 0.0006,
'cost_out': 0.0006,
'coding': 9.0,
'speed': 6,
'value': 8,
'response_time': 3.5,
'best': ['Production code', 'SQL optimization', 'Data pipelines'],
'avoid': ['Maximum complexity', 'Ultra-fast needs']
},
'llama_8b': {
'name': 'Llama 3.1 8B Instruct',
'provider': 'Meta',
'params': '8B',
'context': 128000,
'output_ max': 4096,
'thinking _ max': 0,
'cost_ in': 0.0001,
'cost_out': 0.0001,
'coding': 6.5,
'speed': 10,
'value': 10,
'response_time': 0.8,
'best': ['Quick scripts', 'Learning', 'High volume'],
'avoid': ['Complex reasoning', 'Critical systems']
},
'llama_ maverick': {
'name': 'Llama 4 Maverick',
'provider': 'Meta',
'params': '~100B',
'context': 128000,
'output_ max': 4096,
'thinking _ max': 2000,
'cost_ in': 0.0008,
'cost_out': 0.0008,
'coding': 9.5,
'speed': 7,
'value': 7,
'response_time': 4.0,
'best': ['Next-gen features', 'Experimental'],
'avoid': ['Production critical', 'Stability needed']
},
'claude_opus_41': {
'name': 'Claude Opus 4.1',
'provider': 'Anthropic',
'params': 'Proprietar y',
'context': 200000,
'output_ max': 8192,
'thinking _ max': 0,
'cost_ in': 0.015,
'cost_out': 0.075,
'coding': 9.5,
'speed': 5,
'value': 3,
'response_time': 6.0,
'best': ['Highest quality', 'Compliance', 'Critical review'],
'avoid': ['Budget constraints', 'High volume']
},
'claude_opus_4': {
'name': 'Claude Opus 4',
'provider': 'Anthropic',
'params': 'Proprietar y',
'context': 200000,
'output_ max': 8192,
'thinking _ max': 3000,
'cost_ in': 0.015,
'cost_out': 0.075,
'coding': 9.5,
'speed': 5,
'value': 3,
'response_time': 7.0,
'best': ['Deep reasoning', 'Complex analysis'],
'avoid': ['Cost-sensitive', 'Fast iteration']
},
'claude_sonnet_45': {
'name': 'Claude Sonnet 4.5',
'provider': 'Anthropic',
'params': 'Proprietar y',
'context': 200000,
'output_ max': 8192,
'thinking _ max': 2500,
'cost_ in': 0.003,
'cost_out': 0.015,
'coding': 10.0,
'speed': 8,
'value': 9,
'response_time': 2.5,
'best': ['Production coding', 'PySpark', 'Best overall'],
'avoid': ['Simple tasks only']
},
'claude_sonnet_4': {
'name': 'Claude Sonnet 4',
'provider': 'Anthropic',
'params': 'Proprietar y',
'context': 200000,
'output_ max': 8192,
'thinking _ max': 2000,
'cost_ in': 0.003,
'cost_out': 0.015,
'coding': 10.0,
'speed': 8,
'value': 9,
'response_time': 2.8,
'best': ['Production dev', 'Balanced per formance'],
'avoid': ['Budget critical']
},
'claude_sonnet_37': {
'name': 'Claude Sonnet 3.7',
'provider': 'Anthropic',
'params': 'Proprietar y',
'context': 200000,
'output_ max': 8192,
'thinking _ max': 1500,
'cost_ in': 0.003,
'cost_out': 0.015,
'coding': 9.5,
'speed': 8,
'value': 8,
'response_time': 3.0,
'best': ['General purpose', 'Legacy'],
'avoid': ['Use Sonnet 4.5 instead']
},
'gpt_oss_120b': {
'name': 'GPT OSS 120B',
'provider': 'Databricks',
'params': '120B',
'context': 32000,
'output_ max': 4096,
'thinking _ max': 1000,
'cost_ in': 0.0005,
'cost_out': 0.0005,
'coding': 8.0,
'speed': 7,
'value': 7,
'response_time': 4.5,
'best': ['Open source', 'Custom tuning', 'DB optimized'],
'avoid': ['Cutting-edge needs']
},
'gpt_oss_20b': {
'name': 'GPT OSS 20B',
'provider': 'Databricks',
'params': '20B',
'context': 32000,
'output_ max': 4096,
'thinking _ max': 500,
'cost_ in': 0.0002,
'cost_out': 0.0002,
'coding': 6.5,
'speed': 9,
'value': 9,
'response_time': 1.2,
'best': ['Cost-effective', 'Batch', 'Simple tasks'],
'avoid': ['Complex reasoning']
},
'gemma_12b': {
'name': 'Gemma 3 12B',
'provider': 'Google',
'params': '12B',
'context': 8192,
'output_ max': 2048,
'thinking _ max': 500,
'cost_ in': 0.0001,
'cost_out': 0.0001,
'coding': 7.0,
'speed': 10,
'value': 10,
'response_time': 0.9,
'best': ['Ultra-fast', 'High volume', 'Simple code'],
'avoid': ['Complex tasks', 'Large context']
}
}
# ============================================================================
# CSS STYLING - Dark Mode
# ============================================================================
st.markdown(f"""
<style>
.stApp {{
background-color: {GRAY_DARK};
color: {WHITE};
}}
h1, h2, h3 {{
color: {RED_PRIMARY} !impor tant;
font-weight: 700 !impor tant;
}}
.stButton > button {{
background-color: {RED_PRIMARY} !impor tant;
color: white !impor tant;
border: none !impor tant;
border-radius: 8px !impor tant;
font-weight: 600 !impor tant;
padding: 12px 30px !impor tant;
transition: all 0.3s !impor tant;
}}
.stButton > button:hover {{
background-color: {RED_DARK} !impor tant;
transform: translateY(-2px);
box-shadow: 0 5px 15px rgba(237, 27, 46, 0.4) !impor tant;
}}
[data-testid="stSidebar"] {{
background-color: {GRAY_MED};
border-right: 3px solid {RED_PRIMARY};
}}
.stTabs [data-baseweb="tab-list"] {{
gap: 10px;
}}
.stTabs [data-baseweb="tab"] {{
background-color: {GRAY_MED};
color: {WHITE};
border-radius: 8px;
padding: 12px 24px;
font-weight: 600;
}}
.stTabs [aria-selected="true"] {{
background-color: {RED_PRIMARY} !impor tant;
color: white !impor tant;
}}
.metric-container {{
background: linear-gradient(135deg, {RED_PRIMARY}20, {RED_DARK}20);
border: 2px solid {RED_PRIMARY};
border-radius: 12px;
padding: 20px;
text-align: center;
}}
.stMetric {{
background-color: {GRAY_MED};
padding: 15px;
border-radius: 8px;
border-left: 4px solid {RED_PRIMARY};
}}
.stMetric label {{
color: {GRAY_LIGHT} !impor tant;
font-size: 14px !impor tant;
}}
.stMetric [data-testid="stMetricValue"] {{
color: {RED_PRIMARY} !impor tant;
font-size: 32px !impor tant;
font-weight: 800 !impor tant;
}}
</style>
""", unsafe_allow_html=True)
# ============================================================================
# HEADER
# ============================================================================
col1, col2 = st.columns([1, 8])
with col1:
st.markdown(f"""
<div style="background: {RED_PRIMARY}; width: 70px; height: 70px;
border-radius: 12px; display: flex; align-items: center;
justify-content: center; font-size: 32px;">
</div>
""", unsafe_allow_html=True)
with col2:
st.title("Databricks AI Models Dashboard")
st.caption("CIBC Analytics | Model Selection & Cost Analysis")
st.markdown("---")
# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
st.markdown(f"## Controls")
st.markdown("### Filter Models")
providers = ['Meta', 'Anthropic', 'Databricks', 'Google']
selected _ providers = st.multiselect(
"Select Providers",
providers,
default=providers
)
min_score = st.slider("Min Coding Score", 0.0, 10.0, 0.0, 0.5)
max_cost = st.slider("Max Cost ($/1K)", 0.0, 0.02, 0.02, 0.001, format="%.4f")
only_thinking = st.checkbox("Only Thinking Token Models")
max_ response_time = st.slider("Max Response Time (sec)", 0.0, 10.0, 10.0, 0.5)
st.markdown("---")
st.markdown("### Expor t Data")
if st.button(" Expor t JSON"):
json_str = json.dumps(st.session_state.models, indent=2)
st.download _button(
"Download",
json_str,
f"models_{datetime.now().str ftime('%Y%m%d')}.json",
"application/json"
)
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px;
background: linear-gradient(135deg, {RED_PRIMARY}30, {ORANGE}20);
border-radius: 10px; border: 2px solid {RED_PRIMARY};">
<div style="font-size: 28px; margin-bottom: 10px;"> </div>
<div style="font-weight: 700; color: {RED_PRIMARY}; font-size: 18px;">CIBC</div>
<div style="font-size: 11px; color: {GRAY_LIGHT};">
Analytics & Data Science
</div>
</div>
""", unsafe_allow_html=True)
# ============================================================================
# FILTER MODELS
# ============================================================================
filtered = {
k: v for k, v in st.session_state.models.items()
if v['provider'] in selected _ providers
and v['coding'] >= min_score
and v['cost_ in'] <= max_cost
and (not only_thinking or v['thinking _ max'] > 0)
and v['response_time'] <= max_ response_time
}
# ============================================================================
# KEY METRICS
# ============================================================================
st.markdown("## Dashboard Over view")
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
st.metric("Total Models", len(filtered), delta=f"{len(st.session_state.models)} total")
with m2:
avg _cost = sum([m['cost_ in'] for m in filtered.values()]) / len(filtered) if filtered else 0
st.metric("Avg Cost/1K", f"${avg _cost:.4f}")
with m3:
thinking _count = sum([1 for m in filtered.values() if m['thinking _ max'] > 0])
st.metric("With Thinking", thinking _count)
with m4:
avg _coding = sum([m['coding'] for m in filtered.values()]) / len(filtered) if filtered else 0
st.metric("Avg Coding", f"{avg _coding:.1f}/10")
with m5:
avg _ response = sum([m['response_time'] for m in filtered.values()]) / len(filtered) if filtered else 0
st.metric("Avg Response", f"{avg _ response:.1f}s")
st.markdown("---")
# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs([" Models", " Learn", " Calculator", " Edit"])
# ============================================================================
# TAB 1: MODELS - Visual Comparison + Detailed Cards
# ============================================================================
with tab1:
st.markdown("## Model Comparison & Details")
if not filtered:
st.warning("⚠️ No models match your filters. Adjust settings in sidebar.")
else:
# Highlight Databricks Assistant
if 'databricks_assistant' in filtered:
st.info(" **Databricks Assistant** is optimized for quick notebook queries with full context awareness.
It's **FREE** with your workspace!")
st.markdown("---")
st.markdown("### Quick Comparison")
# Create comparison dataframe
comparison_data = []
for model _ id, m in filtered.items():
comparison_data.append({
'Model': m['name'],
'Provider': m['provider'],
'Params': m['params'],
'Coding': m['coding'],
'Speed': m['speed'],
'Value': m['value'],
'Cost': m['cost_ in'],
'Response': m['response_time'],
'Thinking': m['thinking _ max'],
'Context': m['context']
})
df_compare = pd.DataFrame(comparison_data)
# Interactive comparison table
st.dataframe(
df_compare.style.background _gradient(subset=['Coding', 'Speed', 'Value'], cmap='Reds')
.format({'Cost': '${:.4f}', 'Response': '{:.1f}s', 'Thinking': '{:,}', 'Context': '{:,}'}),
use_container_width=True,
height=300
)
st.markdown("---")
# Visual comparisons in tabs
compare_tabs = st.tabs([" Scores", " Cost & Speed", " Capabilities"])
with compare_tabs[0]:
# Scores comparison
fig _scores = go.Figure()
fig _scores.add _trace(go.Bar(
name='Coding',
x=[m['name'] for m in filtered.values()],
y=[m['coding'] for m in filtered.values()],
marker_color=RED_PRIMARY,
text=[f"{m['coding']:.1f}" for m in filtered.values()],
textposition='outside'
))
fig _scores.add _trace(go.Bar(
name='Speed',
x=[m['name'] for m in filtered.values()],
y=[m['speed'] for m in filtered.values()],
marker_color=ORANGE,
text=[f"{m['speed']}" for m in filtered.values()],
textposition='outside'
))
fig _scores.add _trace(go.Bar(
name='Value',
x=[m['name'] for m in filtered.values()],
y=[m['value'] for m in filtered.values()],
marker_color=GOLD,
text=[f"{m['value']}" for m in filtered.values()],
textposition='outside'
))
fig _scores.update_layout(
title="Per formance Scores Comparison (0-10)",
xaxis_title="",
yaxis_title="Score",
barmode='group',
template='plotly_dark',
height=450,
yaxis=dict(range=[0, 11]),
legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_char t(fig _scores, use_container_width=True)
with compare_tabs[1]:
# Cost and response time
col1, col2 = st.columns(2)
with col1:
fig _cost = go.Figure()
colors_cost = [RED_PRIMARY if m['cost_ in'] == 0 else ORANGE for m in filtered.values()]
fig _cost.add _trace(go.Bar(
x=[m['name'] for m in filtered.values()],
y=[m['cost_ in'] * 1000 for m in filtered.values()],
marker_color=colors_cost,
text=[f"${m['cost_ in']:.4f}" if m['cost_ in'] > 0 else "FREE" for m in filtered.values()],
textposition='outside'
))
fig _cost.update_layout(
title="Input Cost per 1K Tokens",
xaxis_title="",
yaxis_title="Cost ($)",
template='plotly_dark',
height=400,
showlegend=False
)
st.plotly_char t(fig _cost, use_container_width=True)
with col2:
fig _time = go.Figure()
colors_time = [RED_PRIMARY if m['response_time'] < 2 else (ORANGE if m['response_time'] < 4 else
GOLD) for m in filtered.values()]
fig _time.add _trace(go.Bar(
x=[m['name'] for m in filtered.values()],
y=[m['response_time'] for m in filtered.values()],
marker_color=colors_time,
text=[f"{m['response_time']}s" for m in filtered.values()],
textposition='outside'
))
fig _time.update_layout(
title="Response Time",
xaxis_title="",
yaxis_title="Seconds",
template='plotly_dark',
height=400,
showlegend=False
)
st.plotly_char t(fig _time, use_container_width=True)
with compare_tabs[2]:
# Capabilities (thinking tokens and context)
col1, col2 = st.columns(2)
with col1:
fig _thinking = go.Figure()
thinking _ models = [(m['name'], m['thinking _ max']) for m in filtered.values() if m['thinking _ max'] > 0]
if thinking _ models:
fig _thinking.add _trace(go.Bar(
x=[m[0] for m in thinking _ models],
y=[m[1] for m in thinking _ models],
marker_color=RED_PRIMARY,
text=[f"{m[1]:,}" for m in thinking _ models],
textposition='outside'
))
fig _thinking.update_layout(
title="Max Thinking Tokens",
xaxis_title="",
yaxis_title="Tokens",
template='plotly_dark',
height=400,
showlegend=False
)
st.plotly_char t(fig _thinking, use_container_width=True)
else:
st.info("No models with thinking tokens in current filter")
with col2:
fig _context = go.Figure()
fig _context.add _trace(go.Bar(
x=[m['name'] for m in filtered.values()],
y=[m['context'] / 1000 for m in filtered.values()],
marker_color=ORANGE,
text=[f"{m['context']//1000}K" for m in filtered.values()],
textposition='outside'
))
fig _context.update_layout(
title="Context Window Size",
xaxis_title="",
yaxis_title="Tokens (K)",
template='plotly_dark',
height=400,
showlegend=False
)
st.plotly_char t(fig _context, use_container_width=True)
st.markdown("---")
st.markdown("### Detailed Model Information")
st.caption("Expand each card for complete details")
# Display detailed model cards
for idx, (model _ id, m) in enumerate(filtered.items()):
# Create expandable card for each model
with st.expander(f"{' ' if model _ id == 'databricks_assistant' else ''}{m['name']} - {m['params']}",
expanded=False):
# Provider and basic info
col _ info, col _ metrics = st.columns([1, 2])
with col _ info:
st.markdown(f"**Provider:** {m['provider']}")
st.markdown(f"**Parameters:** {m['params']}")
st.markdown(f"**Context:** {m['context']:,} tokens")
st.markdown(f"**Max Output:** {m['output_ max']:,} tokens")
if m['thinking _ max'] > 0:
st.markdown(f"** Thinking Tokens:** {m['thinking _ max']:,}")
if model _ id == 'databricks_assistant':
st.markdown("** Notebook Context Aware**")
with col _ metrics:
# Metrics in columns
mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
st.metric("Coding", f"{m['coding']}/10")
with mc2:
cost_display = "FREE" if m['cost_ in'] == 0 else f"${m['cost_ in']:.4f}"
st.metric("Cost/1K", cost_display)
with mc3:
st.metric("Speed", f"{m['speed']}/10")
with mc4:
if m['response_time'] <= 2:
speed _label = " "
elif m['response_time'] <= 4:
speed _label = " "
else:
speed _label = " "
st.metric("Response", f"{m['response_time']}s", delta=speed _label)
# Best for / Avoid
col _best, col _avoid = st.columns(2)
with col _best:
st.markdown(f"** BEST FOR:**")
for item in m['best'][:3]:
st.markdown(f"- {item}")
with col _avoid:
st.markdown(f"** AVOID FOR:**")
for item in m['avoid'][:2]:
st.markdown(f"- {item}")
# ============================================================================
# TAB 2: LEARN
# ============================================================================
with tab2:
st.markdown("## Educational Guide")
learn_tabs = st.tabs([" Reasoning", " Thinking Tokens", " Parameters", " DB Assistant"])
with learn_tabs[0]:
st.markdown("### What is a Reasoning Model?")
st.info("A reasoning model thinks step-by-step before answering. It breaks down complex tasks, considers
alternatives, and validates logic.")
col1, col2 = st.columns(2)
with col1:
st.markdown("** Without Reasoning**")
st.code("""
User: Optimize this quer y
Model: Here's the quer y
(may miss issues)
""")
with col2:
st.markdown("** With Reasoning**")
st.code("""
User: Optimize this quer y
Model: [Analyzes joins...]
[Checks par titions...]
Here's why this works...
""")
st.markdown("### Reasoning Models Available")
reasoning _ models = {k: v for k, v in filtered.items() if v['thinking _ max'] > 0}
for model _ id, m in reasoning _ models.items():
st.success(f"**{m['name']}** - {m['thinking _ max']} thinking tokens")
with learn_tabs[1]:
st.markdown("### What are Thinking Tokens?")
st.info("Thinking tokens are the model's internal dialogue before responding. You set a budget (e.g., 4000)
for how much thinking space it gets.")
thinking _budget = st.slider("Set Thinking Budget", 0, 4000, 2000, 500)
c1, c2, c3 = st.columns(3)
quality = min(10, (thinking _budget / 400) + 5)
c1.metric("Expected Quality", f"{quality:.1f}/10")
time = 1 + (thinking _budget / 1000)
c2.metric("Response Time", f"{time:.1f}s")
cost = 1 + (thinking _budget / 1000)
c3.metric("Cost Multiplier", f"{cost:.1f}x")
st.warning(f"**Cost Impact:** Thinking tokens cost the same as input! {thinking _budget} thinking + 500
output = {thinking _budget + 500} total tokens")
st.markdown("### Recommended Settings")
df_thinking = pd.DataFrame([
{'Task': 'Simple quer y', 'Tokens': '0-500', 'Example': 'Basic SELECT'},
{'Task': 'Medium task', 'Tokens': '1000-1500', 'Example': 'Optimize JOIN'},
{'Task': 'Complex', 'Tokens': '2000-3000', 'Example': 'Design pipeline'},
{'Task': 'Critical', 'Tokens': '4000', 'Example': 'Architecture review'}
])
st.dataframe(df_thinking, use_container_width=True, hide_ index=True)
with learn_tabs[2]:
st.markdown("### Understanding Parameters")
st.info("Parameters are the model's brain cells. More = smar ter but slower and more expensive.")
df_ params = pd.DataFrame([
{'Size': '8-12B', 'Speed': ' ', 'Quality': ' ', 'Cost': ' ', 'Response': '<1s', 'Use For': 'Simple,
learning'},
{'Size': '70-120B', 'Speed': ' ', 'Quality': ' ', 'Cost': ' ', 'Response': '2-4s', 'Use For':
'Production'},
{'Size': '405B+', 'Speed': ' ', 'Quality': ' ', 'Cost': ' ', 'Response': '6-8s', 'Use For':
'Critical'}
])
st.dataframe(df_ params, use_container_width=True, hide_ index=True)
with learn_tabs[3]:
st.markdown("### Databricks Assistant")
st.success("The Databricks Assistant is built into notebooks and understands your workspace context!")
col1, col2 = st.columns(2)
with col1:
st.markdown("** What It Knows:**")
st.markdown("- Current notebook cells & variables")
st.markdown("- Your table schemas (Unity Catalog)")
st.markdown("- Available databases & tables")
st.markdown("- Spark configuration")
with col2:
st.markdown("** Best Use Cases:**")
st.markdown("- Quick SQL quer y generation")
st.markdown("- Explain existing code")
st.markdown("- Debug PySpark errors")
st.markdown("- Generate test data")
st.info("**When to use DB Assistant:** Quick queries in notebook, context-aware help, cost is a concern
(FREE)")
st.warning("**When to use other models:** Complex reasoning (>2000 thinking tokens), large codebase
analysis, system design")
# ============================================================================
# TAB 3: CALCUL ATOR
# ============================================================================
with tab3:
st.markdown("## Cost Calculator")
calc_col1, calc_col2 = st.columns(2)
with calc_col1:
st.markdown("### Scenario Settings")
selected _ model = st.selectbox(
"Select Model",
list(filtered.keys()),
format_func=lambda x: filtered[x]['name']
)
num_ requests = st.number_ input("Number of Requests", 1, 1000000, 1000, 100)
avg _ input = st.number_ input("Avg Input Tokens", 10, 100000, 500, 50)
avg _output = st.number_ input("Avg Output Tokens", 10, 10000, 500, 50)
m = filtered[selected _ model]
thinking = st.number_ input(
"Thinking Tokens",
0,
m['thinking _ max'],
0,
100,
disabled=(m['thinking _ max'] == 0)
)
with calc_col2:
st.markdown("### Cost Results")
total _ input = (avg _ input + thinking) * num_ requests
total _output = avg _output * num_ requests
cost_ input = (total _ input / 1000) * m['cost_ in']
cost_output = (total _output / 1000) * m['cost_out']
total _cost = cost_ input + cost_output
total _time = num_ requests * m['response_time']
time_hours = total _time / 3600
# Display metrics
c1, c2 = st.columns(2)
c1.metric("Input Cost", f"${cost_ input:.2f}")
c2.metric("Output Cost", f"${cost_output:.2f}")
st.metric(" TOTAL COST", f"${total _cost:.2f}", delta=f"{total _ input + total _output:,} tokens")
c3, c4 = st.columns(2)
c3.metric("Total Time", f"{time_hours:.2f} hours" if time_hours > 1 else f"{total _time:.0f}s")
c4.metric("Per Request", f"{m['response_time']}s")
st.markdown("---")
st.markdown("### Cost Comparison")
comparison = []
for mid, model in filtered.items():
m_ input = ((avg _ input + (thinking if model['thinking _ max'] > 0 else 0)) * num_ requests / 1000) *
model['cost_ in']
m_output = (avg _output * num_ requests / 1000) * model['cost_out']
m_total = m_ input + m_output
m_time = num_ requests * model['response_time']
comparison.append({
'Model': model['name'],
'Total Cost': m_total,
'Time (hrs)': m_time / 3600
})
df_comp = pd.DataFrame(comparison).sor t_values('Total Cost')
fig = go.Figure()
fig.add _trace(go.Bar(
name='Cost',
x=df_comp['Model'],
y=df_comp['Total Cost'],
marker_color=RED_PRIMARY,
text=[f"${x:.2f}" for x in df_comp['Total Cost']],
textposition='outside'
))
fig.update_layout(
title=f"Cost Comparison for {num_ requests:,} Requests",
xaxis_title="",
yaxis_title="Cost ($)",
template='plotly_dark',
height=400
)
st.plotly_char t(fig, use_container_width=True)
# ============================================================================
# TAB 4: EDIT
# ============================================================================
with tab4:
st.markdown("## Edit Models")
edit_ model = st.selectbox(
"Select Model to Edit",
list(st.session_state.models.keys()),
format_func=lambda x: st.session_state.models[x]['name']
)
m = st.session_state.models[edit_ model]
c1, c2 = st.columns(2)
with c1:
st.markdown("### Basic Info")
new_ name = st.text_ input("Name", m['name'])
new_ provider = st.selectbox("Provider", ['Meta', 'Anthropic', 'Databricks', 'Google'],
index=['Meta', 'Anthropic', 'Databricks', 'Google'].index(m['provider']))
new_ params = st.text_ input("Parameters", m['params'])
new_context = st.number_ input("Context Length", value=m['context'], step=1000)
new_thinking = st.number_ input("Max Thinking", value=m['thinking _ max'], step=100)
new_ response_time = st.number_ input("Response Time (sec)", value=m['response_time'], step=0.1,
format="%.1f")
with c2:
st.markdown("### Per formance")
new_cost_ in = st.number_ input("Cost In ($/1K)", value=m['cost_ in'], format="%.6f", step=0.0001)
new_cost_out = st.number_ input("Cost Out ($/1K)", value=m['cost_out'], format="%.6f", step=0.0001)
new_coding = st.slider("Coding Score", 0.0, 10.0, m['coding'], 0.5)
new_speed = st.slider("Speed Score", 0, 10, m['speed'])
new_value = st.slider("Value Score", 0, 10, m['value'])
if st.button(" Save Changes", use_container_width=True):
st.session_state.models[edit_ model].update({
'name': new_ name,
'provider': new_ provider,
'params': new_ params,
'context': new_context,
'thinking _ max': new_thinking,
'response_time': new_ response_time,
'cost_ in': new_cost_ in,
'cost_out': new_cost_out,
'coding': new_coding,
'speed': new_speed,
'value': new_value
})
st.success(" Model updated successfully!")
st.rerun()
# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
st.markdown(f"""
<div style="text-align: center; padding: 20px;">
<div style="font-size: 24px; color: {RED_PRIMARY}; margin-bottom: 10px;"> </div>
<p style="margin: 5px 0; color: {RED_PRIMARY}; font-weight: 700;">CIBC Analytics</p>
<p style="margin: 5px 0; font-size: 12px; color: {GRAY_LIGHT};">
Databricks AI Model Dashboard | {datetime.now().str ftime("%Y-%m-%d %H:%M")}
</p>
<p style="margin: 5px 0; font-size: 11px; color: {GRAY_LIGHT};">
Displaying {len(filtered)} of {len(st.session_state.models)} models
</p>
</div>
""", unsafe_allow_html=True)
