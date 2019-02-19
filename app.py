import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import matplotlib.pyplot as plt

#below library is to make wordcloud
import pprint
import numpy as np



# Plotly
import plotly.plotly as py
import plotly.tools as tls
import seaborn as sns
# Matplotlib
import matplotlib.pyplot as plt


df = pd.read_csv('airline-sentiment-tweets/train.csv')
## Generating the data..



####################

#Visualizing 'airline_sentiment' and 'airline'
mpl2_fig = plt.figure()
g = mpl2_fig.add_subplot(111)
g = sns.catplot(x='airline', data=df, order=['Virgin America', 'United'], kind="count",  hue='negativereason', height=6, aspect=0.9)
#ax = sns.factorplot(x='airline', data=df,order=['Virgin America', 'United'], kind='count', hue='negativereason', size=6, aspect=0.9)
plt.title('Overall Sentiment')
plt.show()
plotly_fig2 = tls.mpl_to_plotly(mpl2_fig)
#####################

app = dash.Dash(__name__)
server = app.server
pos_words = ''

#show only selected column in table
map_data = df[["text",'airline_sentiment']].drop_duplicates()
#wordcloud
wordcloud = df[["text", 'airline_sentiment']].drop_duplicates()
app = dash.Dash()

colors = {"background": "#F3F6FA", "background_div": "white"}
PAGE_SIZE = 5

for index, row in df.iterrows():
	if(row['airline_sentiment'] =="positive"):
		pos_words = pos_words + row['text']
    	#print(row['text'], file=sys.stdout)



# Libraries



app.layout = html.Div([
   		html.Img(src='/plot.png'),
        html.H1('LavaVino'),
        html.H3('Volcanic Wines of the World...'),
        html.Div(style={'width': '400px'}, children=[
            html.H1('Social Media Analysis'),
            dcc.Graph(id='example',
                      figure={
                          'data': [
                              {'x': [1, 2, 3, 4, 5], 'y':[5, 6, 3, 5, 2],
                              	'type':'line', 'name':'boats'},
                              {'x': [1, 2, 3, 4, 5], 'y':[8, 6, 2, 4, 2],
                              	'type':'bar', 'name':'cars'},
                          ],
                          'layout': {
                              'title': 'line andbar'
                          }
                      })
        ]),
        html.Div(style={'width': '400px'}, children=[
			dash_table.DataTable(
				id='table-paging-and-sorting',
				columns=[
					{'name': i, 'id': i, 'deletable': True} for i in sorted(map_data.columns)
				],
				style_table={'width': '100%'},
				style_data={'whiteSpace': 'normal'},
				content_style='grow',
				css=[{
					'selector': '.dash-cell div.dash-cell-value',
					'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
				}],
				data=map_data.to_dict('rows'),
				style_cell_conditional=[
					{
						'if': {'row_index': 'odd'},
						'backgroundColor': 'rgb(248, 248, 248)'
					}
				] + [
					{
						'if': {'column_id': c},
						'textAlign': 'left'
					} for c in ['airline_sentiment', 'text']
				],
				style_header={
					'backgroundColor': 'white',
					'fontWeight': 'bold'
				},
				pagination_settings={
					'current_page': 0,
					'page_size': PAGE_SIZE
				},
				pagination_mode='be',

				sorting='be',
				sorting_type='single',
				sorting_settings=[]
			)
		]),
  		html.Div(style={'width': '400px'}, children=[
			#dcc.Graph(id='myGraph', figure=plotly_fig)
		]),
  		html.Div(style={'width': '400px'}, children=[
			dcc.Graph(id='myGraph2', figure=plotly_fig2)
		])
], className='two-columns')





#callback
@app.callback(
    Output('table-paging-and-sorting', 'data'),
    [Input('table-paging-and-sorting', 'pagination_settings'),
     Input('table-paging-and-sorting', 'sorting_settings')])
def update_graph(pagination_settings, sorting_settings):
    if len(sorting_settings):
        dff = df.sort_values(
            sorting_settings[0]['column_id'],
            ascending=sorting_settings[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1) *
        pagination_settings['page_size']
    ].to_dict('rows')



if __name__ == '__main__':
	app.run_server(debug=True)
