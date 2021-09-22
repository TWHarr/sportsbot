"""Extracts data, charts games by league."""
import settings
import pandas as pd
import peewee
from peewee import *
import chart_studio.plotly as py
import plotly.graph_objects as go

db = MySQLDatabase(settings.dbname,
                   user=settings.dbuser,
                   passwd=settings.dbpasswd)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class games(BaseModel):
    matchdate = peewee.DateTimeField()
    hometeam = peewee.CharField()
    awayteam = peewee.CharField()
    homescore = peewee.IntegerField()
    awayscore = peewee.IntegerField()
    league = peewee.CharField()
    stage = peewee.CharField()
    view = peewee.CharField()


class leagues(BaseModel):
    leagues = peewee.CharField()
    sports = peewee.CharField()


rq = db.execute_sql("""select a.leagues, COUNT(b.hometeam) number, a.sports
                    from leagues a join games b on b.league=a.leagues GROUP BY
                    a.leagues ORDER BY number DESC LIMIT 20""")

toPandas = []

for row in rq.fetchall():
    toPush = (row[0], int(row[1]), row[2])
    toPandas.append(toPush)

toPandas = tuple(toPandas)

df = pd.DataFrame([[ij for ij in i] for i in toPandas])
df.rename(columns={0: 'League', 1: 'Games', 2: 'Sport'}, inplace=True)

colors = dict(
    Soccer='#1f77b4',
    Hockey='#D21E27',
    Baseball='#2ca02c',
    Football='#FC7E1A',
    Basketball='#9264BC',
    Esports='#8C564B',
    T20='#D372B7'
)
color = []

for index, row in df.iterrows():
    color.append(colors[row['Sport']])


data = [
    go.Bar(
        x=df['League'],
        y=df['Games'],
        text=df['Sport'],
        marker=dict(
            color=color
        )
    )
]

fig = go.Figure(data=data)
fig.update_layout(title="Games by League")
fig.update_xaxes(title_text="League (Top 20)")
fig.update_yaxes(title_text="Games Watched")
py.plot(fig, filename='GamesByLeague')
