import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from mplsoccer import Pitch

# Import the core analysis functions from your separate file
from feasible_pass_analysis import analyze_pass_scenario, generate_xt_grid

# --- DASH APP SETUP ---
app = dash.Dash(__name__)

# --- LAYOUT ---
app.layout = html.Div(
    style={'backgroundColor': '#111111', 'color': 'white', 'fontFamily': 'sans-serif'},
    children=[
        html.H1(
            children="⚽️ Pass Decision Analysis App",
            style={'textAlign': 'center', 'margin': '20px'}
        ),
        html.Div(
            children="Use this app to analyze a pass scenario and compare the actual pass against the best feasible alternatives. Adjust the player positions in the sliders below to create a new scenario.",
            style={'textAlign': 'center', 'margin-bottom': '40px'}
        ),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center'},
            children=[
                # --- CONTROLS COLUMN ---
                html.Div(
                    style={'width': '30%', 'padding': '20px', 'background': '#222222', 'borderRadius': '10px'},
                    children=[
                        html.H2("Player Positions", style={'textAlign': 'center'}),
                        html.Div(
                            style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'},
                            children=[
                                html.P("Passer X:", style={'margin-top': '20px'}),
                                dcc.Slider(id='passer-x', min=0, max=120, step=1, value=60, tooltip={'always_visible': True}),
                                html.P("Passer Y:"),
                                dcc.Slider(id='passer-y', min=0, max=80, step=1, value=40, tooltip={'always_visible': True}),

                                html.P("Attacker 2 X:"),
                                dcc.Slider(id='attacker2-x', min=0, max=120, step=1, value=70, tooltip={'always_visible': True}),
                                html.P("Attacker 2 Y:"),
                                dcc.Slider(id='attacker2-y', min=0, max=80, step=1, value=20, tooltip={'always_visible': True}),

                                html.P("Attacker 3 X (Actual Receiver):"),
                                dcc.Slider(id='attacker3-x', min=0, max=120, step=1, value=75, tooltip={'always_visible': True}),
                                html.P("Attacker 3 Y (Actual Receiver):"),
                                dcc.Slider(id='attacker3-y', min=0, max=80, step=1, value=55, tooltip={'always_visible': True}),

                                html.P("Attacker 4 X:"),
                                dcc.Slider(id='attacker4-x', min=0, max=120, step=1, value=80, tooltip={'always_visible': True}),
                                html.P("Attacker 4 Y:"),
                                dcc.Slider(id='attacker4-y', min=0, max=80, step=1, value=70, tooltip={'always_visible': True}),

                                html.P("Attacker 5 X:"),
                                dcc.Slider(id='attacker5-x', min=0, max=120, step=1, value=50, tooltip={'always_visible': True}),
                                html.P("Attacker 5 Y:"),
                                dcc.Slider(id='attacker5-y', min=0, max=80, step=1, value=60, tooltip={'always_visible': True}),

                                html.P("Defender 1 X:"),
                                dcc.Slider(id='defender1-x', min=0, max=120, step=1, value=65, tooltip={'always_visible': True}),
                                html.P("Defender 1 Y:"),
                                dcc.Slider(id='defender1-y', min=0, max=80, step=1, value=30, tooltip={'always_visible': True}),

                                html.P("Defender 2 X:"),
                                dcc.Slider(id='defender2-x', min=0, max=120, step=1, value=70, tooltip={'always_visible': True}),
                                html.P("Defender 2 Y:"),
                                dcc.Slider(id='defender2-y', min=0, max=80, step=1, value=50, tooltip={'always_visible': True}),

                                html.P("Defender 3 X:"),
                                dcc.Slider(id='defender3-x', min=0, max=120, step=1, value=85, tooltip={'always_visible': True}),
                                html.P("Defender 3 Y:"),
                                dcc.Slider(id='defender3-y', min=0, max=80, step=1, value=45, tooltip={'always_visible': True}),

                                html.P("Defender 4 X:"),
                                dcc.Slider(id='defender4-x', min=0, max=120, step=1, value=60, tooltip={'always_visible': True}),
                                html.P("Defender 4 Y:"),
                                dcc.Slider(id='defender4-y', min=0, max=80, step=1, value=60, tooltip={'always_visible': True}),
                            ]
                        )
                    ]
                ),

                # --- VISUALIZATION COLUMN ---
                html.Div(
                    style={'width': '60%', 'padding': '20px'},
                    children=[
                        dcc.Graph(id='pitch-visualization'),
                        html.H2("Analysis Results", style={'textAlign': 'center'}),
                        html.Div(id='analysis-results', style={'textAlign': 'center'})
                    ]
                )
            ]
        )
    ]
)

# --- CALLBACKS ---
@app.callback(
    [Output('pitch-visualization', 'figure'),
     Output('analysis-results', 'children')],
    [Input('passer-x', 'value'), Input('passer-y', 'value'),
     Input('attacker2-x', 'value'), Input('attacker2-y', 'value'),
     Input('attacker3-x', 'value'), Input('attacker3-y', 'value'),
     Input('attacker4-x', 'value'), Input('attacker4-y', 'value'),
     Input('attacker5-x', 'value'), Input('attacker5-y', 'value'),
     Input('defender1-x', 'value'), Input('defender1-y', 'value'),
     Input('defender2-x', 'value'), Input('defender2-y', 'value'),
     Input('defender3-x', 'value'), Input('defender3-y', 'value'),
     Input('defender4-x', 'value'), Input('defender4-y', 'value')]
)
def update_graph(passer_x, passer_y, a2x, a2y, a3x, a3y, a4x, a4y, a5x, a5y, d1x, d1y, d2x, d2y, d3x, d3y, d4x, d4y):
    # Prepare scenario data from slider inputs
    scenario_data = {
        'passer_id': 1,
        'actual_pass': {
            'receiver_id': 3,
            'start_x': passer_x,
            'start_y': passer_y,
            'end_x': a3x,
            'end_y': a3y
        },
        'players': {
            1: {'team': 'Attackers', 'position': (passer_x, passer_y)},
            2: {'team': 'Attackers', 'position': (a2x, a2y)},
            3: {'team': 'Attackers', 'position': (a3x, a3y)},
            4: {'team': 'Attackers', 'position': (a4x, a4y)},
            5: {'team': 'Attackers', 'position': (a5x, a5y)},
            6: {'team': 'Defenders', 'position': (d1x, d1y)},
            7: {'team': 'Defenders', 'position': (d2x, d2y)},
            8: {'team': 'Defenders', 'position': (d3x, d3y)},
            9: {'team': 'Defenders', 'position': (d4x, d4y)},
        }
    }

    # Run the analysis
    analysis_df = analyze_pass_scenario(scenario_data)

    # --- PLOTTING WITH PLOTLY ---
    pitch = Pitch(pitch_color='#008300', line_color='white', line_zorder=2)
    fig = pitch.draw(figsize=(10, 7), show=False)
    ax = fig.gca()

    # Create a Plotly figure from Matplotlib
    plotly_fig = go.Figure()

    # Add player scatter plots
    attacker_x = [p['position'][0] for p in scenario_data['players'].values() if p['team'] == 'Attackers']
    attacker_y = [p['position'][1] for p in scenario_data['players'].values() if p['team'] == 'Attackers']
    defender_x = [p['position'][0] for p in scenario_data['players'].values() if p['team'] == 'Defenders']
    defender_y = [p['position'][1] for p in scenario_data['players'].values() if p['team'] == 'Defenders']
    
    plotly_fig.add_trace(go.Scatter(x=attacker_x, y=attacker_y, mode='markers', marker=dict(color='blue', size=15), name='Attackers'))
    plotly_fig.add_trace(go.Scatter(x=defender_x, y=defender_y, mode='markers', marker=dict(color='red', size=15), name='Defenders'))

    # Add pass arrows
    actual_pass = analysis_df[analysis_df['is_actual']]
    if not actual_pass.empty:
        plotly_fig.add_trace(go.Scatter(x=[actual_pass.iloc[0]['start_x'], actual_pass.iloc[0]['end_x']],
                                         y=[actual_pass.iloc[0]['start_y'], actual_pass.iloc[0]['end_y']],
                                         mode='lines+markers', line=dict(color='gold', width=2), name='Actual Pass'))
    
    alternative_passes = analysis_df[~analysis_df['is_actual']].head(3)
    for _, row in alternative_passes.iterrows():
        plotly_fig.add_trace(go.Scatter(x=[row['start_x'], row['end_x']],
                                         y=[row['start_y'], row['end_y']],
                                         mode='lines+markers', line=dict(color='darkgreen', width=2), name='Feasible Alternative'))

    # Set up layout for the pitch
    plotly_fig.update_layout(
        xaxis=dict(range=[0, 120], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 80], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='#008300',
        paper_bgcolor='#111111',
        showlegend=True,
        title='Pass Analysis: Feasible vs. Actual Options'
    )

    # Convert DataFrame to an HTML table for display
    analysis_table = html.Table(
        style={'width': '100%', 'borderCollapse': 'collapse', 'textAlign': 'left'},
        children=[
            html.Thead(
                html.Tr([html.Th(col) for col in analysis_df.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(analysis_df.iloc[i][col]) for col in analysis_df.columns
                ]) for i in range(len(analysis_df))
            ])
        ]
    )

    return plotly_fig, analysis_table

if __name__ == '__main__':
    app.run_server(debug=True)
