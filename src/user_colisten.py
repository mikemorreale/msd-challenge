from numpy import argsort, lexsort, zeros
from multiprocessing import Process

def create_user_colisten(range_start, range_end, outfile, play_count):
    user_colisten = {}
    print(str(outfile))
    with open(outfile, 'w')as file:
        for user1 in range(range_start, range_end):       
            max_song_match = -1
            for user2 in range(user1 + 1, range_end):
                has_colisten = set(play_count[user1].keys()) & set(play_count[user2].keys())
                if has_colisten:
                    song_list_length = len(has_colisten)
                    if song_list_length > max_song_match:
                        user_colisten[user1] = set(play_count[user1].keys()) or set(play_count[user2].keys())
                        max_song_match = song_list_length
            if user1 in user_colisten:
                file.write(str(user1) + ":" + str(user_colisten[user1]) + "\n")

def main():
    
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
       
    # Create user colisten dictionary using threads
    print("thread function creating user colisten dictionary")
    p1 = Process(target=create_user_colisten, args=(1, 27500, "../results/user_colisten1.txt", play_count))
    p2 = Process(target=create_user_colisten, args=(27501, 55000, "../results/user_colisten2.txt", play_count))
    p3 = Process(target=create_user_colisten, args=(55001, 82500, "../results/user_colisten3.txt", play_count))
    p4 = Process(target=create_user_colisten, args=(82501, 110001, "../results/user_colisten4.txt", play_count))
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()

if __name__ == "__main__":
    main()

