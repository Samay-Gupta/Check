api_key = 'AIzaSyD38jaYuksM41v34SIn1vOFSI7Kk75QRlw'

import googlemaps
from datetime import datetime


class Map:
    def __init__(self, api_key):
        self.map = googlemaps.Client(key=api_key)

    def html_cleaner(self, data):
        while "<" in data and ">" in data:
            ind1 = data.index("<")
            ind2 = data.index(">")
            if ind2 < ind1:
                data = data[:ind2] + data[ind2+1:]
            elif data[ind1+1:ind1+4].lower() == "div":
                data = data[:ind1] + ". " + data[ind2+1:]
            else:
                data = data[:ind1] + data[ind2+1:]
        for i in ("<", ">"):
            if i in data:
                ind = data.index[i]
                data = data[:ind] + data[ind+1:]
        return data

    def directions(self, to ,frm):
        now = datetime.now()
        directions_result = self.map.directions(frm, to,
                                             mode="transit",
                                             departure_time=now)
        directions = []

        for leg in directions_result[0]['legs']:
            startAddress = leg['start_address']
            print("Start Address:", startAddress)
            endAddress = leg['end_address']
            print("End Address:", endAddress)
            distance = leg['distance']['text']
            print("Distance:", distance)
            duration = leg['duration']['text']
            print("Duration:", duration)
            for step in leg['steps']:
                html_instructions = step['html_instructions']
                instr = step['distance']['text']
                instrtime = step['duration']['text']
                crd = step['start_location']
                crd = [crd['lat'], crd['lng']]
                instruct = self.html_cleaner(html_instructions + " " + instr + " " + instrtime)
                directions.append([crd, instruct])
                if 'steps' in step.keys():
                    
                    for stepp in step['steps']:
                        crd = stepp['start_location']
                        crd = [crd['lat'], crd['lng']]
                        instruct = self.html_cleaner(stepp['html_instructions'])
                        directions.append([crd, instruct])
                        print("\t", instruct)
            print()
        return directions

api_key = 'AIzaSyD38jaYuksM41v34SIn1vOFSI7Kk75QRlw'
mp = Map(api_key)
venue = (59.277245, 18.014883)
dr = mp.directions("generator stockholm", venue)
print(dr)

