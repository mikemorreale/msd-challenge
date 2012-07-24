from multiprocessing import Process
import itertools 

# Divide the train triplet file into 4 pieces so that it can be analyzed to produce the song colisten by 4 Python processes 
#print("dividing train triplets")
#line_index = 0       
#with open("../data/train_triplets.txt")as file:
#    for line in file:
#        line_index += 1
#        
#line_threshold = int(line_index / 4)
#line_index = 1
#with open("../data/train_triplets.txt", "r") as read_file:
#    for i in range(1,5):
#        print(i)
#        with open("../data/train_triplets_divided"+str(i)+".txt", "w") as write_file:
#            for line in read_file:
#                line_index += 1
#                if line_index % line_threshold == 0 :
#                    line_index = 0
#                    break
#                write_file.write(line)  

def main():                
    # Creating dictionary mapping song id to index
    print("Creating songs dictionary")
    with open("../data/kaggle_songs.txt", "r") as file:
        songs = {}
        for line in file:
            song_id, index = line.strip().split(" ")
            songs[song_id] = int(index) - 1
            
    p1 = Process(target=create_song_colisten, args= ("../data/train_triplets_divided1.txt", "../data/song_colsiten1.txt", songs))
    p2 = Process(target=create_song_colisten, args= ("../data/train_triplets_divided2.txt", "../data/song_colsiten2.txt", songs))
    p3 = Process(target=create_song_colisten, args= ("../data/train_triplets_divided3.txt", "../data/song_colsiten3.txt", songs))
    p4 = Process(target=create_song_colisten, args= ("../data/train_triplets_divided4.txt", "../data/song_colsiten4.txt", songs))
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()
        
        
def create_song_colisten(read_file, write_file, songs):        
    # Creating the song colisten and writing to file
    print("Create Song colisten")
    print(write_file)
    prev_user = ""
    index = 0
    user_songs = []
    with open(read_file, "r") as read_file:
        with open(write_file, "w") as write_file:
            for line in read_file:
                user, song, _ = line.strip().split("\t")
                if prev_user != user:
                    index += 1
                    print(index)
                    prev_user = user
                    if user_songs != []:
                        permutation_tuples = list(itertools.permutations(user_songs, 2))
                        for song_id in user_songs:
                            permutation_tuples.append(str(song_id)+","+str(song_id))
                        for permutation_tuple in permutation_tuples:
                            write_file.write(str(permutation_tuple) + "\n")
                    user_songs = []
                else:
                    user_songs.append(songs[song])           

if __name__ == "__main__":
    main()