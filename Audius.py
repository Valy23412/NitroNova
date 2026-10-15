def run_search():
    SearchWord = SearchBar.get()  ### Get what the user typed into the search bar ###
    url = "https://api.audius.co/v1/tracks/search?query=" + SearchWord + "&app_name=NitroNova"
    Reply = requests.get(url)  ### Ask Audius for the data ###
    Data = Reply.json()  ### Turn the reply into Python data ###
    AllSongs = Data["data"]

    for SingleSong in AllSongs:
        Title = SingleSong["title"]
        Artist = SingleSong["user"]["name"]
        print(Title, "by", Artist)