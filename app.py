import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="CIBC Databricks AI Dashboard",
    page_icon="🏦",
    layout="wide"
)

# ============================================================================
# CIBC COLORS - Dark Mode Only
# ============================================================================
RED_PRIMARY = "#ED1B2E"
RED_DARK = "#C8102E"
RED_LIGHT = "#FF5252"
ORANGE = "#FF6B35"
GOLD = "#FFB800"
GRAY_DARK = "#1A1A1A"
GRAY_MED = "#2D2D2D"
GRAY_LIGHT = "#CCCCCC"
WHITE = "#FFFFFF"

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
            'output_max': 4096,
            'thinking_max': 0,
            'cost_in': 0.0,
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
            'output_max': 4096,
            'thinking_max': 4000,
            'cost_in': 0.003,
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
            'output_max': 4096,
            'thinking_max': 2000,
            'cost_in': 0.0006,
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
            'output_max': 4096,
            'thinking_max': 0,
            'cost_in': 0.0001,
            'cost_out': 0.0001,
            'coding': 6.5,
            'speed': 10,
            'value': 10,
            'response_time': 0.8,
            'best': ['Quick scripts', 'Learning', 'High volume'],
            'avoid': ['Complex reasoning', 'Critical systems']
        },
        'llama_maverick': {
            'name': 'Llama 4 Maverick',
            'provider': 'Meta',
            'params': '~100B',
            'context': 128000,
            'output_max': 4096,
            'thinking_max': 2000,
            'cost_in': 0.0008,
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
            'params': 'Proprietary',
            'context': 200000,
            'output_max': 8192,
            'thinking_max': 0,
            'cost_in': 0.015,
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
            'params': 'Proprietary',
            'context': 200000,
            'output_max': 8192,
            'thinking_max': 3000,
            'cost_in': 0.015,
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
            'params': 'Proprietary',
            'context': 200000,
            'output_max': 8192,
            'thinking_max': 2500,
            'cost_in': 0.003,
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
            'params': 'Proprietary',
            'context': 200000,
            'output_max': 8192,
            'thinking_max': 2000,
            'cost_in': 0.003,
            'cost_out': 0.015,
            'coding': 10.0,
            'speed': 8,
            'value': 9,
            'response_time': 2.8,
            'best': ['Production dev', 'Balanced performance'],
            'avoid': ['Budget critical']
        },
        'claude_sonnet_37': {
            'name': 'Claude Sonnet 3.7',
            'provider': 'Anthropic',
            'params': 'Proprietary',
            'context': 200000,
            'output_max': 8192,
            'thinking_max': 1500,
            'cost_in': 0.003,
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
            'output_max': 4096,
            'thinking_max': 1000,
            'cost_in': 0.0005,
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
            'output_max': 4096,
            'thinking_max': 500,
            'cost_in': 0.0002,
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
            'output_max': 2048,
            'thinking_max': 500,
            'cost_in': 0.0001,
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
        color: {RED_PRIMARY} !important;
        font-weight: 700 !important;
    }}
    
    .stButton > button {{
        background-color: {RED_PRIMARY} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 30px !important;
        transition: all 0.3s !important;
    }}
    
    .stButton > button:hover {{
        background-color: {RED_DARK} !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(237, 27, 46, 0.4) !important;
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
        background-color: {RED_PRIMARY} !important;
        color: white !important;
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
        color: {GRAY_LIGHT} !important;
        font-size: 14px !important;
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        color: {RED_PRIMARY} !important;
        font-size: 32px !important;
        font-weight: 800 !important;
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
            🏦
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
    st.markdown(f"## 🎛️ Controls")
    
    st.markdown("### Filter Models")
    
    providers = ['Meta', 'Anthropic', 'Databricks', 'Google']
    selected_providers = st.multiselect(
        "Select Providers",
        providers,
        default=providers
    )
    
    min_score = st.slider("Min Coding Score", 0.0, 10.0, 0.0, 0.5)
    max_cost = st.slider("Max Cost ($/1K)", 0.0, 0.5, 0.5, 0.01, format="%.4f")
    only_thinking = st.checkbox("Only Thinking Token Models")
    max_response_time = st.slider("Max Response Time (sec)", 0.0, 10.0, 10.0, 0.5)
    
    st.markdown("---")
    
    st.markdown("### 💾 Export Data")
    
    if st.button("📥 Export JSON"):
        json_str = json.dumps(st.session_state.models, indent=2)
        st.download_button(
            "Download",
            json_str,
            f"models_{datetime.now().strftime('%Y%m%d')}.json",
            "application/json"
        )
    
    st.markdown("---")
    
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; 
                    background: linear-gradient(135deg, {RED_PRIMARY}30, {ORANGE}20);
                    border-radius: 10px; border: 2px solid {RED_PRIMARY};">
            <div style="font-size: 28px; margin-bottom: 10px;">🏦</div>
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
    if v['provider'] in selected_providers
    and v['coding'] >= min_score
    and v['cost_in'] <= max_cost
    and (not only_thinking or v['thinking_max'] > 0)
    and v['response_time'] <= max_response_time
}

# ============================================================================
# KEY METRICS
# ============================================================================
st.markdown("## 📊 Dashboard Overview")

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.metric("Total Models", len(filtered), delta=f"{len(st.session_state.models)} total")

with m2:
    avg_cost = sum([m['cost_in'] for m in filtered.values()]) / len(filtered) if filtered else 0
    st.metric("Avg Cost/1K", f"${avg_cost:.4f}")

with m3:
    thinking_count = sum([1 for m in filtered.values() if m['thinking_max'] > 0])
    st.metric("With Thinking", thinking_count)

with m4:
    avg_coding = sum([m['coding'] for m in filtered.values()]) / len(filtered) if filtered else 0
    st.metric("Avg Coding", f"{avg_coding:.1f}/10")

with m5:
    avg_response = sum([m['response_time'] for m in filtered.values()]) / len(filtered) if filtered else 0
    st.metric("Avg Response", f"{avg_response:.1f}s")

st.markdown("---")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["🤖 Models", "📚 Learn", "💰 Calculator", "✏️ Edit"])

# ============================================================================
# TAB 1: MODELS - Visual Comparison + Detailed Cards
# ============================================================================
with tab1:
    st.markdown("## 🤖 Model Comparison & Details")
    
    if not filtered:
        st.warning("⚠️ No models match your filters. Adjust settings in sidebar.")
    else:
        # Highlight Databricks Assistant
        if 'databricks_assistant' in filtered:
            st.info("⚡ **Databricks Assistant** is optimized for quick notebook queries with full context awareness. It's **FREE** with your workspace!")
        
        st.markdown("---")
        st.markdown("### 📊 Quick Comparison")
        
        # Create comparison dataframe
        comparison_data = []
        for model_id, m in filtered.items():
            comparison_data.append({
                'Model': m['name'],
                'Provider': m['provider'],
                'Params': m['params'],
                'Coding': m['coding'],
                'Speed': m['speed'],
                'Value': m['value'],
                'Cost': m['cost_in'],
                'Response': m['response_time'],
                'Thinking': m['thinking_max'],
                'Context': m['context']
            })
        
        df_compare = pd.DataFrame(comparison_data)
        
        # Interactive comparison table
        st.dataframe(
            df_compare.style.background_gradient(subset=['Coding', 'Speed', 'Value'], cmap='Reds')
                            .format({'Cost': '${:.4f}', 'Response': '{:.1f}s', 'Thinking': '{:,}', 'Context': '{:,}'}),
            use_container_width=True,
            height=300
        )
        
        st.markdown("---")
        
        # Visual comparisons in tabs
        compare_tabs = st.tabs(["📊 Scores", "💰 Cost & Speed", "🧠 Capabilities"])
        
        with compare_tabs[0]:
            # Scores comparison
            fig_scores = go.Figure()
            
            fig_scores.add_trace(go.Bar(
                name='Coding',
                x=[m['name'] for m in filtered.values()],
                y=[m['coding'] for m in filtered.values()],
                marker_color=RED_PRIMARY,
                text=[f"{m['coding']:.1f}" for m in filtered.values()],
                textposition='outside'
            ))
            
            fig_scores.add_trace(go.Bar(
                name='Speed',
                x=[m['name'] for m in filtered.values()],
                y=[m['speed'] for m in filtered.values()],
                marker_color=ORANGE,
                text=[f"{m['speed']}" for m in filtered.values()],
                textposition='outside'
            ))
            
            fig_scores.add_trace(go.Bar(
                name='Value',
                x=[m['name'] for m in filtered.values()],
                y=[m['value'] for m in filtered.values()],
                marker_color=GOLD,
                text=[f"{m['value']}" for m in filtered.values()],
                textposition='outside'
            ))
            
            fig_scores.update_layout(
                title="Performance Scores Comparison (0-10)",
                xaxis_title="",
                yaxis_title="Score",
                barmode='group',
                template='plotly_dark',
                height=450,
                yaxis=dict(range=[0, 11]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig_scores, use_container_width=True)
        
        with compare_tabs[1]:
            # Cost and response time
            col1, col2 = st.columns(2)
            
            with col1:
                fig_cost = go.Figure()
                
                colors_cost = [RED_PRIMARY if m['cost_in'] == 0 else ORANGE for m in filtered.values()]
                
                fig_cost.add_trace(go.Bar(
                    x=[m['name'] for m in filtered.values()],
                    y=[m['cost_in'] * 1000 for m in filtered.values()],
                    marker_color=colors_cost,
                    text=[f"${m['cost_in']:.4f}" if m['cost_in'] > 0 else "FREE" for m in filtered.values()],
                    textposition='outside'
                ))
                
                fig_cost.update_layout(
                    title="Input Cost per 1K Tokens",
                    xaxis_title="",
                    yaxis_title="Cost ($)",
                    template='plotly_dark',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_cost, use_container_width=True)
            
            with col2:
                fig_time = go.Figure()
                
                colors_time = [RED_PRIMARY if m['response_time'] < 2 else (ORANGE if m['response_time'] < 4 else GOLD) for m in filtered.values()]
                
                fig_time.add_trace(go.Bar(
                    x=[m['name'] for m in filtered.values()],
                    y=[m['response_time'] for m in filtered.values()],
                    marker_color=colors_time,
                    text=[f"{m['response_time']}s" for m in filtered.values()],
                    textposition='outside'
                ))
                
                fig_time.update_layout(
                    title="Response Time",
                    xaxis_title="",
                    yaxis_title="Seconds",
                    template='plotly_dark',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_time, use_container_width=True)
        
        with compare_tabs[2]:
            # Capabilities (thinking tokens and context)
            col1, col2 = st.columns(2)
            
            with col1:
                fig_thinking = go.Figure()
                
                thinking_models = [(m['name'], m['thinking_max']) for m in filtered.values() if m['thinking_max'] > 0]
                
                if thinking_models:
                    fig_thinking.add_trace(go.Bar(
                        x=[m[0] for m in thinking_models],
                        y=[m[1] for m in thinking_models],
                        marker_color=RED_PRIMARY,
                        text=[f"{m[1]:,}" for m in thinking_models],
                        textposition='outside'
                    ))
                    
                    fig_thinking.update_layout(
                        title="Max Thinking Tokens",
                        xaxis_title="",
                        yaxis_title="Tokens",
                        template='plotly_dark',
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_thinking, use_container_width=True)
                else:
                    st.info("No models with thinking tokens in current filter")
            
            with col2:
                fig_context = go.Figure()
                
                fig_context.add_trace(go.Bar(
                    x=[m['name'] for m in filtered.values()],
                    y=[m['context'] / 1000 for m in filtered.values()],
                    marker_color=ORANGE,
                    text=[f"{m['context']//1000}K" for m in filtered.values()],
                    textposition='outside'
                ))
                
                fig_context.update_layout(
                    title="Context Window Size",
                    xaxis_title="",
                    yaxis_title="Tokens (K)",
                    template='plotly_dark',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_context, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📋 Detailed Model Information")
        st.caption("Expand each card for complete details")
        
        # Display detailed model cards
        for idx, (model_id, m) in enumerate(filtered.items()):
            # Create expandable card for each model
            with st.expander(f"{'⭐ ' if model_id == 'databricks_assistant' else ''}{m['name']} - {m['params']}", expanded=False):
                # Provider and basic info
                col_info, col_metrics = st.columns([1, 2])
                
                with col_info:
                    st.markdown(f"**Provider:** {m['provider']}")
                    st.markdown(f"**Parameters:** {m['params']}")
                    st.markdown(f"**Context:** {m['context']:,} tokens")
                    st.markdown(f"**Max Output:** {m['output_max']:,} tokens")
                    
                    if m['thinking_max'] > 0:
                        st.markdown(f"**🧠 Thinking Tokens:** {m['thinking_max']:,}")
                    
                    if model_id == 'databricks_assistant':
                        st.markdown("**📓 Notebook Context Aware**")
                
                with col_metrics:
                    # Metrics in columns
                    mc1, mc2, mc3, mc4 = st.columns(4)
                    
                    with mc1:
                        st.metric("Coding", f"{m['coding']}/10")
                    
                    with mc2:
                        cost_display = "FREE" if m['cost_in'] == 0 else f"${m['cost_in']:.4f}"
                        st.metric("Cost/1K", cost_display)
                    
                    with mc3:
                        st.metric("Speed", f"{m['speed']}/10")
                    
                    with mc4:
                        if m['response_time'] <= 2:
                            speed_label = "⚡⚡⚡"
                        elif m['response_time'] <= 4:
                            speed_label = "⚡⚡"
                        else:
                            speed_label = "⚡"
                        st.metric("Response", f"{m['response_time']}s", delta=speed_label)
                
                # Best for / Avoid
                col_best, col_avoid = st.columns(2)
                
                with col_best:
                    st.markdown(f"**✅ BEST FOR:**")
                    for item in m['best'][:3]:
                        st.markdown(f"- {item}")
                
                with col_avoid:
                    st.markdown(f"**❌ AVOID FOR:**")
                    for item in m['avoid'][:2]:
                        st.markdown(f"- {item}")
# ============================================================================
# TAB 2: LEARN
# ============================================================================
with tab2:
    st.markdown("## 📚 Educational Guide")
    
    learn_tabs = st.tabs(["🧠 Reasoning", "💭 Thinking Tokens", "📏 Parameters", "📓 DB Assistant"])
    
    with learn_tabs[0]:
        st.markdown("### What is a Reasoning Model?")
        st.info("A reasoning model thinks step-by-step before answering. It breaks down complex tasks, considers alternatives, and validates logic.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**❌ Without Reasoning**")
            st.code("""
User: Optimize this query
Model: Here's the query
(may miss issues)
            """)
        
        with col2:
            st.markdown("**✅ With Reasoning**")
            st.code("""
User: Optimize this query
Model: [Analyzes joins...]
       [Checks partitions...]
Here's why this works...
            """)
        
        st.markdown("### 🎯 Reasoning Models Available")
        reasoning_models = {k: v for k, v in filtered.items() if v['thinking_max'] > 0}
        
        for model_id, m in reasoning_models.items():
            st.success(f"**{m['name']}** - 🧠 {m['thinking_max']} thinking tokens")
    
    with learn_tabs[1]:
        st.markdown("### What are Thinking Tokens?")
        st.info("Thinking tokens are the model's internal dialogue before responding. You set a budget (e.g., 4000) for how much thinking space it gets.")
        
        thinking_budget = st.slider("Set Thinking Budget", 0, 4000, 2000, 500)
        
        c1, c2, c3 = st.columns(3)
        
        quality = min(10, (thinking_budget / 400) + 5)
        c1.metric("Expected Quality", f"{quality:.1f}/10")
        
        time = 1 + (thinking_budget / 1000)
        c2.metric("Response Time", f"{time:.1f}s")
        
        cost = 1 + (thinking_budget / 1000)
        c3.metric("Cost Multiplier", f"{cost:.1f}x")
        
        st.warning(f"**Cost Impact:** Thinking tokens cost the same as input! {thinking_budget} thinking + 500 output = {thinking_budget + 500} total tokens")
        
        st.markdown("### 📋 Recommended Settings")
        df_thinking = pd.DataFrame([
            {'Task': 'Simple query', 'Tokens': '0-500', 'Example': 'Basic SELECT'},
            {'Task': 'Medium task', 'Tokens': '1000-1500', 'Example': 'Optimize JOIN'},
            {'Task': 'Complex', 'Tokens': '2000-3000', 'Example': 'Design pipeline'},
            {'Task': 'Critical', 'Tokens': '4000', 'Example': 'Architecture review'}
        ])
        st.dataframe(df_thinking, use_container_width=True, hide_index=True)
    
    with learn_tabs[2]:
        st.markdown("### Understanding Parameters")
        st.info("Parameters are the model's brain cells. More = smarter but slower and more expensive.")
        
        df_params = pd.DataFrame([
            {'Size': '8-12B', 'Speed': '⚡⚡⚡⚡⚡', 'Quality': '⭐⭐⭐', 'Cost': '💰', 'Response': '<1s', 'Use For': 'Simple, learning'},
            {'Size': '70-120B', 'Speed': '⚡⚡⚡', 'Quality': '⭐⭐⭐⭐', 'Cost': '💰💰', 'Response': '2-4s', 'Use For': 'Production'},
            {'Size': '405B+', 'Speed': '⚡', 'Quality': '⭐⭐⭐⭐⭐', 'Cost': '💰💰💰', 'Response': '6-8s', 'Use For': 'Critical'}
        ])
        st.dataframe(df_params, use_container_width=True, hide_index=True)
    
    with learn_tabs[3]:
        st.markdown("### 📓 Databricks Assistant")
        st.success("The Databricks Assistant is built into notebooks and understands your workspace context!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ What It Knows:**")
            st.markdown("- 📓 Current notebook cells & variables")
            st.markdown("- 📊 Your table schemas (Unity Catalog)")
            st.markdown("- 🗃️ Available databases & tables")
            st.markdown("- ⚡ Spark configuration")
        
        with col2:
            st.markdown("**🎯 Best Use Cases:**")
            st.markdown("- Quick SQL query generation")
            st.markdown("- Explain existing code")
            st.markdown("- Debug PySpark errors")
            st.markdown("- Generate test data")
        
        st.info("**When to use DB Assistant:** Quick queries in notebook, context-aware help, cost is a concern (FREE)")
        st.warning("**When to use other models:** Complex reasoning (>2000 thinking tokens), large codebase analysis, system design")

# ============================================================================
# TAB 3: CALCULATOR
# ============================================================================
with tab3:
    st.markdown("## 💰 Cost Calculator")
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        st.markdown("### 📊 Scenario Settings")
        
        selected_model = st.selectbox(
            "Select Model",
            list(filtered.keys()),
            format_func=lambda x: filtered[x]['name']
        )
        
        num_requests = st.number_input("Number of Requests", 1, 1000000, 1000, 100)
        avg_input = st.number_input("Avg Input Tokens", 10, 100000, 500, 50)
        avg_output = st.number_input("Avg Output Tokens", 10, 10000, 500, 50)
        
        m = filtered[selected_model]
        thinking = st.number_input(
            "Thinking Tokens",
            0,
            m['thinking_max'],
            0,
            100,
            disabled=(m['thinking_max'] == 0)
        )
    
    with calc_col2:
        st.markdown("### 💵 Cost Results")
        
        total_input = (avg_input + thinking) * num_requests
        total_output = avg_output * num_requests
        
        cost_input = (total_input / 1000) * m['cost_in']
        cost_output = (total_output / 1000) * m['cost_out']
        total_cost = cost_input + cost_output
        
        total_time = num_requests * m['response_time']
        time_hours = total_time / 3600
        
        # Display metrics
        c1, c2 = st.columns(2)
        c1.metric("Input Cost", f"${cost_input:.2f}")
        c2.metric("Output Cost", f"${cost_output:.2f}")
        
        st.metric("💰 TOTAL COST", f"${total_cost:.2f}", delta=f"{total_input + total_output:,} tokens")
        
        c3, c4 = st.columns(2)
        c3.metric("Total Time", f"{time_hours:.2f} hours" if time_hours > 1 else f"{total_time:.0f}s")
        c4.metric("Per Request", f"{m['response_time']}s")
    
    st.markdown("---")
    st.markdown("### 📊 Cost Comparison")
    
    comparison = []
    for mid, model in filtered.items():
        m_input = ((avg_input + (thinking if model['thinking_max'] > 0 else 0)) * num_requests / 1000) * model['cost_in']
        m_output = (avg_output * num_requests / 1000) * model['cost_out']
        m_total = m_input + m_output
        m_time = num_requests * model['response_time']
        comparison.append({
            'Model': model['name'], 
            'Total Cost': m_total,
            'Time (hrs)': m_time / 3600
        })
    
    df_comp = pd.DataFrame(comparison).sort_values('Total Cost')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Cost',
        x=df_comp['Model'],
        y=df_comp['Total Cost'],
        marker_color=RED_PRIMARY,
        text=[f"${x:.2f}" for x in df_comp['Total Cost']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"Cost Comparison for {num_requests:,} Requests",
        xaxis_title="",
        yaxis_title="Cost ($)",
        template='plotly_dark',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4: EDIT
# ============================================================================
with tab4:
    st.markdown("## ✏️ Edit Models")
    
    edit_model = st.selectbox(
        "Select Model to Edit",
        list(st.session_state.models.keys()),
        format_func=lambda x: st.session_state.models[x]['name']
    )
    
    m = st.session_state.models[edit_model]
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 📋 Basic Info")
        new_name = st.text_input("Name", m['name'])
        new_provider = st.selectbox("Provider", ['Meta', 'Anthropic', 'Databricks', 'Google'], 
                                   index=['Meta', 'Anthropic', 'Databricks', 'Google'].index(m['provider']))
        new_params = st.text_input("Parameters", m['params'])
        new_context = st.number_input("Context Length", value=m['context'], step=1000)
        new_thinking = st.number_input("Max Thinking", value=m['thinking_max'], step=100)
        new_response_time = st.number_input("Response Time (sec)", value=m['response_time'], step=0.1, format="%.1f")
    
    with c2:
        st.markdown("### 💰 Performance")
        new_cost_in = st.number_input("Cost In ($/1K)", value=m['cost_in'], format="%.6f", step=0.0001)
        new_cost_out = st.number_input("Cost Out ($/1K)", value=m['cost_out'], format="%.6f", step=0.0001)
        new_coding = st.slider("Coding Score", 0.0, 10.0, m['coding'], 0.5)
        new_speed = st.slider("Speed Score", 0, 10, m['speed'])
        new_value = st.slider("Value Score", 0, 10, m['value'])
    
    if st.button("💾 Save Changes", use_container_width=True):
        st.session_state.models[edit_model].update({
            'name': new_name,
            'provider': new_provider,
            'params': new_params,
            'context': new_context,
            'thinking_max': new_thinking,
            'response_time': new_response_time,
            'cost_in': new_cost_in,
            'cost_out': new_cost_out,
            'coding': new_coding,
            'speed': new_speed,
            'value': new_value
        })
        st.success("✅ Model updated successfully!")
        st.rerun()

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col2:
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 24px; color: {RED_PRIMARY}; margin-bottom: 10px;">🏦</div>
            <p style="margin: 5px 0; color: {RED_PRIMARY}; font-weight: 700;">CIBC Analytics</p>
            <p style="margin: 5px 0; font-size: 12px; color: {GRAY_LIGHT};">
                Databricks AI Model Dashboard | {datetime.now().strftime("%Y-%m-%d %H:%M")}
            </p>
            <p style="margin: 5px 0; font-size: 11px; color: {GRAY_LIGHT};">
                Displaying {len(filtered)} of {len(st.session_state.models)} models
            </p>
        </div>
    """, unsafe_allow_html=True)