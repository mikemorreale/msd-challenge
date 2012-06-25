from scipy import sparse

with open("../data/kaggle_users.txt", "r") as file:
    users = {}
    index = 0
    for line in file:
        user_id = line.strip()
        users[user_id] = index
        index += 1

with open("../data/kaggle_songs.txt", "r") as file:
    songs = {}
    for line in file:
        song_id, index = line.strip().split(" ")
        songs[song_id] = int(index)

with open("../data/taste_profile_song_to_tracks.txt", "r") as file:
    tracks = {}
    for line in file:
        temp = line.strip().split("\t")
        song_id = temp[0]
        track = []
        track = temp[1:]
        tracks[songs[song_id]] = track

with open("../data/kaggle_visible_evaluation_triplets.txt", "r") as file:
    play_count = {}
    for line in file:
        user_id, song_id, count = line.strip().split("\t")
        if users[user_id] in play_count:
            play_count[users[user_id]][songs[song_id]] = int(count)
        else:
            play_count[users[user_id]] = {songs[song_id] : int(count)}

colisten = sparse.lil_matrix((len(songs), len(songs)))
for user in play_count:
    song_indices = []
    for key in play_count[user].keys():
        song_indices.append(key)
    for i in range(len(song_indices)):
        for j in range(i, len(song_indices)):
            colisten[song_indices[i] - 1, song_indices[j] - 1] += 1
            colisten[song_indices[j] - 1, song_indices[i] - 1] += 1