#
# These two codes will take in a Json file, and using the API's will provide data
# The first code will use the Google Maps API to tell the distances between given cities, and also show the time it gets to get from one city to another
# The second code will use the Itunes API to compare artists, to see which was more productive by comparing their charts
#

import requests
import string
import json

"""
Examples you might want to run during class:

Web scraping, the basic command (Thanks, Prof. Medero!)

#
# basic use of requests:
#
url = "https://www.cs.hmc.edu/~dodds/demo.html"  # try it + source
result = requests.get(url)
text = result.text   # provides the source as a large string...

#
# try it for another site...
#

# 
# let's demo the weather example...
# 
url = 'http://api.wunderground.com/api/49e4f67f30adb299/geoloookup/conditions/q/Us/Ca/Claremont.json' # JSON!
       # try it + source
result = requests.get(url)
data = result.json()      # this creates a data structure from the json file!
# What type will it be?
# familiarity with dir and .keys() to access json data...

#
# let's try the Open Google Maps API -- also provides JSON-formatted data
#   See the webpage for the details and allowable use
#
# Try this one by hand - what are its parts?
# http://maps.googleapis.com/maps/api/distancematrix/json?origins=%22Claremont,%20CA%22&destinations=%22Seattle,%20WA%22&mode=%22walking%22
#
# Take a look at the result -- imagine the structure of that data... That's JSON! (Sketch?)
#
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 1- Google Maps API
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#
# 
#
def google_distances_api_scrape(filename_to_save="distances.json"):
    """ a short function that shows how  
        part of Google Maps' API can be used to 
        obtain and save a json file of distances data...
    """
    url="http://maps.googleapis.com/maps/api/distancematrix/json"

    city1="Claremont,CA| Pittsburgh, PA| Boston, MA"
    city2="San Francisco,CA| Seattle, WA|"
    my_mode="walking"

    inputs={"origins":city1,"destinations":city2,"mode":my_mode}

    result = requests.get(url,params=inputs)
    data = result.json()
    print("data is", data)

    # save this json data to file
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")
    # no need to return anything, since we're better off reading it from file!
    return


def google_distances_api_process(filename_to_read = "distances.json"):
    #process a file
    """ a function with examples of how to manipulate json data --
        here the data is from the file scraped and saved by 
        google_distances_api_starter()
    """
    f = open( filename_to_read, "r" )
    string_data = f.read()
    data = json.loads( string_data )
    print("data (not spiffified!) is\n\n", data, "\n")

    print("Accessing its components:\n")

    row0 = data['rows'][0]
    print("row0 is", row0, "\n")

    cell0 = row0['elements'][0]
    print("cell0 is", cell0, "\n")

    distance_as_string = cell0['distance']['text']
    print("distance_as_string is", distance_as_string, "\n")

    # here, we may want to continue operating on the whole json dictionary
    # so, we return it:
    return data

def multicity_distance_scrape( Origins, Dests, filename_to_save="multicity.json" ):
    """ This method will take a list of starting destinations, and finishing destinations
    and return the distances between them in multiplicity.json""" 
    
    url="http://maps.googleapis.com/maps/api/distancematrix/json"
    
    origin_string = ""
    dest_string = ""
    for x in range(len(Origins)):
        origin_string += Origins[x] + "|"
    origin_string = origin_string[:-1]
    for x in range(len(Dests)):
        dest_string += Dests[x] + "|"
    dest_string = dest_string[:-1]
    
    city1= origin_string
    city2= dest_string
    my_mode="walking"

    inputs={"origins":city1,"destinations":city2,"mode":my_mode}

    result = requests.get(url,params=inputs)
    data = result.json()
    print("data is", data)

    # save this json data to file
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")
    # no need to return anything, since we're better off reading it from file!
    return
    

#
# multicity_distance_process
#
def multicity_distance_process(filename_to_read = "multicity.json"):
    """ 
    This method returns the distance between each given place in the multicity.json file
    """
    f = open( filename_to_read, "r" )
    string_data = f.read()
    data = json.loads( string_data )

    #extra credit- getting the html page to look nice, and posted on github
    new_html_string = '<table>'
    for row in data["rows"]:
        L = row["elements"]
        new_html_string += '<tr>'
        for d in L:
            printer = (d["distance"]["text"])
            print(printer)
            new_html_string += '<td>' + str(printer) + '</td>'
        
        new_html_string += '</tr>'
    new_html_string += '</table>'
    return(new_html_string)

#
# a main function for problem 1 (the multicity distance problem)
#
def main_pr1():
    """ a top-level function for testing things! """
    # these were the cities from class:
    # Origins = ['Pittsburgh,PA','Boston,MA','Seattle,WA']  # starts
    # Dests = ['Claremont,CA','Atlanta,GA']         # goals
    #
    # Origins are rows...
    # Dests are columns...
    pass




# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 2a starter code
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#
#
#

def apple_api_id_scraper(artist_name, filename_to_save="appledata_id.json"):
    """ 
    Takes an artists name, and saves all of their information into a json filename_to_save
    Returns the artist's ID number
    """
    ### Use the search url to get an artist's itunes ID
    search_url = "https://itunes.apple.com/search"
    parameters = {"term":artist_name, "entity":"musicArtist","media":"music","limit":200}
    result = requests.get(search_url, params=parameters)
    data = result.json()

    # save to a file to examine it...
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")


    f = open( filename_to_save, "r" )
    string_data = f.read()
    data = json.loads( string_data )
    return(data["results"][0]["artistId"]) #artistId number


#
# 
#
def apple_api_full_scraper(artistid =136975, filename_to_save="appledata_full.json"):
    """ 
    Takes an artistid and grabs a full set of that artist's albums.
    """
    lookup_url = "https://itunes.apple.com/lookup"    
    parameters = {"entity":"album","id":artistid}    
    result = requests.get(lookup_url, params=parameters)
    data = result.json()

    # save to a file to examine it...
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")

    # we'll leave the processing to another function...
    return



#
#
#
def apple_api_full_process(filename_to_read="appledata_full.json"):
    """ example of extracting one (small) piece of information from 
        the appledata json file...
    """
    f = open( filename_to_read, "r" )
    string_data = f.read()
    data = json.loads( string_data )
    #print("data (not spiffified!) is\n\n", data, "\n")

    # for live investigation, here's the full data structure
    return data



#
#
#

def most_productive_scrape(artist1, artist2, fname1="artist1.json", fname2="artist2.json"):
    """
    Gets the ID numbers of the artists, and saves their information to Json files
    """
    #gets ID numbers
    id_num1 = apple_api_id_scraper(artist1)
    id_num2 = apple_api_id_scraper(artist2)
    apple_api_full_scraper(id_num1, fname1)
    apple_api_full_scraper(id_num2, fname2)

    #print("file artist1.json written")
    #print("file artist2.json written")
    return

#
#
#
def most_productive_process(fname1="artist1.json", fname2="artist2.json"):
    """
    gets the file inputs and outputs their name and number of albums, to ultimately see who is more
    productive
    """
    data_artist1 = apple_api_full_process(fname1)
    data_artist2 = apple_api_full_process(fname2)

    result_data1 = data_artist1['resultCount']
    artistname1 = data_artist1['results'][0]['artistName']

    result_data2 = data_artist2['resultCount']
    artistname2 = data_artist2['results'][0]['artistName']
    
    
    print("# of results for " + artistname1 + " == " + str(result_data1))
    print("# of results for " + artistname2 + " == " + str(result_data2))
    


#extra credit
def hasNumbers(givenString):
    return any(char.isdigit() for char in givenString)


def most_productive_num_process(fname1="artist1.json", fname2="artist2.json"):
    """
    gets the file inputs and outputs the artists name as well as number of albums that has a number in the title
    """
    data_artist1 = apple_api_full_process(fname1)
    data_artist2 = apple_api_full_process(fname2)

    result_data1 = 0
    for i in range(int(data_artist1["resultCount"])):
        if i != 0:
            if hasNumbers(data_artist1["results"][i]["collectionName"]) == True:
                result_data1 = result_data1 + 1

    result_data2 = 0
    for d in range(int(data_artist2["resultCount"])):
        if d != 0:
            if hasNumbers(data_artist2["results"][d]["collectionName"]) == True:
                result_data2 = result_data2 + 1
    
    artistname1 = data_artist1['results'][0]['artistName']
    artistname2 = data_artist2['results'][0]['artistName']
    
    
    print("# of results for " + artistname1 + " == " + str(result_data1))
    print("# of results for " + artistname2 + " == " + str(result_data2))



#
# main_pr2()  for testing problem 2's functions...
#
def main_pr2():
    """ a top-level function for testing things... """
    most_productive_scrape( "Katy Perry", "Steve Perry" )
    most_productive_process()  # uses default filenames!
    return

"""
Overview of progress on this problem - test cases you ran

For example: most_productive_scrape( "Taylor Swift", "Kanye West" ); most_productive_process()--> # of results for Taylor Swift == 36, # of results for Kanye West == 51

Regular-
Example 1: most_productive_scrape( "Drake", "Meek Mill" ); most_productive_process()--> # of results for Drake == 51, # of results for Meek Mill == 51
Example 2: most_productive_scrape( "Mariah Carey", "Nicki Minaj" ); most_productive_process()--> # of results for Mariah Carey == 51, # of results for Nicki Minaj == 51
Example 3: most_productive_scrape( "Katy Perry", "Taylor Swift" ); most_productive_process()--> # of results for Katy Perry == 32, # of results for Taylor Swift == 36

Extra Credit-
Example 1: most_productive_scrape( "Beyonce", "Adele" ); most_productive_num_process() --> # of results for Beyonce == 3, # of results for Adele == 4
Example 2: most_productive_scrape( "Taylor Swift", "Usher" ); most_productive_num_process() --> # of results for Taylor Swift == 4, # of results for Usher == 4
Example 3: most_productive_scrape( "U2", "the Beatles" ); most_productive_num_process() --> # of results for U2 == 5, # of results for the Beatles == 9
"""