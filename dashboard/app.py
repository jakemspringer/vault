import os
from datetime import datetime
from html import escape
from pathlib import Path

# Plotly's optional-import checks can observe a partially loaded NumPy module
# when Streamlit sessions start concurrently. Complete its import first.
import numpy  # noqa: F401 -- intentional eager import
import plotly.graph_objects as go
import requests
import streamlit as st

INCOME_COLOR = "#246354"
EXPENSE_COLOR = "#A8C2B5"
FONT = "Arial, Helvetica, sans-serif"
TEXT = "#172F27"
MUTED = "#53675D"


def get_api_url():
    try:
        if "API_URL" in st.secrets:
            return st.secrets["API_URL"].rstrip("/")
    except FileNotFoundError:
        pass
    return os.getenv("API_URL", "http://localhost:8000").rstrip("/")


API_URL = get_api_url()
st.set_page_config(page_title="Vault", layout="wide")
st.html(f"<style>{(Path(__file__).parent / 'style.css').read_text()}</style>")


def api_get(path):
    response = requests.get(f"{API_URL}{path}",
                            headers={"Authorization": f"Bearer {st.session_state.token}"}, timeout=60)
    if response.status_code == 401:
        del st.session_state.token
        st.session_state.login_notice = "Your session expired. Sign in again to continue."
        st.rerun()
    response.raise_for_status()
    return response.json()


def money(value):
    return f"{'−' if value < 0 else ''}${abs(value):,.0f}"


def masthead():
    st.markdown('<header class="vt-masthead"><div class="vt-wordmark">Vault<span>.</span></div>'
                '<span class="vt-workspace">Personal finance / Sample workspace</span></header>',
                unsafe_allow_html=True)


def login_form():
    masthead()
    intro, form = st.columns([1.2, 1], gap="large", vertical_alignment="center")
    with intro:
        st.markdown('<div class="vt-login-intro"><h1>Your finances,<br>in perspective.</h1>'
                    '<p>A clear view of income, spending, and the difference between them.</p>'
                    '<p class="vt-login-note">Explore Vault with generated sample data. '
                    'No personal financial information is used.</p></div>', unsafe_allow_html=True)
    with form:
        with st.container(key="login-panel"):
            st.markdown('<h2>Open your workspace</h2>', unsafe_allow_html=True)
            if notice := st.session_state.pop("login_notice", None):
                st.info(notice)
            with st.form("login", border=False):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign in", type="primary")
            st.markdown('<div class="vt-demo"><span>Try the sample workspace</span>'
                        '<div>Username <code>demo</code> · Password <code>demo123</code></div></div>',
                        unsafe_allow_html=True)
            st.caption("The demo may take about a minute to wake up after inactivity.")
            if submitted:
                if not username.strip() or not password:
                    st.error("Enter your username and password to sign in.")
                    return
                try:
                    with st.spinner("Opening your workspace…"):
                        response = requests.post(f"{API_URL}/login",
                                                 data={"username": username, "password": password}, timeout=60)
                    if response.status_code == 401:
                        st.error("Username or password not recognized. Try the demo credentials below.")
                        return
                    response.raise_for_status()
                    st.session_state.token = response.json()["access_token"]
                    st.rerun()
                except (requests.RequestException, ValueError, KeyError):
                    st.error("Couldn't open the workspace. The demo may be waking up; try again shortly.")


def period_label(rows):
    dates = sorted(datetime.strptime(row["month"], "%Y-%m") for row in rows)
    if dates[0] == dates[-1]:
        return dates[0].strftime("%B %Y")
    return f"{dates[0].strftime('%B %Y')} – {dates[-1].strftime('%B %Y')}"


def summary(rows):
    income = sum(row["income"] for row in rows)
    spending = sum(row["expenses"] for row in rows)
    items = [("Total income", income, "Across the reporting period"),
             ("Total spending", spending, "Across the reporting period"),
             ("Net income", income - spending, "Income less spending")]
    cells = "".join(f'<div class="vt-summary-cell"><dt>{label}</dt><dd>{money(value)}</dd>'
                    f'<span>{detail}</span></div>' for label, value, detail in items)
    st.markdown(f'<dl class="vt-summary">{cells}</dl>', unsafe_allow_html=True)


def section_title(title, description):
    st.markdown(f'<div class="vt-section-title"><h2>{escape(title)}</h2>'
                f'<p>{escape(description)}</p></div>', unsafe_allow_html=True)


def month_chart(rows):
    rows = sorted(rows, key=lambda row: row["month"])
    months = [datetime.strptime(row["month"], "%Y-%m") for row in rows]
    fig = go.Figure([
        go.Bar(name="Income", x=months, y=[row["income"] for row in rows],
               marker=dict(color=INCOME_COLOR, cornerradius=2),
               hovertemplate="Income  $%{y:,.2f}<extra></extra>"),
        go.Bar(name="Spending", x=months, y=[row["expenses"] for row in rows],
               marker=dict(color=EXPENSE_COLOR, cornerradius=2, line=dict(color="#648C78", width=0.7)),
               hovertemplate="Spending  $%{y:,.2f}<extra></extra>"),
    ])
    fig.update_layout(template="none", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                      font=dict(family=FONT, size=12, color=MUTED),
                      margin=dict(l=48, r=8, t=8, b=36), barmode="group", bargap=0.34,
                      bargroupgap=0.08, height=330, hovermode="x unified", showlegend=False,
                      hoverlabel=dict(bgcolor=TEXT, font=dict(color="#FFFFFF", family=FONT), bordercolor=TEXT))
    fig.update_xaxes(showgrid=False, zeroline=False, tickformat="%b", dtick="M1",
                     hoverformat="%B %Y", fixedrange=True, tickfont=dict(size=11, color=MUTED),
                     showline=True, linecolor="#C9D6CD", automargin=True)
    fig.update_yaxes(gridcolor="#E7EDE9", zeroline=False, tickprefix="$",
                     tickformat=",.0f", nticks=4, fixedrange=True, tickfont=dict(size=11, color=MUTED),
                     automargin=True)
    st.markdown('<div class="vt-legend"><span><i class="income"></i>Income</span>'
                '<span><i class="spending"></i>Spending</span></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, config={"displayModeBar": False}, theme=None)


def category_breakdown(rows):
    rows = sorted(rows, key=lambda row: row["total"], reverse=True)
    maximum = max((row["total"] for row in rows), default=0)
    if maximum <= 0:
        st.info("No spending recorded for this period.")
        return
    items = "".join(
        '<li class="vt-category"><div>'
        f'<span>{escape(row["category"])}</span><strong>{money(row["total"])}</strong></div>'
        f'<div class="vt-track" aria-hidden="true"><span style="width:{max(0, row["total"]) / maximum * 100:.2f}%"></span></div></li>'
        for row in rows)
    st.markdown(f'<ul class="vt-categories">{items}</ul>', unsafe_allow_html=True)


def dashboard():
    masthead()
    title, actions = st.columns([5, 1], vertical_alignment="center")
    with title:
        st.markdown('<h1>Financial overview</h1>', unsafe_allow_html=True)
    with actions:
        if st.button("Sign out"):
            del st.session_state.token
            st.rerun()
    try:
        with st.spinner("Loading the overview…"):
            by_month = api_get("/summary/by-month")
            by_category = api_get("/summary/by-category")
    except (requests.RequestException, ValueError):
        st.error("Couldn't load the overview. Your session is still open; retry in a moment.")
        if st.button("Retry loading"):
            st.rerun()
        return
    if not by_month:
        st.info("No transactions yet. This workspace has no activity to summarize.")
        return
    st.markdown(f'<p class="vt-period">{escape(period_label(by_month))} '
                '<span>· Generated sample data</span></p>', unsafe_allow_html=True)
    summary(by_month)
    movement, categories = st.columns([1.85, 1], gap="large")
    with movement:
        section_title("Income and spending", "Monthly movement across the year")
        month_chart(by_month)
        if max(row["month"] for row in by_month) == datetime.now().strftime("%Y-%m"):
            st.caption(f"{datetime.now().strftime('%B')} includes activity through the current sample date.")
        with st.expander("View monthly figures"):
            st.dataframe([{"Month": row["month"], "Income ($)": row["income"],
                           "Spending ($)": row["expenses"], "Net ($)": round(row["income"] - row["expenses"], 2)}
                          for row in sorted(by_month, key=lambda row: row["month"])], hide_index=True,
                         column_config={name: st.column_config.NumberColumn(format="$%.2f")
                                        for name in ("Income ($)", "Spending ($)", "Net ($)")})
    with categories:
        section_title("Where it went", "Spending by category · largest first")
        category_breakdown(by_category)
    st.markdown('<footer class="vt-footer"><span>Sample data only. No personal financial information.</span>'
                '<span>Vault · Python application demo</span></footer>', unsafe_allow_html=True)


if "token" in st.session_state:
    dashboard()
else:
    login_form()
