from click import style
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import altair as alt
from vega_datasets import data

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server

# Plotting
cars = data.cars()

# Layout Components
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

plot1 = html.Iframe(
    id = 'scatter',
    style = {'width': '100%', 'height': '400px'}
)

app.layout = dbc.Container([
    navbar,
    dbc.Alert("alert!", color="primary"),
    html.P('words', id = 'text'),
    dcc.Slider(
        min = 1,
        max = 5,
        value = 1,
        id = 'sldr',
        updatemode = 'drag'),
    plot1,
    dbc.Row([
        dbc.Col(html.P('X axis variable: ')),
        dbc.Col(
            dcc.Dropdown(
                id = 'xcol',
                value = 'Horsepower',
                options = [{'label': col, 'value': col} for col in cars.columns],
                clearable = False
            )
        ),
    ]),
    dbc.Row([
        dbc.Col(html.P('Y axis variable: ')),
        dbc.Col(
            dcc.Dropdown(
                id = 'ycol',
                value = 'Weight_in_lbs',
                options = [{'label': col, 'value': col} for col in cars.columns],
                clearable = False   
            )
        )
    ]),
    dbc.Row([
        dbc.Col(html.P('Color variable')),
        dbc.Col(
            dcc.Dropdown(
                id = 'ccol',
                value = 'Miles_per_Gallon',
                options = [{'label': col, 'value': col} for col in cars.columns],
                clearable = False
            )
        )
    ])
])

@app.callback(
    Output('text', 'style'),
    Input('sldr', 'value')
)
def txt_size(s):
    return {'fontSize': f'{s}em'}

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol', 'value'),
    Input('ycol', 'value'),
    Input('ccol', 'value')
)
def plot_cars(x, y, c):
    chart = alt.Chart(
        cars
    ).encode(
        x = x,
        y = y,
        color = c
    ).mark_point()

    return chart.interactive().to_html()

if __name__ == '__main__':
    app.run_server(debug=True)