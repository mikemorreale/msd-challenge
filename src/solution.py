from scipy import sparse
import numpy

print("storing data in dictionaries")
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

print("creating colisten matrix")
colisten = sparse.lil_matrix((len(songs), len(songs)))
for user in play_count:
    for song1 in play_count[user]:
        for song2 in play_count[user]:
            colisten[song1 - 1, song2 - 1] += 1

print("outputting solution")
with open("../results/solution.txt", "w") as out:
        songs_list = []
        counts_list = []
    
        colisten_diagonal = colisten.diagonal()
        sorted_diagonal = numpy.argsort(-colisten_diagonal)[:500]
    
        for user in play_count:
            for user_songs, counts in play_count[user].items():            
                songs_list.append(user_songs)
                counts_list.append(counts)
        
            counts_array = numpy.array(counts_list)[numpy.newaxis, :]
            user_songs_matrix = colisten[numpy.array(songs_list) - 1,:]
            sort_reference =  counts_array * user_songs_matrix
            
            nonzero_sort_reference = sort_reference.nonzero()[1]
            srt = numpy.lexsort((-colisten_diagonal[nonzero_sort_reference], -sort_reference[0,nonzero_sort_reference]))
            sorted_songs = nonzero_sort_reference[srt]
            
            guess = []
            for song in sorted_songs:
                if song + 1 in songs_list: continue
                guess.append(str(song + 1))
                if len(guess) == 500: break
                else:
                    for song in sorted_diagonal:
                        if song + 1 in songs_list or song + 1 in sorted_songs: continue
                        guess.append(str(song + 1))
                        if len(guess) == 500: break
                        out.write(' '.join(guess) + '\n')
                        
print("finished")
