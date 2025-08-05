import reflex as rx
import plotly.graph_objects as go
from data import generate_mock_data
 
df = generate_mock_data()
 
def metric_card(title, value, change):
    color = "green" if change > 0 else "red"
    return rx.card(
        rx.vstack(
            rx.text(title, size="3"),
            rx.text(f"{value}", size="5", weight="bold"),
            rx.text(f"{'▲' if change > 0 else '▼'} {abs(change):.2f}%", color=color),
        ),
        width="20%",
        padding="1em",
        shadow="md"
    )
 
def line_chart(title, column):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["week"], y=df[column], mode="lines", name=column))
    fig.update_layout(title=title, height=250, margin=dict(l=10, r=10, t=30, b=10))
    return rx.plotly(data=fig)
 
def histogram_time_to_open():
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df["median_time_open"], nbinsx=10))
    fig.add_vline(x=df["median_time_open"].median(), line_dash="dash", line_color="blue")
    fig.update_layout(title="Time Distribution to Account Opening", height=300)
    return rx.plotly(data=fig)
 
def index() -> rx.Component:
    return rx.container(
        rx.heading("🔍 Onboarding Funnel Dashboard", size="3", mb="2em"),

        # Top metrics
        rx.hstack(
            metric_card("Registered Users", df["total_users"].iloc[-1], (df["total_users"].iloc[-1] - df["total_users"].iloc[-2])/df["total_users"].iloc[-2]*100),
            metric_card("Reg to Open CVR", f"{df['reg_to_open_cvr'].iloc[-1]:.2f}%", df["reg_to_open_cvr"].iloc[-1] - df["reg_to_open_cvr"].iloc[-2]),
            metric_card("Verification CVR", f"{df['verification_cvr'].iloc[-1]:.2f}%", df["verification_cvr"].iloc[-1] - df["verification_cvr"].iloc[-2]),
            metric_card("Open to Txn CVR", f"{df['open_to_txn_cvr'].iloc[-1]:.2f}%", df["open_to_txn_cvr"].iloc[-1] - df["open_to_txn_cvr"].iloc[-2]),
            metric_card("First Deposit CVR", f"{df['first_deposit_cvr'].iloc[-1]:.2f}%", df["first_deposit_cvr"].iloc[-1] - df["first_deposit_cvr"].iloc[-2]),
        ),
        rx.divider(),
 
        # Charts
        rx.grid(
            line_chart("Registered Users Over Time", "total_users"),
            line_chart("CVR: Registration to Opening", "reg_to_open_cvr"),
            line_chart("CVR: Verification to Opening", "verification_cvr"),
            line_chart("CVR: Account to First Txn", "open_to_txn_cvr"),
            line_chart("CVR: First Deposit", "first_deposit_cvr"),
            line_chart("Total First Transactions", "total_txns"),
            columns="3",
            spacing="4"
        ),
        rx.divider(),
 
        # Time to Account Opening Section
        rx.hstack(
            rx.card(
                rx.vstack(
                    rx.text("⏱️ Median Time to Open Account", size="4"),
                    rx.text(f"{df['median_time_open'].iloc[-1]:.2f} sec", weight="bold"),
                ),
                width="30%"
            ),
            histogram_time_to_open(),
        ),
        rx.divider(),
 
        # Time-Limited Conversions
        rx.hstack(
            line_chart("Registrations < 5 mins", "fast_reg_5m"),
            line_chart("Registrations < 10 mins", "fast_reg_10m"),
        ),


        margin_y="2em"

    )
 
# Add state and page to the app.
app = rx.App()
app.add_page(index)
