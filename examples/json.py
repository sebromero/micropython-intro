import json

json_data = '''
[
  {
    "date": "2022-05-06",
    "temperatureC": 1,
    "summary": "Freezing",
  },
  {
    "date": "2022-05-07",
    "temperatureC": 14,
    "summary": "Bracing",
  },
  {
    "date": "2022-05-08",
    "temperatureC": -13,
    "summary": "Freezing",
  },
  {
    "date": "2022-05-09",
    "temperatureC": -16,
    "summary": "Balmy",
  },
  {
    "date": "2022-05-10",
    "temperatureC": -2,
    "summary": "Chilly",
  }
]
'''

print("")
object_data = json.loads(json_data)
for weather in object_data:
    print(f"📆 {weather['date']}: 🌡️ {weather['temperatureC']}°, {weather['summary']}")