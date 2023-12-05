import requests
from bs4 import BeautifulSoup
import re
import json

def get_station_data(name):
    # Ersetzen Sie 'test' durch den eingegebenen Namen
    url = f'https://www.invg.de/rt/showRealtimeCombined.action?locale=de&nameKey={name}'

    # GET-Anfrage senden
    response = requests.get(url)

    # Prüfen Sie, ob die Anfrage erfolgreich war (Statuscode 200)
    if response.status_code == 200:
        # HTML-Inhalt analysieren
        soup = BeautifulSoup(response.text, 'html.parser')

        # Das gewünschte HTML-Element finden
        station_element = soup.find('td', {'bgcolor': '#FBFBFB', 'align': 'left'})

        # Überprüfen, ob das Element gefunden wurde
        if station_element:
            # Den Namen und die Station extrahieren
            name = station_element.a.get_text(strip=True)
            station_url = station_element.a['href']

            # Extrahieren von station und sid aus der station_url
            station_parts = station_url.split('&')
            station = station_parts[0].split('=')[1]

            # Verwenden Sie ein reguläres Ausdrucksmuster, um die SID zu extrahieren
            sid_match = re.search(r'sid=(\d+)', station_url)
            sid = sid_match.group(1) if sid_match else None

            # Ergebnisse ausgeben
            #print(f'Name: {name}')
            #print(f'Station: {station}')
            #print(f'SID: {sid}')

            return station, sid
        else:
            #print('Keine Informationen gefunden.')

            return 'none', 'none'
    else:
        #print(f'Fehler beim Abrufen der Seite. Statuscode: {response.status_code}')
        return 'none', 'none'

def get_timetable(st, sid):
    url = f'https://www.invg.de/rt/getRealtimeData.action?stopPoint=1&station={st}&sid={sid}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
def visualize(zdata):


        data = json.loads(zdata)

        # Überprüfen, ob Daten vorhanden sind
        if "departures" not in data:
            print("Keine Abfahrtsdaten gefunden.")
            return

        # Spaltenüberschriften
        print("{:<6} {:<20} {:<5} {:<15}".format("Linie", "Ziel", "Zeit", "Richtung"))
        print("="*50)  # Trennlinie

        # Daten durchgehen und ausgeben
        for departure in data["departures"]:
            linie = departure["route"]
            ziel = departure["destination"]
            zeit = departure["strTime"]
            richtung = "Stadtauswärts (H)" if departure["direction"] == "H" else "Stadteinwärts (R)"

            print("{:<6} {:<20} {:<5} {:<15}".format(linie, ziel, zeit, richtung))

def get_timtable_by_name(name):
    station, sid = get_station_data(name)
    zeitdata = get_timetable(station, sid)
    return zeitdata

if __name__ == '__main__':
    # Benutzereingabe für den Namen
    input_name = input('Geben Sie einen Stationsnamen ein: ')

    # Funktion aufrufen
    station, sid = get_station_data(input_name)
    zeitdata = get_timetable(station, sid)
    visualize(zeitdata)