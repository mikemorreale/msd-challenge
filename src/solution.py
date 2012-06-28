from numpy import argsort, lexsort, zeros
from scipy import sparse
import io

# store data from the text files into dictionaries
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

with open("../data/triplets_subset.txt", "r") as file:
    play_count = {}
    for line in file:
        user_id, song_id, count = line.strip().split("\t")
        if users[user_id] in play_count:
            play_count[users[user_id]][songs[song_id]] = int(count)
        else:
            play_count[users[user_id]] = {songs[song_id] : int(count)}

# create colisten matrix
print("creating colisten matrix")
colisten = sparse.lil_matrix((len(songs), len(songs)))
for user in play_count:
    for song1 in play_count[user]:
        for song2 in play_count[user]:
            colisten[song1 - 1, song2 - 1] += 1

# convert colisten matrix to compressed sparse row format
print("converting colisten matrix to csr format")
colisten = colisten.tocsr()

# store the diagonal elements of the colisten matrix into an array and sort it
print("creating array storing colisten diagonal")
colisten_diagonal = colisten.diagonal().astype("int32")
sorted_diagonal = argsort(-colisten_diagonal[:500])

# output the solution and write it to a file
print("outputting solution")
with open("../results/solution.txt", "w") as file:
    for user in play_count:
        file_str = io.StringIO()
        
        # create lists for songs heard by the user and their play counts
        song_list = [user_song for user_song in play_count[user].keys()]
        count_list = [count for count in play_count[user].values()]
        
        # create a list of rows as arrays from the colisten matrix for every song the user heard
        song_rows = [colisten[song - 1, :].toarray()[0] for song in song_list]
        
        # create weighted scores by multiplying the row corresponding to a song by the play count of that song
        weighted_row_sums = zeros(colisten.shape[0]).astype("int32")
        index = 0
        for row in song_rows:
            weighted_row_sums += row * count_list[index]
            index += 1
        nonzero_weighted_row_sums = weighted_row_sums.nonzero()[0]
        
        # reverse sort by the weighted row sums followed by the colisten diagonal elements
        recommended_songs = lexsort((-colisten_diagonal[nonzero_weighted_row_sums], -weighted_row_sums[nonzero_weighted_row_sums])) # could add [nonzero_weighted_row_sums] for nonzero values
        recommendation_indices = nonzero_weighted_row_sums[recommended_songs] + 1
        
        # recommend more songs if there are not enough already recommended
        solution = list(recommendation_indices)
        for recommendation_index in solution:
            if recommendation_index in song_list:
                solution.remove(recommendation_index)
        solution_string = " ".join(map(str, solution))
        
        count = len(solution)
        if count < 500:
            file_str.write(solution_string)
            for song in sorted_diagonal:
                if count == 500:
                    file_str.write("\n")
                    break
                elif song not in solution:
                    file_str.write(" " + str(song))
                    count += 1
        else:
            solution = solution[:500]
            file_str.write(" ".join(map(str, solution)) + "\n")
        
        # write solution to results file
        file.write(file_str.getvalue())

print("finished")
