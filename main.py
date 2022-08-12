import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.YvXRyOzMI0Q"

# 1. Download the web page
page = requests.get(url)

# 2. Parse the page using bs
soup = BeautifulSoup(page.content, "html.parser")

# 3. Find element with id "seven-day-forecast"
seven_day_forecast = soup.find(id="seven-day-forecast")

# 4. Get forecast for each of 7 periods
# 5. Extract the data for each forecast item
# 5.1 Get the period tags & extract the content
period_tags = seven_day_forecast.select(".tombstone-container .period-name")
periods = [p.get_text(strip=True) for p in period_tags]

# 5.2 Get the short-desc tags & extract the content
short_desc_tags = seven_day_forecast.select(".tombstone-container .short-desc")
# Use of separator to replace any nested tags with space, such as <br/>
short_descs = [sd.get_text(separator=" ", strip=True) for sd in short_desc_tags]

# 5.3 Get the temp tags & extract the content
temp_tags = seven_day_forecast.select(".tombstone-container .temp")
temps = [t.get_text(strip=True) for t in temp_tags]

# 5.4 Get the full desc tags (in img tags) & extract the content
img_tags = seven_day_forecast.select(".tombstone-container img")
descs = [d.get("title") for d in img_tags]  # The desc is in the attr. title of img tag

# 6. Construct Panda dataframe (tabular object)
weather = pd.DataFrame(
    {"period": periods, "short_desc": short_descs, "temp": temps, "desc": descs}
)

# print(weather.to_string())

# pd.set_option("display.max_columns", 1000)  # or 1000
# pd.set_option("display.max_rows", 1000)  # or 1000
# pd.set_option("display.max_colwidth", None)  # or 199
# more options can be specified also
# with pd.option_context("display.max_rows", None, "display.max_columns", None):
#     print(weather)

# 7. Analysis
# 7.1 Get all temp nums as integers
# (?P<named_group>d+) means find any matching group (named or unaming group) that satisfies regex d+
# https://stackoverflow.com/questions/7988942/what-does-this-django-regular-expression-mean-p
# temp_nums = weather["temp"].str.extract("(?Pd+)", expand=False)
# weather["temp_num"] = temp_nums.astype("int")

# Extract temps and convert to ints
temp_nums = weather["temp"].str.extract(r"(\d+)", expand=False)
ts = temp_nums.astype("int")
weather["temp_nums"] = ts
print(weather["temp_nums"].mean())  # Get the mean temp

# Add a col specifying whether a period is during day (High temp) or night (Low temp)
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night  # Boolean value
