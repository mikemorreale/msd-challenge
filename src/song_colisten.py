import itertools

# Creating dictionary mapping song id to index
with open("../data/kaggle_songs.txt", "r") as file:
    songs = {}
    for line in file:
        song_id, index = line.strip().split(" ")
        songs[song_id] = int(index) - 1

# Creating the song colisten and writing to file
prev_user = ""
index = 0
user_songs = []
with open("../data/train_triplets.txt", "r") as read_file:
    with open("../data/song_colisten.txt", "w") as write_file:
        for line in read_file:
            user, song, play_count = line.strip().split("\t")
            if prev_user != user:
                prev_user = user
                if user_songs != []:
                    permutation_tuples = list(itertools.permutations(user_songs, 2))
                    for song_id in user_songs:
                        permutation_tuples.append(str(song_id)+","+str(song_id))
                    write_file.write(str(permutation_tuples))
                user_songs = []
                index += 1
            else:
                user_songs.append(songs[song]) 
                