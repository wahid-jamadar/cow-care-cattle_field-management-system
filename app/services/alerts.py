def get_alert_from_sample(temp, spo2, motion):
    alerts = []

    if temp > 39.5:
        alerts.append(("Fever detected", "High"))

    if spo2 < 90:
        alerts.append(("Low SpO₂ detected", "High"))

    if motion == "Low":
        alerts.append(("Low movement detected", "Medium"))

    return alerts