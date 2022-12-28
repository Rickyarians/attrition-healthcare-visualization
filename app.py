from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Create dash app instance
app = Dash(external_stylesheets=[dbc.themes.LUX])

# Dashboard Title
app.title = 'Dashboard Employee Attrition for Healthcare'

# Dashboard Component

## 1. NAVBAR
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    ],
    brand="Employee Attrition for Healthcare Dashboard",
    brand_href="#",
    color="#618685",
    dark=True,
)

## 2. Load Data Set

healthcare_data = pd.read_csv('watson_healthcare_modified.csv')
healthcare_data1 = healthcare_data.copy()
healthcare_data1['Attrition'] = healthcare_data1['Attrition'].map({'Yes': 1, 'No': 0})

## 3. Card Content
#### Card Content 1
information_card = [
    dbc.CardHeader('Information'),
    dbc.CardBody([
        html.P('This is the information of employeed in our Company.'),
    ])
]

#### Card Content 2
employee_card = [
    dbc.CardHeader('Total Employee'),
    dbc.CardBody([
        html.H1(healthcare_data.shape[0])
    ]),
]

#### Card Content 3
promotion_card = [
    dbc.CardHeader('Number of employees Attrition'),
    dbc.CardBody([
        html.H1(healthcare_data[healthcare_data['Attrition']=='Yes'].shape[0], style={'color':'red'})
    ]),
]


# ### Barplot1
data_agg = healthcare_data.groupby(['Department', 'Attrition']).count()[['EmployeeID']].reset_index()
data_agg = data_agg.sort_values(by = 'EmployeeID', ascending=False)
bar_plot1 = px.bar(
    data_agg,
    x = 'Department',
    y = 'EmployeeID',
    color = 'Attrition',
    color_discrete_sequence = ['#618685','#80ced6'],
    barmode = 'group',
    labels = {
        'Department': 'Department',
        'EmployeeID': 'No of Employee',
        'Attrition': 'Attrition',
    },
    title = 'Total Attrition employees in each Department',
    height = 700
).update_layout(showlegend=False)


data_educationfield_attrition = healthcare_data.groupby(['EducationField', 'Attrition']).count()[['EmployeeID']].reset_index()
data_educationfield_attrition = data_educationfield_attrition.sort_values(by = 'EmployeeID', ascending=False)
bar_data_educationfield_attrition = px.bar(
   data_educationfield_attrition,
    x = 'EducationField',
    y = 'EmployeeID',
    color = 'Attrition',
    color_discrete_sequence = ['#618685','#80ced6'],
    barmode = 'group',
    labels = {
        'EducationField': 'Education Field',
        'EmployeeID': 'Total of Employee',
        'Attrition': 'Attrition',
    },
    title = 'Total Attrition employees in each Education Field',
    height = 700
).update_layout(showlegend=False)


data_agg1 = healthcare_data1.groupby(['OverTime'])['Attrition'].sum().reset_index()
bar_plot2 = px.bar(
    x = data_agg1['OverTime'],
    y = data_agg1['Attrition'],
    color=['#618685','#80ced6'],
    color_discrete_map="identity",
    labels = {
        'y': 'Count',
        'x': 'Overtime'
    },
    title = 'Relation between Attrition and Overtime',
    height = 700
).update_layout(showlegend=False)

data_gender_attrition = healthcare_data1.groupby(['Gender'])['Attrition'].sum().reset_index()
pie_gender_attrition = px.pie(
    data_gender_attrition, 
    names="Gender" , 
    values='Attrition', 
    color="Gender",
    title = "The Percentage of Employee Attrition per Gender",
    color_discrete_map={
        'Male':'#618685',
        'Female':'#80ced6',
    })

# User Interface
app.layout = html.Div([
    navbar,
    html.Br(),

    #### ----ROW1----
    dbc.Row([

        ## Row 1 Col 1
        dbc.Col(dbc.Card(information_card, color='#fefbd8'), width=6),

        ## Row 1 Col 2
        dbc.Col(dbc.Card(employee_card, color='#80ced6'), width=3),

        # Row 1 Col 3
        dbc.Col(dbc.Card(promotion_card, color='#d5f4e6'), width=3),

    ]),

    html.Br(),

    ### ----ROW2----
    dbc.Row([

        # Row 2 Col 1
        dbc.Col(dbc.Tabs([
            # Tab 1
            dbc.Tab(dcc.Graph(figure=bar_plot1),
            label='Each Department'),

            # Tab 2
            dbc.Tab(dcc.Graph(figure=bar_data_educationfield_attrition),
            label='Education Field'),

            dbc.Tab(dcc.Graph(figure=bar_plot2),
            label='Overtime'),

            dbc.Tab(dcc.Graph(figure=pie_gender_attrition),
            label='Gender'),
        ])),

        # Row 2 Col 2
        dbc.Col([
            dcc.Dropdown(
                id='choose_dept',
                options=healthcare_data['Department'].unique(),
                value='Maternity',
            ),
            dcc.Graph(id='plot3'),
        ]),

    ]),
])

@app.callback(
    Output(component_id='plot3', component_property='figure'),
    Input(component_id='choose_dept', component_property='value')
)

def update_plot(dept_name):
    data_agg = healthcare_data[healthcare_data['Department'] == dept_name]
    hist_plot3 = px.histogram(
        data_agg,
         x = 'YearsAtCompany',
        nbins = 20,
        color_discrete_sequence = ['#618685','#80ced6'],
        title = f'Length of Service Distribution in {dept_name} Department',
        template = 'ggplot2',
        labels={
            'YearsAtCompany': 'Years At Company (years)',
        },
        marginal = 'box',
        height=700,
    )
    return hist_plot3

# Run app at local
if __name__ == '__main__':
    app.run_server(debug=True)