from multiprocessing import Process
import itertools

def make_train_triplets():    
    # Creating song dictionary
    print("Creating songs dictionary")
    with open("../data/kaggle_songs.txt", "r") as file:
        songs = {}
        for line in file:
            song_id, index = line.strip().split(" ")
            songs[song_id] = int(index) - 1
            
    user_index = 0
    with open("../data/train_triplets.txt", "r") as file:
        for i in range(1,5):
            with open("../data/train_triplets"+str(i)+".txt", "w") as write_file:
                prev_user = ""
                for line in file:
                    user, song_id, play_count = line.strip().split("\t")
                    if user != prev_user:
                        prev_user = user
                        user_index += 1
                    write_file.write(str(user_index) + "\t" + str(songs[song_id]) +"\t" + str(play_count) + "\n")
                    if user_index == int(1019318/4) * i:
                        break  

def create_song_colsiten(i):
    print("Creating Song Colisten "+ str(i))
    prev_user = 1
    user_songs = []
    with open("../data/train_triplets"+str(i)+".txt", "r") as read_file:
        with open("/data/song_colisten"+str(i)+".txt", "w") as write_file:
            for line in read_file:
                user,song, _ = line.strip().split("\t")
                if prev_user != user and user_songs != []:
                    song_permutations = list(itertools.permutations(user_songs))
                    print(song_permutations)
                    for j in user_songs:
                        song_permutations.append(str(j)+" "+str(j))
                    
                    for song_pair in song_permutations:
                        write_file.write(str(song_pair) + "\n")
                    prev_user = user
                    user_songs = []
                    user_songs.append(song)
                else:
                    user_songs.append(song)
def main():
    print("Starting Song Colisten Processes")
    p1 = Process(target=create_song_colsiten, args= ("1"))
    p2 = Process(target=create_song_colsiten, args= ("2"))
    p3 = Process(target=create_song_colsiten, args= ("3"))
    p4 = Process(target=create_song_colsiten, args= ("4"))
    
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