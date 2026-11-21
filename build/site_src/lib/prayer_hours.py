"""Working-hours window for the contact card: from Fajr to Asr in Dhaka, recalculated every day.
Method: University of Islamic Sciences, Karachi (Fajr = sun 18 deg below horizon), Asr = Hanafi
(shadow factor 2) - the convention used in Bangladesh. Same maths will be ported to JS for the site."""
import math
from datetime import date, datetime, timedelta, timezone

LAT, LON, TZ = 23.8103, 90.4125, 6.0   # Dhaka


def _sun(jd):
    d = jd - 2451545.0
    g = math.radians((357.529 + 0.98560028 * d) % 360)
    q = (280.459 + 0.98564736 * d) % 360
    L = math.radians((q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360)
    e = math.radians(23.439 - 0.00000036 * d)
    ra = math.degrees(math.atan2(math.cos(e) * math.sin(L), math.cos(L))) / 15
    decl = math.asin(math.sin(e) * math.sin(L))
    eqt = q / 15 - (ra % 24)
    eqt = (eqt + 12) % 24 - 12
    return decl, eqt


def _jd(dt):
    y, m, d = dt.year, dt.month, dt.day
    if m <= 2:
        y -= 1; m += 12
    A = y // 100; B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5


def times(day: date):
    jd = _jd(day) - LON / 360
    decl, eqt = _sun(jd + 0.5)
    noon = 12 - LON / 15 - eqt + TZ
    lat = math.radians(LAT)

    def hour_angle(alt_deg):
        a = math.radians(alt_deg)
        return math.degrees(math.acos((math.sin(a) - math.sin(lat) * math.sin(decl)) / (math.cos(lat) * math.cos(decl)))) / 15

    fajr = noon - hour_angle(-18.0)
    sunrise = noon - hour_angle(-0.833)
    asr_alt = math.degrees(math.atan(1 / (2 + math.tan(abs(lat - decl)))))   # Hanafi factor 2
    asr = noon + hour_angle(asr_alt)
    maghrib = noon + hour_angle(-0.833)
    fmt = lambda h: f"{int(h):02d}:{int(round((h % 1) * 60)) % 60:02d}"
    return {"fajr": fmt(fajr), "sunrise": fmt(sunrise), "dhuhr": fmt(noon), "asr": fmt(asr), "maghrib": fmt(maghrib)}


if __name__ == "__main__":
    for dd in [date(2026, 11, 14), date(2026, 6, 21), date(2026, 12, 21)]:
        print(dd, times(dd))
