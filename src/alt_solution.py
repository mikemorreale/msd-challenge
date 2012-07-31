import copy, math

print("storing data in dictionaries")
with open("../data/kaggle_users.txt", "r") as file:
    users = {}
    index = 0
    for line in file:
        user_id = line.strip()
        index += 1
        users[user_id] = index

with open("../data/kaggle_songs.txt", "r") as file:
    songs = {}
    for line in file:
        song_id, index = line.strip().split(" ")
        songs[song_id] = int(index)

print("creating play_count")
play_count = {}
with open("../data/kaggle_visible_evaluation_triplets.txt", "r") as file:
    for line in file:
        user_id, song_id, count = line.strip().split("\t")
        if users[user_id] in play_count:
            play_count[users[user_id]][songs[song_id]] = int(count)
        else:
            play_count[users[user_id]] = {songs[song_id] : int(count)}

print("creating song_colisten")
song_colisten = {}
for user in play_count:
    for song1 in play_count[user]:
        for song2 in play_count[user]:
            if song1 in song_colisten and song2 in song_colisten[song1]:
                song_colisten[song1][song2] += 1
            elif song1 not in song_colisten:
                song_colisten[song1] = {song2 : 1}
            elif song2 not in song_colisten[song1]:
                song_colisten[song1][song2] = 1

print("creating sorted_diagonal")
sorted_diagonal = {}
for song1 in song_colisten:
    for song2 in song_colisten[song1].keys():
        if song1 == song2:
            sorted_diagonal[song1] = -song_colisten[song1][song2]
sorted_diagonal = sorted(sorted_diagonal, key=sorted_diagonal.get)

print("Generating solution for each user")
