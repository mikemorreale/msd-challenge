from numpy import argsort, lexsort, zeros

# store data from the text files into dictionaries
print("storing data in dictionaries")
with open("../data/kaggle_users.txt", "r") as file:
    users = {}
    index = 1
    for line in file:
        user_id = line.strip()
        users[user_id] = index
        index += 1

with open("../data/kaggle_songs.txt", "r") as file:
    songs = {}
    for line in file:
        song_id, index = line.strip().split(" ")
        songs[song_id] = int(index) - 1

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

# create colisten dictionary
print("creating colisten matrix")
colisten = {}
for user in play_count:
    for song1 in play_count[user]:
        for song2 in play_count[user]:
            if song1 in colisten and song2 in colisten[song1]:
                colisten[song1][song2] += 1
            elif song1 not in colisten:
                colisten[song1] = {song2 : 1}
            elif song2 not in colisten[song1]:
                colisten[song1][song2] = 1

# store the diagonal elements of the colisten matrix into an array and sort it
print("creating array storing colisten diagonal and sorted colisten diagonal")
colisten_diagonal = zeros(len(songs)).astype("int32")
for song1 in colisten:
    for song2, _ in colisten[song1].items():
        if song1 == song2:
            colisten_diagonal[song1] += colisten[song1][song2]
sorted_diagonal = argsort(-colisten_diagonal[:500])

# output the solution and write it to a file
write_counter = 1
buffer = ""
print("outputting solution")
with open("../results/solution.txt", "w") as file:
    for user in play_count:        
        # create list for songs heard by the user and dictionary for play counts
        song_list = [user_song for user_song in play_count[user].keys()]
        count_dict = {song:counts for song,counts in play_count[user].items()}
        
        weighted_row_sums = zeros(len(songs)).astype("int32")
        for song in song_list:
            for row_song, colisten_val in colisten[song].items():
                weighted_row_sums[row_song] += colisten_val * count_dict[song]
        nonzero_weighted_row_sums = weighted_row_sums.nonzero()[0]
        
        # reverse sort by the weighted row sums followed by the colisten diagonal elements
        recommended_songs = lexsort((-colisten_diagonal[nonzero_weighted_row_sums], -weighted_row_sums[nonzero_weighted_row_sums]))
        recommendation_indices = nonzero_weighted_row_sums[recommended_songs]
        
        # recommend more songs if there are not enough already recommended
        guess_index = 0
        guess = 500 * [0]
        for recommendation_index in recommendation_indices:
            if guess_index < 500 and recommendation_index not in song_list:
                guess[guess_index] += recommendation_index + 1
                guess_index += 1
        
        for song in sorted_diagonal:
            if guess_index < 500 and song not in guess:
                guess[guess_index] = song + 1
                guess_index += 1
            elif guess_index == 500:
                break
        solution_string = " ".join(map(str, guess)) + "\n"
        
        # write solution to results file
        if write_counter % 1 == 0:
            file.write(solution_string)
        write_counter += 1

print("finished")
