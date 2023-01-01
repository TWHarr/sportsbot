
/*Cumulative watched for a year*/
SELECT SUM(gtime)
FROM games a
    JOIN leagues b ON a.league = b.leagues
    JOIN gametime c on b.sports = c.sport
WHERE YEAR(matchdate)=2016

/*Games by sport for the year*/
SELECT
    count(a.id),
    b.sports
FROM
    games a
    JOIN leagues b ON a.league = b.leagues
WHERE
    YEAR(a.matchdate) = 2022
GROUP BY
    b.sports
ORDER BY
    count(a.id)
    DESC;

/*Games by view for the year*/
SELECT
    count(a.id),
    a.view
FROM
    games a
    WHERE
    YEAR(a.matchdate) = 2022
GROUP BY
    a.`view`
ORDER BY
    count(a.id)
    DESC;

/*Hours by Sport*/
SELECT
    sum(c.gtime),
    c.sport
FROM
    games a
    JOIN leagues b ON a.league = b.leagues
    JOIN gametime c ON b.sports = c.sport
WHERE
    YEAR(a.matchdate) = 2022
GROUP BY
    c.sport
ORDER BY
    sum(c.gtime)
    DESC;

/*Hours by League*/
SELECT
    sum(c.gtime),
    a.league
FROM
    games a
    JOIN leagues b ON a.league = b.leagues
    JOIN gametime c ON b.sports = c.sport
WHERE
    YEAR(a.matchdate) = 2022
GROUP BY
    a.league
ORDER BY
    sum(c.gtime)
    DESC;

/*Total count of games*/
SELECT
    count(a.id)
FROM
    games a
WHERE
    YEAR(a.matchdate) = 2022;

/*Games per team by year*/
SELECT
    a.team,
    count(a.id),
    a.sports
FROM (
    SELECT
        a.hometeam AS team,
        a.id,
        b.sports
    FROM
        games a
        JOIN leagues b ON a.league = b.leagues
    WHERE
        YEAR(a.matchdate) = 2022
    UNION
    SELECT
        a.awayteam AS team,
        a.id,
        b.sports
    FROM
        games a
        JOIN leagues b ON a.league = b.leagues
    WHERE
        YEAR(a.matchdate) = 2022) a
GROUP BY a.team, a.sports
ORDER BY count(a.id) desc
LIMIT 10;

