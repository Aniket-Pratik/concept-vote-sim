import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from typing import Dict, Any, List
import time

# Page config
st.set_page_config(
    page_title="Concept Vote Simulator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
/* Global styles */
.main {
    padding: 0;
}

/* Top bar styling */
.top-bar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding: 1rem 0;
    margin-bottom: 2rem;
}

.dark .top-bar {
    background: rgba(0, 0, 0, 0.95);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* Card styling */
.card {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
}

.dark .card {
    background: #1a1a1a;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-1px);
}

/* Gradient button */
.gradient-btn {
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
    border: none;
    color: white;
    padding: 0.75rem 2rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.gradient-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.gradient-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

/* Sticky run bar */
.run-bar {
    position: sticky;
    top: 80px;
    z-index: 999;
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dark .run-bar {
    background: #1a1a1a;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
}

.dark .kpi-card {
    background: linear-gradient(135deg, #1e293b, #334155);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Option pills */
.option-pill {
    display: inline-block;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 0.5rem 1rem;
    margin: 0.25rem;
    font-size: 0.9rem;
    color: #475569;
}

.dark .option-pill {
    background: #334155;
    border: 1px solid #475569;
    color: #e2e8f0;
}

/* Status indicators */
.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 0.5rem;
}

.status-connected {
    background: #10b981;
}

.status-disconnected {
    background: #ef4444;
}

/* Progress bar */
.progress-container {
    background: #e2e8f0;
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.progress-bar {
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
}

/* Help tooltips */
.help-text {
    color: #6b7280;
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

.dark .help-text {
    color: #9ca3af;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .card {
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .run-bar {
        position: fixed;
        bottom: 1rem;
        left: 1rem;
        right: 1rem;
        top: auto;
        z-index: 1001;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# API configuration
API = os.getenv("API_BASE", "http://localhost:8001")

def check_api_health():
    """Check if the API is connected"""
    try:
        response = requests.get(f"{API}/healthz", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_vote_test(question, brief, options, mode, rule, n_voters, persona_source, temperature, seed=None):
    """Run the vote test and return results"""
    payload = {
        "question": question,
        "brief": brief,
        "options": options,
        "mode": mode,
        "rule": rule,
        "n_voters": n_voters,
        "persona_source": persona_source,
        "temperature": temperature
    }
    
    if seed:
        payload["seed"] = seed
    
    try:
        response = requests.post(f"{API}/v1/concept/vote", json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def create_bar_chart(data, title):
    """Create a bar chart for vote results"""
    if not data:
        return None
    
    df = pd.DataFrame([
        {"Option": k, "Count": v} for k, v in data.items()
    ])
    
    fig = px.bar(
        df, 
        x="Option", 
        y="Count",
        title=title,
        color="Count",
        color_continuous_scale="viridis"
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_condorcet_matrix(data, options):
    """Create a pairwise comparison matrix for Condorcet results"""
    if not data or rule != "condorcet":
        return None
    
    # Create matrix data
    matrix_data = []
    for i, opt1 in enumerate(options):
        row = []
        for j, opt2 in enumerate(options):
            if i == j:
                row.append(0)
            else:
                key = f"{opt1} vs {opt2}"
                value = data.get(key, 0)
                row.append(value)
        matrix_data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=options,
        y=options,
        colorscale='RdBu',
        zmid=0,
        text=[[f"{val}" for val in row] for row in matrix_data],
        texttemplate="%{text}",
        textfont={"size": 12}
    ))
    
    fig.update_layout(
        title="Pairwise Comparison Matrix",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def export_to_csv(tallies, options):
    """Export results to CSV"""
    df = pd.DataFrame([
        {"Option": option, "Count": tallies.get(option, 0)} 
        for option in options
    ])
    return df.to_csv(index=False)

def export_to_json(data):
    """Export results to JSON"""
    return json.dumps(data, indent=2)

# Main app
def main():
    # Top Bar (Sticky)
    st.markdown("""
    <div class="top-bar">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
            <div>
                <h1 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #1f2937;">🧪 Concept Vote Simulator</h1>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">AI-powered concept testing with diverse personas</p>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <!-- API status moved to fixed position indicator -->
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status indicator in top right corner
    if check_api_health():
        st.markdown("""
        <div style="position: fixed; top: 20px; right: 20px; z-index: 1001;">
            <div style="background: #10b981; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                🟢 API Connected
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="position: fixed; top: 20px; right: 20px; z-index: 1001;">
            <div style="background: #ef4444; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                🔴 API Offline
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Two-pane layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Configuration")
        
        # Persona Source
        persona_source = st.selectbox(
            "Persona Source",
            ["synthetic", "personahub", "genz_synthetic"],
            format_func=lambda x: {
                "synthetic": "General Synthetic",
                "personahub": "PersonaHub",
                "genz_synthetic": "Gen Z Synthetic"
            }[x],
            help="Choose the source for generating voter personas"
        )
        
        if persona_source == "genz_synthetic":
            st.info("🎯 Using specialized Gen Z personas (18-25, social media savvy, bold & playful)")
        
        # Voting Mode
        mode = st.selectbox(
            "Voting Mode",
            ["forced_choice", "approval", "ranking"],
            format_func=lambda x: {
                "forced_choice": "Forced Choice",
                "approval": "Approval",
                "ranking": "Ranking"
            }[x],
            help="Forced Choice: Pick one best option\nApproval: Pick any acceptable options\nRanking: Rank all options in order"
        )
        
        # Counting Rule
        rule = st.selectbox(
            "Counting Rule",
            ["plurality", "approval", "borda", "condorcet"],
            format_func=lambda x: {
                "plurality": "Plurality",
                "approval": "Approval",
                "borda": "Borda",
                "condorcet": "Condorcet"
            }[x],
            help="Plurality: Most first-place votes wins\nApproval: Most approvals wins\nBorda: Points-based ranking system\nCondorcet: Pairwise comparison winner"
        )
        
        # Number of Voters
        n_voters = st.slider("Number of Voters", 5, 200, 15, help="More voters = more reliable results but slower processing")
        
        # Temperature
        temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.6, 0.1, help="Higher = more creative/varied responses, Lower = more consistent")
        
        # Seed (optional)
        seed = st.number_input("Seed (optional)", min_value=1, help="Fixed seed for reproducible results")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Concept Details Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🧪 Concept Details")
        
        question = st.text_input(
            "What are you testing?",
            value="Which color should we choose for our new energy drink?",
            help="Be specific about what you want to test"
        )
        
        brief = st.text_area(
            "Brand Brief & Context",
            value="Target audience: Gen Z consumers aged 18-25 who are energetic and social media savvy. Brand personality: Bold, playful, and trend-setting. Looking for colors that will stand out on social media and appeal to young adults.",
            height=120,
            help="Describe target audience, brand personality, constraints, and what you're looking for"
        )
        
        options_input = st.text_input(
            "Options to test (comma-separated)",
            value="red, gold, pink, blue, green",
            help="Enter at least 2 options separated by commas"
        )
        
        # Parse options and show as pills
        options = [opt.strip() for opt in options_input.split(",") if opt.strip()]
        if options:
            st.markdown("**Options loaded:**")
            pills_html = " ".join([f'<span class="option-pill">{opt}</span>' for opt in options])
            st.markdown(pills_html, unsafe_allow_html=True)
            st.markdown(f"<small style='color: #10b981;'>{len(options)} options ready</small>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sticky Run Bar
        st.markdown('<div class="run-bar">', unsafe_allow_html=True)
        
        col_run1, col_run2, col_run3 = st.columns([2, 1, 1])
        
        with col_run1:
            run_disabled = len(options) < 2 or not question or not brief
            if st.button(
                "🚀 Run Concept Test",
                disabled=run_disabled,
                use_container_width=True,
                key="run_button"
            ):
                st.session_state.is_running = True
                st.session_state.progress = 0
                
                # Simulate progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(101):
                    time.sleep(0.05)
                    st.session_state.progress = i
                    progress_bar.progress(i)
                    if i < 30:
                        status_text.text("Generating personas...")
                    elif i < 60:
                        status_text.text("Running vote simulation...")
                    elif i < 90:
                        status_text.text("Aggregating results...")
                    else:
                        status_text.text("Finalizing...")
                
                # Run actual test
                results = run_vote_test(
                    question, brief, options, mode, rule, 
                    n_voters, persona_source, temperature, seed
                )
                
                if results:
                    st.session_state.results = results
                    st.success("✅ Concept test completed successfully!")
                else:
                    st.error("❌ Failed to run concept test")
                
                st.session_state.is_running = False
                st.rerun()
        
        with col_run2:
            if st.session_state.is_running:
                st.markdown(f"<div style='text-align: center;'><strong>Running...</strong><br><small>{st.session_state.progress}%</small></div>", unsafe_allow_html=True)
        
        with col_run3:
            if st.session_state.is_running:
                st.markdown('<div class="progress-container"><div class="progress-bar" style="width: {}%"></div></div>'.format(st.session_state.progress), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Results Section
        if st.session_state.results:
            results = st.session_state.results
            
            # KPI Cards Row
            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
            
            with col_kpi1:
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                st.metric("🏆 Winner", results.get('winner', 'N/A'))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_kpi2:
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                st.metric("👥 Sample Size", f"{results.get('sample', 0)} voters")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_kpi3:
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                generated_time = datetime.fromisoformat(results.get('generated_at', '').replace('Z', '+00:00'))
                st.metric("⏰ Generated", generated_time.strftime("%H:%M"))
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Results Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Overview", "👥 Voters", "📋 Methodology"])
            
            with tab1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Vote Results")
                
                # Chart based on rule
                if rule == "condorcet":
                    fig = create_condorcet_matrix(results.get('tallies', {}), options)
                else:
                    fig = create_bar_chart(results.get('tallies', {}), f"Vote Counts - {rule.title()}")
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Distribution list
                if results.get('tallies'):
                    st.markdown("**Distribution:**")
                    total = sum(results['tallies'].values())
                    for option, count in results['tallies'].items():
                        percentage = (count / total * 100) if total > 0 else 0
                        st.markdown(f"• **{option}**: {count} ({percentage:.1f}%)")
                
                # Download buttons
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    csv_data = export_to_csv(results.get('tallies', {}), options)
                    st.download_button(
                        "📥 Download CSV",
                        csv_data,
                        "concept-vote-results.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col_dl2:
                    json_data = export_to_json(results)
                    st.download_button(
                        "📥 Download JSON",
                        json_data,
                        "concept-vote-results.json",
                        "application/json",
                        use_container_width=True
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Individual Voter Responses")
                
                voters = results.get('voters', [])
                if voters:
                    # Show first 50 voters
                    display_voters = voters[:50]
                    
                    for i, voter in enumerate(display_voters):
                        with st.expander(f"Voter {voter['id']} - {voter['selection'][0] if voter['selection'] else 'No selection'}"):
                            col_v1, col_v2 = st.columns([1, 1])
                            
                            with col_v1:
                                st.markdown(f"**Selection:** {', '.join(voter['selection'])}")
                                st.markdown(f"**Confidence:** {voter['confidence']:.2f}")
                            
                            with col_v2:
                                if voter.get('scores'):
                                    st.markdown("**Per-option scores:**")
                                    for option, score in voter['scores'].items():
                                        st.progress(score)
                                        st.caption(f"{option}: {score:.2f}")
                            
                            st.markdown(f"**Justification:** {voter['justification']}")
                    
                    if len(voters) > 50:
                        st.info(f"Showing first 50 of {len(voters)} voters. Use the API directly for full results.")
                else:
                    st.info("No voter data available")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Methodology & Notes")
                
                st.markdown(f"""
                **Test Configuration:**
                - **Mode:** {mode.replace('_', ' ').title()}
                - **Rule:** {rule.title()}
                - **Persona Source:** {persona_source.replace('_', ' ').title()}
                - **Temperature:** {temperature}
                - **Voters:** {n_voters}
                """)
                
                if results.get('notes'):
                    st.markdown(f"**Additional Notes:** {results['notes']}")
                
                st.markdown("""
                **Disclaimer:** Results are generated by AI personas and should be used as directional guidance, not definitive consumer research.
                """)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Empty State
        elif not st.session_state.is_running:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("""
            ### 🚀 Ready to Test Your Concepts?
            
            Fill in the concept details on the left and click **Run Concept Test** to get started.
            
            The AI will generate diverse personas and simulate their voting behavior based on your brand brief.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
