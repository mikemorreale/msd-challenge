import itertools

with open("../data/kaggle_songs.txt", "r") as file:
    songs = {}
    for line in file:
        song_id, index = line.strip().split(" ")
        songs[song_id] = int(index)

print("Starting Song Colisten Processes")
prev_user = ""
user_index = 0
user_songs = []
with open("../data/train_triplets.txt", "r") as read_file:
    with open("../data/song_colisten.txt", "w") as write_file:
        for line in read_file:
            user,song, _ = line.strip().split("\t")
            if prev_user != user and user_songs != []:
                user_index += 1
                if user_index % 1000 == 0:
                    print(user_index)
                song_permutations = itertools.permutations(user_songs, 2)
                for permutation in song_permutations:
                    write_file.write(str(permutation) + "\n")
                for j in user_songs:
                    write_file.write("("+str(j)+" "+str(j)+")\n" )
                prev_user = user
                user_songs = []
                del song_permutations
                user_songs.append(songs[song])
            else:
                user_songs.append(songs[song])