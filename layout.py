from dash import html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from nba_api.stats.endpoints import leaguegamefinder
import plotly.express as px
import plotly.graph_objects as go

from app import *
from data import *

graph_margin=dict(l=25, r=25, t=0, b=0)
mensagem_inicial = html.H1("Selecione todos os dados de entrada para analisar os valores!", style={"textAlign": "center", "font-size":"30px", "margin-top":"25px"})
config={"displayModeBar": False, "showTips": False}


navbar = dbc.Navbar([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.A(html.Img(src="assets/bola.png", height=80, style={"margin-bottom":"5px"}), href="/")),
                dbc.Col(dbc.NavbarBrand("NBA Analysis")),
                dbc.Col(ThemeSwitchAIO(aio_id="theme",themes=[url_theme1, url_theme2]),style={"color":"white"}, width="auto"),
                dbc.Col(dbc.Button("Head-to-head", id="button", size="md"), width="auto")
            ],
            align="center", justify="center")
        ], fluid=True)

], dark=True, color="dark",class_name="navbar")

team_filter = dbc.Row([
    dbc.Col([
            # Filtos de seleção
            dbc.Row([
                dbc.Col([
                    html.Legend("Temporada"),
                    dbc.Select(id="season", 
                                 className="dropdown",
                                 options=[{"label": value, "value": key, "disabled": False} for key, value in dict_season_final.items()]
                                 )
                ], md=3, sm=12),
                dbc.Col([
                    html.Legend("Time da casa"),
                    dbc.Select(id="home-team", 
                                 className="dropdown",
                                 options=[{"label": value, "value": key, "disabled": False} for key, value in teams_final.items()],
                                 )
                ], md=3, sm=12),
                dbc.Col([
                    html.Legend("Time visitante"),
                    dbc.Select(id="away-team", 
                                 className="dropdown",
                                 options=[{"label": value, "value": key} for key, value in teams_final.items()]
                                 )
                ], md=3, sm=12),
                dbc.Col([
                    dbc.Button("Clique para analisar",color="info", size="md", class_name="button", id="button-analise")
                ], md=3, sm=12),
            ], justify="center", align="center"),

            html.Hr(),
    ])
])

dashboard = html.Div(children=dbc.Spinner(children=mensagem_inicial, id="dash"))

graphs = dbc.Row([
        dbc.Col([
            html.Div(id="dash-home", children=[
                    dbc.Row([
                        html.Label(id="home-team-name"),
                        dbc.Col([
                            dbc.Spinner(dash_table.DataTable(id="home-table", style_cell={"textAlign":"center"}, sort_action="native",
                                                             style_data_conditional=[{'if': {'filter_query': '{V-D} = V', 'column_id': 'V-D'}, 'color': 'green'}, {'if': {'filter_query': '{V-D} = D', 'column_id': 'V-D'}, 'color': 'red'}],
                                                             style_header= {"fontWeight": "bold"}
                                                                ))
                        ]),

                        dbc.Col([
                            # Média de PTs em casa
                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Média de PTs em casa", className="dash_legend")
                                ]),
                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="home-pts-casa", config=config))
                                ])
                            ], class_name="graficos"),
                        ])
                    ]),

                    dbc.Row([
                        dbc.Col([
                            # Média de PTs sofridos nos ultimos 5 jogos
                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Média de PTs contra (ultimos 5 jogos)", className="dash_legend")
                                ]),
                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="home-pts-contra", config=config))
                                ])
                            ], class_name="graficos"),
                        ]),


                        dbc.Col([
                            # Média de PTs feitos nos ultimos 5 jogos
                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Média de PTs a favor (ultimos 5 jogos)", className="dash_legend")
                                ]),
                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="home-pts-a-favor", config=config))
                                ])
                            ], class_name="graficos"),
                            
                        ])
                    ]),

                    dbc.Row([

                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Média de PTs a favor (Temporada)", className="dash_legend")
                                ]),

                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="home-pts-feitos-temporada", config=config))
                                ])  
                            ], class_name="graficos"),

                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Média de PTs contra (Temporada)", className="dash_legend")
                                ]),

                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="home-pts-contra-temporada", config=config))
                                ])
                            ], class_name="graficos")
                        ]),

                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Maior pontuação na temporada", className="dash_legend")
                                ]),

                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="home-maior-pts", config=config))
                                ])
                            ], class_name="graficos"),

                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Menor pontuação na temporada", className="dash_legend")
                                ]),

                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="home-menor-pts", config=config))
                                ])
                            ], class_name="graficos")
                        ])

                    ]),

                    dbc.Row([
                        dbc.Col([
                        dbc.Spinner(dcc.Graph(id="home-analise-pts", config=config))
                    ])
                    ])
            ])
        ]),

        dbc.Col([
            html.Div(id="dash-away",
                children=[
                dbc.Row([
                        html.Label(id="away-team-name"),
                        dbc.Col([
                            dbc.Spinner(dash_table.DataTable(id="away-table", style_cell={"textAlign":"center"}, sort_action="native",
                                                             style_data_conditional=[{'if': {'filter_query': '{V-D} = V', 'column_id': 'V-D'}, 'color': 'green'}, {'if': {'filter_query': '{V-D} = D', 'column_id': 'V-D'}, 'color': 'red'}],
                                                             style_header= {"fontWeight": "bold"}))
                        ]),

                        dbc.Col([

                            # Média de PTs fora
                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Média de PTs fora", className="dash_legend")
                                ]),
                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="away-pts-fora", config=config))
                                 ])
                            ], class_name="graficos"),
                            
                        ])
                ]),

                dbc.Row([
                    dbc.Col([
                        # Média de PTs sofridos nos ultimos 5 jogos
                        dbc.Card([
                            dbc.CardHeader([
                                html.Legend("Média de PTs contra (ultimos 5 jogos)", className="dash_legend")
                            ]),
                            dbc.CardBody([
                                dbc.Spinner(dcc.Graph(id="away-pts-contra", config=config))
                            ])
                        ], class_name="graficos"),
                    ]),

                    dbc.Col([
                        # Média de PTs feitos nos ultimos 5 jogos
                        dbc.Card([
                            dbc.CardHeader([
                                html.Legend("Média de PTs a favor (ultimos 5 jogos)", className="dash_legend")
                            ]),

                            dbc.CardBody([
                                dbc.Spinner(dcc.Graph(id="away-pts-a-favor", config=config))
                            ])
                        ], class_name="graficos"),
                    ])
                ]),

                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                                    dbc.CardHeader([
                                        html.Legend("Média de PTs a favor (Temporada)", className="dash_legend")
                                    ]),

                                    dbc.CardBody([
                                        dbc.Spinner(dcc.Graph(id="away-pts-feitos-temporada", config=config))
                                    ])
                                ], class_name="graficos"),

                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Média de PTs contra (Temporada)", className="dash_legend")
                                ]),

                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="away-pts-contra-temporada", config=config))
                                ])
                            ], class_name="graficos")

                        ]),

                    dbc.Col([
                        dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Maior pontuação na temporada", className="dash_legend")
                                ]),

                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="away-maior-pts", config=config))
                                ])
                            ], class_name="graficos"),

                            dbc.Card([
                                dbc.CardHeader([
                                    html.Legend("Menor pontuação na temporada", className="dash_legend")
                                ]),

                                dbc.CardBody([
                                    dbc.Spinner(dcc.Graph(id="away-menor-pts", config=config))
                                ])
                            ], class_name="graficos")
                        ]),

                    ]),


                dbc.Row([
                    dbc.Col([
                        dbc.Spinner(dcc.Graph(id="away-analise-pts", config=config))
                    ])
                ])

            ])
        ]),
], class_name="g-3 my-20")

@app.callback(
    Output("away-team", "options"),
    Output("home-team", "options"),

    Input("away-team", "value"),
    Input("home-team", "value"),

    State("away-team", "options"),
    State("home-team", "options"),

)
def verifica_team(away_value, home_value, away_options, home_options):
    trigger = dash.callback_context.triggered_id


    if (trigger is not None) and (trigger == "home-team"):

        options = []

        for option in away_options:
            if option["value"] == home_value:
                option["disabled"] = True
                options.append(option)
            else:
                option["disabled"] = False
                options.append(option)

        return options, home_options
    
    elif (trigger is not None) and (trigger == "away-team"):

        options = []

        for option in home_options:
            if option["value"] == away_value:
                option["disabled"] = True
                options.append(option)
            else:
                option["disabled"] = False
                options.append(option)

        return away_options, options
    
    else:
        return away_options, home_options
    
@app.callback(
    Output("dash", "children"),
    Output("home-data", "data"),
    Output("away-data", "data"),
    Output("vs-home-team", "data"),
    Output("vs-away-team", "data"),

    Input("button-analise", "n_clicks"),

    State("home-team", "value"),
    State("away-team", "value"),
    State("season", "value")
)
def cria_data(n_clicks, home_value, away_value, season):

    
    if (n_clicks == None) or (home_value == None) or (away_value == None) or (season ==None):
        return [mensagem_inicial], None, None,None, None
    else:
        data_list = []
        k = 0

        for i in [home_value, away_value, home_value, away_value]:

            if k == 0:
                df_casa = leaguegamefinder.LeagueGameFinder(team_id_nullable=i, timeout=90)
            elif k == 1:
                df_casa = leaguegamefinder.LeagueGameFinder(team_id_nullable=i, timeout=90)
            elif k == 2:
                df_casa = leaguegamefinder.LeagueGameFinder(vs_team_id_nullable=i, timeout=90)
            else:
                df_casa = leaguegamefinder.LeagueGameFinder(vs_team_id_nullable=i, timeout=90)
            
            
            df_casa = df_casa.get_data_frames()[0]

            df_casa["GAME_DATE"] = pd.to_datetime(df_casa["GAME_DATE"])
            df_casa["ANO"] = df_casa["GAME_DATE"].apply(lambda x: x.year)
            df_casa["MES"] = df_casa["GAME_DATE"].apply(lambda x: x.month)

            year = (int(str(season).split("-")[0]), int(str(season).split("-")[0]) + 1)

            df_casa = df_casa[((df_casa["ANO"] == year[0]) & (df_casa["MES"] >= 8)) | ((df_casa["ANO"] == year[1]) & (df_casa["MES"] <= 8))]

            df_casa = df_casa[["TEAM_ABBREVIATION", "TEAM_NAME","GAME_DATE", "MATCHUP", "WL","PTS"]]

            df_casa = df_casa.to_dict()
            
            data_list.append(df_casa)
            k += 1

        return graphs, data_list[0], data_list[1], data_list[2], data_list[3]
    

@app.callback(
    Output("home-team-name","children"),
    Output("home-table", "data"),
    Output("home-pts-a-favor", "figure"),
    Output("home-pts-contra","figure"),
    Output("home-pts-casa","figure"),
    Output("home-pts-feitos-temporada","figure"),
    Output("home-pts-contra-temporada","figure"),
    Output("home-maior-pts", "figure"),
    Output("home-menor-pts", "figure"),
    Output("home-analise-pts", "figure"),

    Output("away-team-name","children"),
    Output("away-table", "data"),
    Output("away-pts-a-favor", "figure"),
    Output("away-pts-contra", "figure"),
    Output("away-pts-fora", "figure"),
    Output("away-pts-feitos-temporada", "figure"),
    Output("away-pts-contra-temporada", "figure"),
    Output("away-maior-pts", "figure"),
    Output("away-menor-pts", "figure"),
    Output("away-analise-pts", "figure"),

    Input(ThemeSwitchAIO.ids.switch("theme"),"value"),
    Input("home-data", "data"),
    

    State("away-data", "data"),
    State("home-team", "value"),
    State("away-team", "value"),
    State("vs-home-team", "data"),
    State("vs-away-team", "data"),

)
def atualiza_graficos(url, home_data, away_data, home_value, away_value, vs_home_data, vs_away_data):

    template = theme1 if url else theme2

    if home_value == None or away_value == None:
        return [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ]

    else:
        retornos = []
        k = 0

        for i, j in [[home_data,vs_home_data], [away_data, vs_away_data]]:
            
            df_data = pd.DataFrame(i)
            df_data_vs = pd.DataFrame(j)

            nome_time = df_data.at[df_data.index[0],"TEAM_NAME"]
            retornos.append(nome_time)

            table_data = df_data[["MATCHUP","GAME_DATE", "WL", "PTS"]].copy()
            table_data["GAME_DATE"] = pd.to_datetime(table_data["GAME_DATE"]).dt.date
            table_data = table_data.rename(columns={"MATCHUP": "Partida", "GAME_DATE":"Data","WL":"V-D"})
            table_data["V-D"] = table_data["V-D"].map(dict(W="V", L="D"))
            table_data = table_data.head(5)
            table_data = table_data.to_dict('records')
            retornos.append(table_data)

            media_pts_favor_5_jogos = df_data.head(5)["PTS"].mean()
            retornos.append(cria_grafico(template, graph_margin, media_pts_favor_5_jogos, "green"))
           
            media_pts_contra_5_jogos = df_data_vs.head(5)["PTS"].mean()
            retornos.append(cria_grafico(template, graph_margin, media_pts_contra_5_jogos, "red"))

            if k == 0:
                media_pts_casa = df_data[df_data["MATCHUP"].str.contains("vs")]["PTS"].mean()
                retornos.append(cria_grafico(template, graph_margin, media_pts_casa, "green"))
                
            else:
                media_pts_fora = df_data[df_data["MATCHUP"].str.contains("@")]["PTS"].mean()
                retornos.append(cria_grafico(template, graph_margin, media_pts_fora, "green"))
                

            media_pts_feitos_temporada = df_data["PTS"].mean()
            retornos.append(cria_grafico(template, graph_margin, media_pts_feitos_temporada, "green"))
            

            media_pts_contra_temporada = df_data_vs["PTS"].mean()
            retornos.append(cria_grafico(template, graph_margin, media_pts_contra_temporada, "red"))
            

            maior = df_data["PTS"].max()
            retornos.append(cria_grafico(template, graph_margin, maior, "green"))


            menor = df_data["PTS"].min()
            retornos.append(cria_grafico(template, graph_margin, menor, "red"))

            df_data["ADV"] = df_data["MATCHUP"].str.replace("@", "-", regex=False).str.replace("vs.", "-",regex=False)
            df_data["ADV"] = df_data["ADV"].apply(lambda x: x.split("-")[1])
            df_data = df_data.sort_values("GAME_DATE")
            df_analise = df_data[["ADV", "PTS","WL", "GAME_DATE"]].tail(10).reset_index(drop=True).reset_index().rename(columns={"index":"Jogo","ADV": "Oponente","PTS": "Pontos","WL":"Resultado", "GAME_DATE":"Data"})
            df_analise["Data"] = pd.to_datetime(df_analise["Data"]).dt.date
            df_analise["Jogo"] = df_analise["Jogo"].apply(lambda x: x+1)
            df_analise["Resultado"] = df_analise["Resultado"].map(dict(W="Vitoria", L="Derrota"))
            eixo_x = df_analise["Jogo"].to_list()
            
            fig = px.line(df_analise, x="Jogo",y="Pontos",markers=True, template=template, hover_data=df_analise.columns)
            fig.update_layout(xaxis=dict(tickvals=eixo_x), title=f"{nome_time} - Pontuação últimos 10 jogos")
            retornos.append(fig)
            k+=1
        return retornos


            

            

            

        




