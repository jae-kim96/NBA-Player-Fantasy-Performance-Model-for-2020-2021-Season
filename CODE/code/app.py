import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
# import plotly.graph_objs as go
import re

# Initiliazing the app
app = dash.Dash(__name__)

# Load data
player_stat = pd.read_csv(
    '../data/input/players_stats_multi_season_2010_2020.csv', index_col=0)
model_output = pd.read_csv('../data/output/MODEL_OUTPUT_2020-2021.csv')

# Add Fantasy Points Column
player_stat['Total Points'] = player_stat['PTS'] + player_stat['FG3M'] - player_stat['FGA'] + \
    (player_stat['FGM'] * 2) - player_stat["FTA"] + player_stat['FTM'] + player_stat["REB"] + \
    (player_stat['AST'] * 2) + (player_stat['STL'] * 4) + (player_stat['BLK'] * 4) - (
    2 * player_stat['TOV'])
model_output['Total Points'] = model_output['PTS'] + model_output['FG3M'] - model_output['FGA'] + \
    (model_output['FGM'] * 2) - model_output["FTA"] + model_output['FTM'] + model_output[
    "REB"] + \
    (model_output['AST'] * 2) + (model_output['STL'] * 4) + (model_output['BLK'] * 4) - (
    2 * model_output['TOV'])

# sort data
player_stat = player_stat.append(
    model_output[model_output["GROUP_VALUE"] == "2020-21"])
player_stat = player_stat.sort_values(['GROUP_VALUE'], ascending=False)


# Select relevant columns
data_cols = ['FGM', 'FGA', 'FG3M', 'FTM', 'FTA', 'REB',
             'AST', 'TOV', 'STL', 'BLK', 'PTS']
col_labels = {
    'FGM': 'Field Goal Made',
    'FGA': 'Field Goal Attempt',
    'FG3M': 'Field Goal 3-Point',
    'FTM': 'Free Throw Made',
    'FTA': 'Free Throw Attempt',
    'REB': 'Rebound',
    'AST': 'Assist',
    'TOV': 'Turnover',
    'STL': 'Steal',
    'BLK': 'Block',
    'PTS': 'Points',
    'DISPLAY_FIRST_LAST': 'Player Name',
    'GROUP_VALUE': 'Season',
    'Total Points': 'Fantasy<br>Points'
}

id_cols = player_stat.columns[:9]

# Get Player Name and Total Points
player_table = player_stat[["DISPLAY_FIRST_LAST",
                            'TEAM_NAME', 'GROUP_VALUE', 'Total Points']]
player_table.append(
    model_output[["DISPLAY_FIRST_LAST", 'TEAM_NAME', 'GROUP_VALUE', 'Total Points']])
player_table = player_table.sort_values(by=["Total Points"], ascending=False)
player_table['Rank'] = player_table.groupby(
    "GROUP_VALUE")["Total Points"].rank(ascending=False).astype(int)
player_table_cols = player_table.columns.tolist()
player_table_cols = player_table_cols[-1:] + player_table_cols[:-1]
player_table = player_table[player_table_cols]


# Select feature
def get_options(list_values, col_labels=None, reverse=False):
    list_values = list(list_values)
    list_values.sort(reverse=reverse)
    dict_list = []
    if col_labels == None:
        for val in list_values:
            dict_list.append({'label': val, 'value': val})
    else:
        for val in list_values:
            dict_list.append({'label': col_labels[val], 'value': val})
    return dict_list


def make_bar_chart(player_stat, x_feature='AST', y_feature='DISPLAY_FIRST_LAST', top_n=20):

    color_param = 'Total Points'

    # Create bar chart
    bar_chart = px.bar(player_stat.sort_values(by=[x_feature], ascending=False).head(top_n),
                       x=x_feature,
                       y=y_feature,
                       color=color_param,
                       # barmode='group',
                       # hover_data=data_cols,
                       orientation='h',
                       labels=col_labels,
                       template='plotly_dark').update_layout(
        {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
         'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
    )
    bar_chart.update_layout(yaxis={'categoryorder': 'total ascending'})

    return bar_chart


# Drop-downs
dropdown_features = html.Div(className='div-for-dropdown', children=[
    dcc.Dropdown(id='feature_selector',
                 options=get_options(data_cols, col_labels),
                 placeholder="Select a parameter",
                 value='AST',
                 multi=False,
                 className='stockselector',)
], style={'backgroundColor': 'rgba(0, 0, 0, 0)', 'color': 'orange'})

checklist_teams = html.Div(className='div-for-dropdown', children=[
    dcc.Checklist(id='team_selector',
                  options=get_options(player_stat['TEAM_NAME'].unique()),
                  value=[],
                  className='stockselector',
                  labelStyle={'padding': '2px'})
], style={'color': 'grey', 'overflowY': 'scroll',
          'height': '350px', 'width': '100%', 'border': 'solid thin white', 'border-radius': '5px'})

option_seasons = get_options(
    model_output['GROUP_VALUE'].unique(), reverse=True)
option_seasons[0]['label'] += ' (Prediction)'

dropdown_seasons = html.Div(className='div-for-dropdown', children=[
    dcc.Dropdown(id='season_selector',
                 options=option_seasons,
                 placeholder="Select a season",
                 value='2020-21',
                 multi=False,)
])

r1c1 = html.Div(className='one columns',
                children=[
                    html.Img(src='https://a.espncdn.com/combiner/i?img=/redesign/assets/img/icons/ESPN-icon-basketball.png&h=160&w=160&scale=crop&cquality=40',
                             style={'height': '75px'})
                ], style={'padding-left': '10px'})

r1c2 = html.Div(className='six columns',
                children=[
                    html.H2('Advanced NBA Analytics for Fantasy Basketball Players',
                            style={'color': 'orange'})
                ])

r1c3 = html.Div(className='two columns', children=[
    # html.H6("  Select a season")
], style={'padding-top': '5px'})

r1c4 = html.Div(className='three columns', children=[
    dropdown_seasons
])


r2c1 = html.Div(className='four columns', children=[
    dropdown_features,
    html.H6(id='bar_chart_label',
            children=['Top Players of the 2019-20 Season'],
            style={'text-align': 'center', 'color': 'rgba(100, 200, 50, 0.75)'}),
    dcc.Graph(id='stats_bar_chart', figure=make_bar_chart(player_stat),
              config={'displayModeBar': False})
], style={'padding': '0px 10px'})

r2c2r1 = html.Div(className='row', children=[
    dcc.Graph(id="player_barChart", style={
              "height": 300}, config={'displayModeBar': False})
])

r2c2r2 = html.Div(className='row', children=[
    dcc.Graph(id="box_plot", style={"height": 300},
              config={'displayModeBar': False})
])

r2c2 = html.Div(className='three columns', children=[
    r2c2r1,
    r2c2r2
])

r2c3 = html.Div(className='four columns', children=[
    dcc.Input(
        id="searchName",
        type="text",
        placeholder="Search by Name",
        debounce=False,
        style={'backgroundColor': 'rgba(0, 0, 0, 0)', 'margin': '10px 0px 5px 0px',
               'width': '100%', 'color': 'white'}
    ),
    dash_table.DataTable(
        id="fantasy_table",
        columns=[{"name": i, "id": i} for i in player_table.columns],
        data=player_table.to_dict('records'),
        style_table={
            'height': '450px',
            'overflowY': 'scroll',
            'width': '100%',
            'font-size': '11px'
        },
        style_header={'backgroundColor': 'rgba(0, 0, 0, 0)'},
        style_cell={
            'backgroundColor': 'rgba(0, 0, 0, 0)'
        },
        sort_action='native',
        row_selectable='single',
        selected_rows=[0]
    )
], style={'padding': '0px 10px'})

r2c4r1 = html.Div(className='row', children=[
    html.Img(id='player_image',
             src='https://ak-static.cms.nba.com/wp-content/uploads/logos/leagues/logo-nba.svg',
             style={'width': '100%'})
])

r2c4r2 = html.Div(className='row', children=[
    html.P("Filter by Team"),
    checklist_teams
])

r2c4 = html.Div(className='columns', children=[
    r2c4r1,
    r2c4r2
], style={'width': '10%'})

# Putting rows and columns togehter
r1 = html.Div(className='row', children=[
    r1c1,
    r1c2,
    r1c3,
    r1c4
])

r2 = html.Div(className='row', children=[
    r2c1,
    r2c2,
    r2c3,
    r2c4
])

app.layout = html.Div(children=[
    r1,
    r2
])


@app.callback(Output('stats_bar_chart', 'figure'),
              Output('bar_chart_label', 'children'),
              Output('fantasy_table', "data"),
              Output('fantasy_table', 'columns'),
              Output('player_image', 'src'),
              Output('player_barChart', 'figure'),
              Output("box_plot", "figure"),
              Input('team_selector', 'value'),
              Input('season_selector', 'value'),
              Input('feature_selector', 'value'),
              Input('searchName', 'value'),
              Input('fantasy_table', 'selected_rows'))
def update(selected_teams, selected_season, selected_feature, searched_name, selected_rows):
    filtered_data = player_stat
    filtered_player_table = player_table

    if selected_teams != []:
        filtered_data = filtered_data[filtered_data['TEAM_NAME'].isin(
            selected_teams)]
        filtered_player_table = filtered_player_table[filtered_player_table['TEAM_NAME'].isin(
            selected_teams)]

    if selected_season == None:
        selected_season = '2019-20'

    new_bar_chart_label = 'Top Players of the ' + selected_season + ' Season'
    filtered_data = filtered_data[filtered_data['GROUP_VALUE']
                                  == selected_season]
    filtered_player_table = filtered_player_table[filtered_player_table['GROUP_VALUE']
                                                  == selected_season]

    if searched_name != None:
        filtered_player_table = filtered_player_table[
            filtered_player_table["DISPLAY_FIRST_LAST"].str.contains(searched_name, flags=re.IGNORECASE, regex=True)]
    fig = px.box(filtered_data[selected_feature], x=selected_feature).update_layout({
        "plot_bgcolor": 'rgba(0, 0, 0, 0)', "paper_bgcolor": 'rgba(0, 0, 0, 0)',
        'font': {'color': "white"},
        'autosize': True,
        'margin': {'t': 0, 'l': 0, 'b': 50, 'r': 0},
        "yaxis": {"showgrid": False},
        "xaxis": {"showgrid": False},
        "orientation": 270},
    )

    if len(filtered_player_table) == 0:
        url = "https://ak-static.cms.nba.com/wp-content/uploads/logos/leagues/logo-nba.svg"
        player_barChart_x = ['REB', 'AST', 'TOV', 'STL', 'BLK', 'PTS']
        player_barChart_data = {
            'data': [
                {'x': player_barChart_x, 'y': [
                    0, 0, 0, 0, 0, 0], 'type': 'bar'}
            ], 'layout': {
                "plot_bgcolor": 'rgba(0, 0, 0, 0)', "paper_bgcolor": 'rgba(0, 0, 0, 0)',
                'font': {'color': "white"},
                'autosize': True,
                'margin': {'t': 0, 'l': 0, 'b': 50, 'r': 0},
                "yaxis": {"showgrid": False}
            }
        }

        if selected_feature == None:
            return make_bar_chart(filtered_data), new_bar_chart_label, None, None, url, player_barChart_data, fig
        else:
            return make_bar_chart(filtered_data,
                                  x_feature=selected_feature), new_bar_chart_label, None, None, url, player_barChart_data, fig

    filtered_player_table = filtered_player_table.drop(
        ["GROUP_VALUE", "TEAM_NAME"], axis=1)

    person_name = filtered_player_table.iloc[selected_rows]["DISPLAY_FIRST_LAST"].values[0]
    person_id = filtered_data.loc[filtered_data["DISPLAY_FIRST_LAST"]
                                  == person_name]["PERSON_ID"]
    url = 'https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png'.format(
        str(person_id.values[0]))

    player_barChart_x = ['REB', 'AST', 'TOV', 'STL', 'BLK', 'PTS']
    player_barChart_y = filtered_data.loc[filtered_data["DISPLAY_FIRST_LAST"]
                                          == person_name][player_barChart_x]
    game_played = filtered_data.loc[filtered_data["DISPLAY_FIRST_LAST"]
                                    == person_name]["GP"]
    if selected_season != "2020-21":
        player_barChart_y /= game_played.values[0]
    player_barChart_data = {
        'data': [
            {'x': player_barChart_x, 'y': player_barChart_y.values.tolist()[
                0], 'type': 'bar'}
        ], 'layout': {
            "plot_bgcolor": 'rgba(0, 0, 0, 0)', "paper_bgcolor": 'rgba(0, 0, 0, 0)',
            'font': {'color': "white"},
            'autosize': True,
            'margin': {'t': 0, 'l': 0, 'b': 50, 'r': 0},
            "yaxis": {"showgrid": False}
        }
    }
    filtered_player_table.columns = ["Rank", "Player Name", "Fantasy Points"]
    data = filtered_player_table.to_dict("records")
    columns = [{"name": i, "id": i} for i in filtered_player_table.columns]

    if selected_feature == None:
        return make_bar_chart(filtered_data), new_bar_chart_label, data, columns, url, player_barChart_data, fig
    else:
        return make_bar_chart(filtered_data,
                              x_feature=selected_feature), new_bar_chart_label, data, columns, url, player_barChart_data, fig


if __name__ == '__main__':
    print('starting the app')
    app.run_server()
