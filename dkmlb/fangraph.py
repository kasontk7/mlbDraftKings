import webbrowser
import datetime

now = datetime.datetime.now()
today_date = now.strftime("%Y-%m-%d")

proj_pitcher_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=sta&lg=all&qual=0&type=1&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
proj_pitcher_url2 = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=sta&lg=all&qual=0&type=1&season=2019&month=3&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
vsleft_pitcher_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2019&month=13&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
vsright_pitcher_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2019&month=14&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
batters_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0"
batters2_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=2&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0"
last7batters_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0"
left_batters_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=13&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0"
right_batters_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=14&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0"
matchups_url = "https://www.rotowire.com/baseball/stats-bvp.php"
pitchers_proj_url = "https://rotogrinders.com/projected-stats/mlb-pitcher?site=draftkings"
relief_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=8&season=2019&month=0&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0"

webbrowser.open(proj_pitcher_url2 + today_date)
webbrowser.open(vsleft_pitcher_url + today_date)
webbrowser.open(vsright_pitcher_url + today_date)
webbrowser.open(batters_url)
webbrowser.open(batters2_url)
webbrowser.open(last7batters_url)
webbrowser.open(left_batters_url)
webbrowser.open(right_batters_url)
webbrowser.open(relief_url)
webbrowser.open(pitchers_proj_url)
webbrowser.open(matchups_url)


