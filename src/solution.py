import math
from multiprocessing import Process

def generate_solution(start_index, end_index, file, play_count, song_colisten, sorted_diagonal):
    with open(file, "w") as write_file:
        for user in range(start_index, end_index + 1):
            user_songs = sorted(play_count[user], key=play_count[user].get, reverse=True)
            user_play_counts = sorted(play_count[user].values(), reverse=True)
            
            user_songs_total = 0
            for count in play_count[user].values():
                user_songs_total += count
            
            user_rankings = []
            for song in play_count[user]:
                user_rankings.append(math.floor(play_count[user][song] / user_songs_total * 500))
            user_rankings.sort(reverse=True)
            for i in range(500 - sum(user_rankings)):
                user_rankings[i % len(user_rankings)] += 1
            
            songs_ignored = list(user_songs)
            colisten_row = {}
            
            count = 0
            index = 0
            while index < 500:
                if count == len(user_songs):
                    break
                count = 0
                
                for i in range(len(user_songs)):                
                    colisten_row = dict(song_colisten[user_songs[i]])
                    for song in songs_ignored:
                        if song in colisten_row:
                            del colisten_row[song]
                    
                    interleaving_index = 0
                    while interleaving_index < user_play_counts[i] and index < 500:
                        if colisten_row == {}:
                            count += 1
                            break
                        
                        recommendation = max(colisten_row, key=colisten_row.get)
                        songs_ignored.append(recommendation)
                        write_file.write(str(recommendation) + " ")
                        del colisten_row[recommendation]
                        index += 1
                        interleaving_index += 1
            
            for song in sorted_diagonal:
                if index == 500:
                    break
                elif song not in songs_ignored:
                    write_file.write(str(song) + " ")
                    index += 1
            
            write_file.write("\n")

def main():
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
    
    print("generating output for each user")
    p1 = Process(target=generate_solution, args=(1, 27500, "../results/solution1.txt", play_count, song_colisten, sorted_diagonal))
    p2 = Process(target=generate_solution, args=(27501, 55000, "../results/solution2.txt", play_count, song_colisten, sorted_diagonal))
    p3 = Process(target=generate_solution, args=(55001, 82500, "../results/solution3.txt", play_count, song_colisten, sorted_diagonal))
    p4 = Process(target=generate_solution, args=(83501, 110000, "../results/solution4.txt", play_count, song_colisten, sorted_diagonal))
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    print("finished")
    
if __name__ == "__main__":
    main()
