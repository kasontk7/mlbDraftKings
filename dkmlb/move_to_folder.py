import os
from pathlib import Path

fangraph_path = Path("/Users/kasonkang/Downloads/FanGraphs Leaderboard.csv")
salary_path = Path("/Users/kasonkang/Downloads/DKSalaries.csv")
if fangraph_path.exists():
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard.csv", "/Users/kasonkang/Documents/Projects/dkmlb/projected_pitchers.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (1).csv", "/Users/kasonkang/Documents/Projects/dkmlb/vsleft_pitchers.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (2).csv", "/Users/kasonkang/Documents/Projects/dkmlb/vsright_pitchers.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (3).csv", "/Users/kasonkang/Documents/Projects/dkmlb/batters.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (4).csv", "/Users/kasonkang/Documents/Projects/dkmlb/batters2.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (5).csv", "/Users/kasonkang/Documents/Projects/dkmlb/last7batters.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (6).csv", "/Users/kasonkang/Documents/Projects/dkmlb/left_batters.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (7).csv", "/Users/kasonkang/Documents/Projects/dkmlb/right_batters.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (8).csv", "/Users/kasonkang/Documents/Projects/dkmlb/relief.csv")
	os.rename("/Users/kasonkang/Downloads/hot-batters.csv", "/Users/kasonkang/Documents/Projects/dkmlb/hot_batters.csv")
	os.rename("/Users/kasonkang/Downloads/cold-batters.csv", "/Users/kasonkang/Documents/Projects/dkmlb/cold_batters.csv")
	os.rename("/Users/kasonkang/Downloads/mlb-pitcher.csv", "/Users/kasonkang/Documents/Projects/dkmlb/mlb_pitchers.csv")

if salary_path.exists():
	os.rename("/Users/kasonkang/Downloads/DKSalaries.csv", "/Users/kasonkang/Documents/Projects/dkmlb/DKSalaries.csv")

