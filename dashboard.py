import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jupyter_dash import JupyterDash
from dash import Dash, html, dcc, Input, Output
from plotly.graph_objs import *

# BOX PLOT
# tabella inerente a LCOE delle principali fonti energetiche di interesse
df1 = pd.read_excel(r"C:/Users/giorg/Downloads/lcoe_definitive.xlsx")

# vettore delle fonti
source = ['Coal', 'Gas Turbine', 'Nuclear', 'Hydro', 'SolarPV', 'WindOnShore']
# vettore discount rates
rate = ['0.03','0.04','0.05', '0.06', '0.07', '0.10']


# CHOROPLETH
df = pd.read_excel(r"C:/Users/giorg/Downloads/energy_consumption_by_fuel.xlsx")
# df.columns
# creo vettore contenente nomi delle varie fonti energetiche, ovvero le colonne di df
sources = [ 'Oil ','Natural Gas ', 'Coal ', 'Nuclear ', 'Hydro ', 'Renewables',
       'Oil variation', 'Natural Gas Variation',
       'Coal Variation', 'Nuclear Variation', 'Hydro Variation',
       'Renewables Variation', 'OilperCap', 'NaturalGasPerCap', 'CoalPerCap',
       'NuclearPerCap', 'HydroPerCap', 'RenewablesPerCap']



# BAR CHART
df6 = pd.read_excel(r"C:/Users/giorg/Downloads/EmissionsCO2.xlsx")
emission = 'Italy'


# SCATTER PLOT for LCOE 
lcoe = pd.read_excel(r"C:/Users/giorg/Downloads/LCOE.xlsx")
country = lcoe['Country'].values.tolist()
set_country = set(country)
country = (list(set_country))


app = JupyterDash(__name__)

app.layout = html.Div([
    html.H1("Energy consumption and efficiency in the world"),
    html.Div([##############################LEFT SIDE ############
        html.P('Select the type of energy source '),
        dcc.Dropdown(sources, 
            value = 'Natural Gas ',
            id = 'sources_input',
            className='dropdown'),#class name per il binding con il css
        html.Div([ #CHOROPLETH_GRAPH
             dcc.Graph(id="choro_output"),
        ],id='choro'),
        html.P('Select the desired discount rate '),
        html.Div([
            dcc.RadioItems([0.03,0.04,0.05, 0.06, 0.07, 0.10],
                value = 0.10,
                id = 'discount_input',
                className='radio',
            ),
        ],id='radio'),
        
        html.Div([ #BOX PLOT GRAPH
            dcc.Graph(id="box_output")
        ],className='table'),
    ],id='left-container'),
    html.Div([ ############################## RIGHT SIDE ##########
        html.P('Select a country for comparison '),
        dcc.Dropdown(df6.Country, 
            value = 'country',
            id = 'country_input',
            className='dropdown'), 
        html.Div([ #BARS GRAPH
             dcc.Graph(id="bar_output"),
        ],className='table'),
        html.P('Select the desired country to compare costs'),
        dcc.Dropdown(country, 
            value = 'United States of America',
            id = 'country1_input',
            className='dropdown'),
        html.Div([ #SCATTER GRAPH
            dcc.Graph(id="scatter_output"),
        ],id='scatter'),
    ],id='right-container'),
],id='container',)




# CHOROPLETH    
@app.callback(Output(component_id = 'choro_output', component_property = 'figure'),  
              Input(component_id = 'sources_input', component_property = 'value'))

def update_choropleth_output(source):
    layout = Layout(
    # PINK
    # paper_bgcolor='rgb(253, 205, 172)',
    paper_bgcolor='rgb(0, 0, 0)',
    plot_bgcolor='rgb(214, 137, 16)',
    geo_bgcolor='rgb(0, 0, 0)',
    )
    
    # devo aggiornare valore unità di misura in base a input dell'utente
    unit = 'EJ '
    colorbar = 'Consumption '
    if source == 'Oil variation'or source =='Natural Gas Variation'or source == 'Coal Variation'or source == 'Nuclear Variation'or source == 'Hydro Variation'or source == 'Renewables Variation':
        unit = '% ' 
        colorbar = 'Variation '



    
    fig = go.Figure(data=go.Choropleth(
        locations = df['Country'],
        locationmode = 'country names',
        z = df[source],
        text = df['Country'],
        colorscale = 'agsunset',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = unit,
        colorbar_title = colorbar,
        colorbar_titlefont = {"color":'rgb(255, 255, 255)'},
        colorbar_tickfont = {"color":'rgb(255, 255, 255)', "size": 20}
        ),
        layout=layout)

    fig.update_layout( 
    title={
        'text': 'Energy consumption by country',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    title_font_color='#ffffff',
    title_font_size=30,
    title_font_family="Calibri",
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    hoverlabel=dict(
            font_size=26,
            font_family="Calibri"
        ),
    

    # MAP RESHAPING
    margin=dict(l=60, r=60, t=50, b=50)
    
    # annotations = [dict(
    #     x=0.52,
    #     y=0.14,
    #     xref='paper',
    #     yref='paper',
    #     text='Source: <a href="https://www.bp.com/en/global/corporate/energy-economics/statistical-review-of-world-energy.html">\
    #         BP Statistical Review</a>',
    #     showarrow = False
    #  )]
    )
    return fig





# BOX PLOT
@app.callback(Output(component_id = 'box_output', component_property = 'figure'),
              Input(component_id = 'discount_input', component_property = 'value'))

def update_boxPlot_output(discount):
  colors = ['rgba(93, 164, 214, 0.8)', 'rgba(255, 144, 14, 0.8)', 'rgba(44, 160, 101, 0.8)',
    'rgba(255, 65, 54, 0.8)', 'rgba(207, 114, 255, 0.8)', 'rgba(127, 96, 0, 0.8)']
  df2 = df1.loc[df1['FuelType'] == 'Coal'] 
  df3 = df2.loc[df2['DiscountRate'] == discount] 
  # capex = df3['CAPEX']
  # capex = capex.drop_duplicates()
  # lcoe for every fuel type
  df3 = df3.loc[df2['CAPEX'] == discount] 

  coal = df1.loc[df1['FuelType'] == 'Coal'] 
  coal = coal.loc[coal['DiscountRate'] == discount]
  lcoeCoal = coal.LCOE.values.tolist()

  gas = df1.loc[df1['FuelType'] == 'Gas Turbine'] 
  gas = gas.loc[gas['DiscountRate'] == discount]
  lcoeGas = gas.LCOE.values.tolist()

  hydro = df1.loc[df1['FuelType'] == 'Hydro'] 
  hydro = hydro.loc[hydro['DiscountRate'] == discount]
  lcoeHydro = hydro.LCOE.values.tolist()

  nuclear = df1.loc[df1['FuelType'] == 'Nuclear'] 
  nuclear = nuclear.loc[nuclear['DiscountRate'] == discount]
  lcoeNuclear = nuclear.LCOE.values.tolist()

  solar = df1.loc[df1['FuelType'] == 'SolarPV'] 
  solar = solar.loc[solar['DiscountRate'] == discount]
  lcoeSolar = solar.LCOE.values.tolist()

  wind = df1.loc[df1['FuelType'] == 'WindOnShore'] 
  wind = wind.loc[wind['DiscountRate'] == discount]
  lcoeWind = wind.LCOE.values.tolist()
  lcoeWind

  lcoe = [lcoeCoal, lcoeGas ,lcoeHydro, lcoeNuclear, lcoeSolar, lcoeWind]

  fig = go.Figure()

  for xd, yd, cls in zip(source, lcoe, colors):
          fig.add_trace(go.Box(
              y=yd,
              name=xd,
              boxpoints='all',
              jitter=0.5,
              whiskerwidth=0.3,
              fillcolor=cls,
              marker_size=4,
              line_width=3)
          )

  fig.update_layout(
    title={
        'text': 'LCOE by type of fuel',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    title_font_color='rgb(255, 255, 255)',
    title_font_size=30,
    title_font_family="Calibri",

      yaxis=dict(
          autorange=True,
          showgrid=True,
          zeroline=False,
          dtick=15,
          gridcolor='rgb(255, 255, 255)',
          gridwidth=0.3,
          zerolinecolor='rgb(255, 255, 255)',
          zerolinewidth=0.5,
          color = 'rgb(255, 255, 255)',
          tickfont=dict(
                    family='Arial',
                    size=20,
                    color='rgb(255, 255, 255)'),
      ),
      xaxis = dict(color = 'rgb(255, 255, 255)',
            tickfont=dict(
                    family='Arial',
                    size=20,
                    color='rgb(255, 255, 255)'),),
      margin=dict(
          l=40,
          r=30,
          b=80,
          t=100,
      ),
      # paper_bgcolor='rgb(229, 196, 148)',
      paper_bgcolor='rgb(0, 0, 0)',
      # plot_bgcolor='rgb(243, 243, 243)',
      # BLACK
      plot_bgcolor='rgb(0, 0, 0)',
      # GREY
      # plot_bgcolor='#222A2A',
      showlegend=False,
      transition = {'duration': 2000},
      hoverlabel=dict(
            font_size=26,
            font_family="Calibri"
        )
  )
  return fig





# BAR CHART
@app.callback(Output(component_id = 'bar_output', component_property = 'figure'),
              Input(component_id = 'country_input', component_property = 'value'))

def update_barChart_output(country):
    # seleziono solo righe corrispondenti a paesi di interesse
    # tengo conto che utente puo selezionarne uno a sua scelta
    countries = ['China', 'United States', 'India', 'Russia', 'Japan', 'Germany', 'Canada', 'Iran']
    countries.append(country)
    emissions = df6.loc[df6['Country'].isin(['China', 'United States', 'India', 'Russia', 'Japan', 'Germany', 'Canada', 'Iran', country])]

    # faccio proiezione sulle due colonne di interesse
    emissions = emissions[["PerCapita", "Share"]]


    bar_data = go.Bar(
            x = countries,
            y = emissions.Share,
            name = 'GlobalShare(%)',
            #   text = sales1.groupby('PRODUCTLINE')['SALES'].sum(),
            #   texttemplate = '%{text:.2s}',
            #   textposition = 'inside',
            marker = dict(color='rgb(228, 26, 28)'),
            yaxis = 'y1',
            offsetgroup=1
    )

    line_data = go.Bar(
            x = countries,
            y = emissions.PerCapita,
            name = 'PerCap(CO2tons)',
            #   text = sales1.groupby('PRODUCTLINE')['QUANTITYORDERED'].sum(),
            #   texttemplate = '%{text:.2s}',
            #   textposition = 'inside',
            marker = dict(color='#3282FE'),
            yaxis = 'y2',   
            offsetgroup=2
    ) 


    data = [bar_data, line_data]

    layout = go.Layout(
        barmode='group',
        title = 'CO2 Emissions by Country',
        hovermode = 'closest',
        
        xaxis=dict(title='Countries',
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(255, 255, 255)',
                    linewidth=2,
                    ticks='outside',
                    color = 'rgb(255, 255, 255)',
            tickfont=dict(
                    family='Arial',
                    size=20,
                    color='rgb(255, 255, 255)',
            ),
                
        ),
        yaxis=dict(title='Global Share',
                   title_font_size=22,
                   color = 'rgb(255, 255, 255)',
                    tickfont=dict(
                    family='Arial',
                    size=20,
                    color='rgb(255, 255, 255)'),
                   ),
        yaxis2=dict(title='Emission perCap', side='right',overlaying='y',
                    title_font_size=18,
                    color = 'rgb(255, 255, 255)',
                    tickfont=dict(
                    family='Arial',
                    size=20,
                    color='rgb(255, 255, 255)'),
                    ),
        
        legend=dict(
            orientation='v',
            bgcolor='rgba(255, 255, 255)',
            bordercolor='rgba(255, 255, 255)',
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            traceorder="normal",
            font=dict(
                family="Arial",
                size=20,
                color='rgb(255, 255, 255)'
            ),
        )
        
    )

    figure2 = go.Figure(data=data, layout=layout)
    figure2.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    # figure2.update_layout(legend_title='<b> Emission Type: </b>')
    figure2.update_layout(legend=dict(
        yanchor="top",
        y=1.05,
        xanchor="left",
        x=1,
        title_font_size=20,
    ))

    figure2.update_layout(
        # paper_bgcolor='rgb(229, 196, 148)',
        paper_bgcolor='rgb(0, 0, 0)',
        # BLACK
        plot_bgcolor='rgb(0, 0, 0)',
        title_font_family="Calibri",
        title_font_color='rgb(255, 255, 255)',
        title_font_size=30,
        legend_title_font_color='rgb(255, 255, 255)',
        font=dict(
            size=22,
        ))

    figure2.update_layout(
        title={
            'text': 'Global Emissions of CO2',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            hoverlabel=dict(
            font_size=26,
            font_family="Calibri"
        )
        )


    return figure2





# SCATTER PLOT
@app.callback(Output(component_id = 'scatter_output', component_property = 'figure'),  
              Input(component_id = 'discount_input', component_property = 'value'),
              Input(component_id = 'country1_input', component_property = 'value'))


def update_scatter_output(discount_rate, country):
    fixed_discount = lcoe.loc[lcoe['DiscountRate'] == discount_rate]
    fixed_discount1 = fixed_discount.loc[fixed_discount['Country'] == country] 
    
    layout = go.Layout(
        barmode='group',
        title = 'CO2 Emissions by Country',
        hovermode = 'closest',
        
        xaxis=dict(title='Construction Cost ($/MWh)',  
                   title_font_size=24, 
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(255, 255, 255)',
                    linewidth=2,
                    ticks='outside',
                    color = 'rgb(255, 255, 255)',
            tickfont=dict(
                    family='Arial',
                    size=20,
                    color='rgb(255, 255, 255)',
            ),
                
        ),
        yaxis=dict(title='LCOE($/MWh)',
                   title_font_size=24,
                   color = 'rgb(255, 255, 255)',
                   tickfont=dict(
                    family='Arial',
                    size=20,
                    color='rgb(255, 255, 255)'),),
    )
    
    fig = go.Figure(data=go.Scatter(
        x = fixed_discount1.ConstructionCost,
        y = fixed_discount1.LCOE,
        mode='markers',
        text=fixed_discount1.PlantCategory,
        marker=dict(
            size=20,
            color= fixed_discount1.OandMCosts,
            colorscale = 'agsunset',
            autocolorscale=False,
            reversescale=True,
            showscale = True,
            colorbar_title = 'O&MCost',
            colorbar_ticksuffix = ' $/MWh',
            colorbar_titlefont = {"color":'rgb(255, 255, 255)'},
            colorbar_tickfont = {"color":'rgb(255, 255, 255)', "size": 20}
        )), 
        layout = layout
    )
    
    
    fig.update_layout(
        transition = {'duration': 2000},
        #paper_bgcolor='rgb(229, 196, 148)',
        title={
            'text': 'LCOE by country',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        title_font_color='rgb(255, 255, 255)',
        title_font_size=30,
        title_font_family="Calibri",
        paper_bgcolor='rgb(0, 0, 0)',
        plot_bgcolor='rgb(0, 0, 0)'
        )
    
    fig.update_layout(
        title_text='LCOE by country',
        transition = {'duration': 2000},
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        hoverlabel=dict(
            font_size=26,
            font_family="Calibri"
        )
        )
    
    fig.update_traces(marker=dict(size=24,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    
    return fig

app.run_server(debug = False)
