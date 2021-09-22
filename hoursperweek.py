"""Extract data, chart by hours watched per week.."""
import settings
import peewee
from peewee import *
import chart_studio.plotly as py
import plotly.graph_objects as go
import datetime

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


class gametime(BaseModel):
    sport = peewee.CharField()
    gtime = peewee.IntegerField()


hockeym = []
hockeyg = []
baseballm = []
baseballg = []
soccerm = []
soccerg = []
footballm = []
footballg = []
basketballm = []
basketballg = []
esportsm = []
esportsg = []
T20m = []
T20g = []


def lastmonth():
    a = []
    rq = db.execute_sql(""" SELECT a.matchdate fdate FROM games a
                        where a.matchdate > curdate() - interval
                        (dayofmonth(curdate()) - 1) day - interval 1 week
                        ORDER BY a.matchdate
                        """)
    for row in rq.fetchall():
        a.append(row[0])
    return a


month = lastmonth()
print(month)


def get_week_days(year, week):
    d = datetime.datetime(year, 1, 1)
    if(d.weekday() > 3):
        d = d + datetime.timedelta(7 - d.weekday())
    else:
        d = d - datetime.timedelta(d.weekday())
    dlt = datetime.timedelta(days=(week - 1) * 7)
    return (datetime.datetime.strftime(d + dlt, '%m/%d') + '-' + datetime.datetime.strftime(d + dlt + datetime.timedelta(days=6), '%m/%d'))


def getBaseball():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'baseball' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC """, ('%U/%Y'))
    for row in rq.fetchall():
        if row[0] in month:
            baseballm.append(get_week_days(int(row[0].strftime('%Y')),
                             int(row[0].strftime('%U'))))
            baseballg.append(int(row[1]))


getBaseball()


def gethockey():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'hockey' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC""", ('%U/%Y'))
    for row in rq.fetchall():
        if row[0] in month:
            hockeym.append(get_week_days(int(row[0].strftime('%Y')),
                           int(row[0].strftime('%U'))))
            hockeyg.append(int(row[1]))


gethockey()


def getsoccer():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'soccer' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC""", ('%U/%Y'))
    for row in rq.fetchall():
        if row[0] in month:
            soccerm.append(get_week_days(int(row[0].strftime('%Y')),
                           int(row[0].strftime('%U'))))
            soccerg.append(int(row[1]))


getsoccer()


def getfootball():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'football' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC""", ('%U/%Y'))
    for row in rq.fetchall():
        if row[0] in month:
            footballm.append(get_week_days(int(row[0].strftime('%Y')),
                             int(row[0].strftime('%U'))))
            footballg.append(int(row[1]))


getfootball()


def getbasketball():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'basketball' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC""", ('%U/%Y'))
    for row in rq.fetchall():
        if row[0] in month:
            basketballm.append(get_week_days(int(row[0].strftime('%Y')),
                               int(row[0].strftime('%U'))))
            basketballg.append(int(row[1]))


getbasketball()


def getEsports():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'esports' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC """, ('%U/%Y'))
    for row in rq.fetchall():
        if row[0] in month:
            esportsm.append(get_week_days(int(row[0].strftime('%Y')),
                             int(row[0].strftime('%U'))))
            esportsg.append(int(row[1]))


getEsports()

def getT20():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'T20' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC """, ('%U/%Y'))
    for row in rq.fetchall():
        if row[0] in month:
            T20m.append(get_week_days(int(row[0].strftime('%Y')),
                             int(row[0].strftime('%U'))))
            T20g.append(int(row[1]))


getT20()


trace2 = go.Bar(
    x=footballm,
    y=footballg,
    name='Football'
)

trace1 = go.Bar(
    x=soccerm,
    y=soccerg,
    name='Soccer'
)

trace3 = go.Bar(
    x=baseballm,
    y=baseballg,
    name='Baseball'
)

trace4 = go.Bar(
    x=hockeym,
    y=hockeyg,
    name='Hockey'
)

trace5 = go.Bar(
    x=basketballm,
    y=basketballg,
    name='Basketball'
)

trace6 = go.Bar(
    x=esportsm,
    y=esportsg,
    name='Esports'
)

trace7 = go.Bar(
    x=T20m,
    y=T20g,
    name='T20'
)

data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7]

fig = go.Figure(data=data)
fig.update_layout(title='Hours Per Week', barmode='stack')
fig.update_xaxes(title_text='Week')
fig.update_yaxes(title_text='Hours')
py.plot(fig, filename='Hoursperweek')
