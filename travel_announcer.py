#!/usr/bin/env python
# Travel guidence announcer.
from gtts import gTTS
import os
import requests
from subprocess import PIPE, Popen
import xml.etree.ElementTree as ET
import pickle

def play_mp3(path):
    Popen(['mpg123', '-q', path], stdout=PIPE, stderr=PIPE).wait()

r49b_southbound ='http://www.ctabustracker.com/bustime/eta/eta.jsp?route=49B&direction=Southbound&stop=Western%20%26%20Albion&id=1702&showAllBusses=on'

route_information = 'http://www.ctabustracker.com/bustime/map/getStopsForRouteDirection.jsp?route=49B&direction=%s'

stop_albion_south = 'http://www.ctabustracker.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=1702'
stop_western_north = 'http://www.ctabustracker.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=1662'

routes = [stop_albion_south, stop_western_north]

def get_schedule(url, offline=False):
    stop_number = url.split('=')[-1]
    cache_file = '/tmp/%s.ctatracker.dat' % stop_number
    if offline:
        return open(cache_file).read()
    tracker = requests.get(stop_albion_south)
    print "saving", cache_file
    f = open(cache_file, 'wb')
    f.write(tracker.text)
    f.close()
    return tracker.text

def play_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("good.mp3")
    #os.system("mpg123 good.mp3")
    play_mp3('good.mp3')
    
def get_prediction(stop_number):
    route_xml = requests.get("http://www.ctabustracker.com"
                 "/bustime/eta/getStopPredictionsETA.jsp"
                 "?route=all&stop=%s" % stop_number).text
    root = ET.fromstring(route_xml)
    
    
def get_routes(offline=False):
    if offline:
        return pickle.load(open('/tmp/bustracker.routes.dat','rb'))
    routes = {}
    route_xml = requests.get(route_information % 'Southbound').text
    root = ET.fromstring(route_xml)
    for c in root.iter('stop'):
        route = dict(
            direction='Southbound',
            id=int(c.find('id').text),
            name='Southbound ' + c.find('name').text
            )
        routes[route['name']] = route
            
    route_xml = requests.get(route_information % 'Northbound').text
    root = ET.fromstring(route_xml)
    for c in root.iter('stop'):
        route = dict(
            direction='Northbound',
            id=int(c.find('id').text),
            name='Northbound ' + c.find('name').text
            )
        routes[route['name']] = route
    f = open('/tmp/bustracker.routes.dat','wb')
    pickle.dump(routes,f)
    
    return routes

    
def poll(routes):

    while True:
        for route in routes:
            print "accessing route {route_name}".foramt(**route) 
    time.sleep(5)
    
def load_routes(config):
    routes = get_routes(offline)
    petes_routes = {'northbound':routes["Northbound Western Brown Line Station"],
                    'southbound': routes["Southbound Western & Albion"]}
    routes = {'pete': petes_routes}
    return routes
    

if __name__ == '__main__':

    
    #print routes["Southbound Western & Albion"]
    #for i in routes.keys(): print i
   
    offline = False
    routes = load_routes(offline)
    print routes['pete']['northbound']['id']
    print get_schedule(route_information % routes['pete']['northbound']['id']).replace('\n','')
    print get_schedule(route_information % routes['pete']['southbound']['id']).replace('\n', '')
    #print routes
    #exit()
    southbound = get_schedule(stop_albion_south, offline)
    northbound = get_schedule(stop_western_north, offline)
    root = ET.fromstring(southbound)
    print root
    #for child in root.iter('pt'):
    for child in root:
        this = dict( minutes_to_stop = child.find('pt').text,
            unit = child.find('pu').text,
            bus_number = child.find('rd').text,
            next_time = child.find('nextbusonroutetime').text,
            from_d = child.find('fd').text )
        text =  "The next southbound {bus_number} bus is due in {minutes_to_stop} {unit}".format( **this )
        print text
        play_text(text)
        break
        #print "minutes ", child['pt'].text
        #for item in child:
        #    print item.tag, item.text
    
    
        
        
    
    #play_text('Good morning. Your bus will arrive in %s minutes' % 3)