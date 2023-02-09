from weather_data import weather_codes

def is_it_raining():
    s = weather_codes()[1].values()
    s = sorted(s)
    if s[-1] >= 61:
        return "Bring an umbrella ☂,\nthere is possibility of rain today.⛈"
    else:
        return "I think it's not going to rain today. 🌤"