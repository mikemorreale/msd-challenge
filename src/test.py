import numpy
from scipy import sparse


colisten = sparse.lil_matrix((5, 5))
colisten[1, 1] += 3
colisten[1, 2] += 2
colisten[1, 3] += 2
colisten[1, 4] += 2
colisten[2, 1] += 2
colisten[2, 2] += 2
colisten[2, 3] += 2
colisten[2, 4] += 1
colisten[3, 1] += 2
colisten[3, 2] += 2
colisten[3, 3] += 3
colisten[4, 1] += 2
colisten[4, 2] += 1
colisten[4, 4] += 2
print("colisten\n", colisten, end="\n\n")

song_list = [2, 3, 5]
counts_list = [1, 1, 1]
print("numpy.array(counts_list)[numpy.newaxis, :]\n", numpy.array(counts_list)[numpy.newaxis, :], end="\n\n")
print("colisten[numpy.array(song_list) -1, :]\n", colisten[numpy.array(song_list) -1, :], end="\n\n")

sim = numpy.array(counts_list)[numpy.newaxis, :] * colisten[numpy.array(song_list) - 1, :]
print("sim\n", sim, end="\n\n")

simidxs = sim.nonzero()[1]
print("simidxs\n", simidxs, end="\n\n")

listens = colisten.diagonal()
print("listens\n", listens, end="\n\n")

print("-listens[simidxs]\n", -listens[simidxs], end="\n\n")
print("-sim[0, simidxs]\n", -sim[0, simidxs], end="\n\n")

srt = numpy.lexsort((-listens[simidxs], -sim[0, simidxs]))
print("srt\n", srt, end="\n\n")

rankidxs = simidxs[srt]
print("rankidxs\n", rankidxs)

#    songs_list = []
#    counts_list = []
#    
#    colisten_diagonal = colisten.diagonal()
#    sorted_diagonal = numpy.argsort(-colisten_diagonal)[:500]
#    
#    for user in play_count:
#        for user_songs, counts in play_count[user].items():            
#            songs_list.append(user_songs)
#            counts_list.append(counts)
#        
#        counts_array = numpy.array(counts_list)[numpy.newaxis, :]
#        user_songs_matrix = colisten[numpy.array(songs_list) - 1,:]
#        sort_reference =  counts_array * user_songs_matrix
#        
#        nonzero_sort_reference = sort_reference.nonzero()[1]
#        srt = numpy.lexsort((-colisten_diagonal[nonzero_sort_reference], -sort_reference[0,nonzero_sort_reference]))
#        sorted_songs = nonzero_sort_reference[srt]
#        
#        guess = []
#        for song in sorted_songs:
#            if song + 1 in songs_list: continue
#            guess.append(str(song + 1))
#            if len(guess) == 500: break
#            else:
#                for song in sorted_diagonal:
#                    if song + 1 in songs_list or song + 1 in sorted_songs: continue
#                    guess.append(str(song + 1))
#                    if len(guess) == 500: break
#                    out.write(' '.join(guess) + '\n')