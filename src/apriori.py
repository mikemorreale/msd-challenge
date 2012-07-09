# Apriori large itemset generator
def apriori_gen(prev_large_itemsets):
    candidate_large_itemsets = []
    # Join part of the apriori gen
    for i in range(len(prev_large_itemsets) - 1 ):
        new_elements = set(prev_large_itemsets) - set(prev_large_itemsets[i]) & set(prev_large_itemsets[i+1])
        print(new_elements)
        if len(new_elements) == 2:
            if new_elements[0] not in prev_large_itemsets[i] and new_elements[0] > prev_large_itemsets[i][len(prev_large_itemsets)-1]:
                new_candidate = prev_large_itemsets[i]
                new_candidate.append(new_elements[0])
                candidate_large_itemsets.append(new_candidate)
                new_candidate = prev_large_itemsets[i+1]
                new_candidate.append(new_elements[1]) 
                candidate_large_itemsets.append(new_candidate)
            elif new_elements[0] not in prev_large_itemsets[i+1] and new_elements[0] > prev_large_itemsets[i][len(prev_large_itemsets)-1]:
                new_candidate = prev_large_itemsets[i+1]
                new_candidate.append(new_elements[0])
                candidate_large_itemsets.append(new_candidate)
                new_candidate = prev_large_itemsets[i]
                new_candidate.append(new_elements[1])
                candidate_large_itemsets.append(new_candidate)
    candidate_large_itemsets = prune(prev_large_itemsets,candidate_large_itemsets)
    return candidate_large_itemsets
    
# prune candiates if their subsets are not large itemsets    
def prune(prev_large_itemset,candidate_song_set):
    for new_itemset in candidate_song_set:
        for i in range(len(new_itemset)):
            large_items_subset = new_itemset
            large_items_subset.remove(new_itemset[i])
            if large_items_subset not in prev_large_itemset:
                candidate_song_set.remove(new_itemset)
                
    return candidate_song_set

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

# Variables used throughout the apriori algorithm
large_itemset_support = {}
#large_itemsets = []
support_threshold = 15
confidence_threshold = 15

# Apply apriori algorithm to predict similar songs to songs 
print("applying apriori to predict similar songs")

# Pass one of apriori algorithm to generate and store size-1 large itemsets which will be used for subsequent larger itemset generation
print("Pass 1 of Apriori")
for song in range (1,len(songs)):
    song_support = 0
    temp_itemset = [song]
    for user in play_count:
        if song in play_count[user]:
            song_support += 1
            print(song, song_support)
    if song_support > support_threshold:
        print(song)
        large_itemset_support[song] = song_support
        
# Pass 2 to K to generate all large itemsets using smaller itemsets as seeds
print("Pass 2 to K of apriori")
new_itemsets_added = True
candidate_itemsets = list(large_itemset_support.keys())

# while new large itemsets are being generated continue
while new_itemsets_added:
    # Generate large itemsets of size k by joining and pruning itemsets of size k-1
    candidate_itemsets = apriori_gen(candidate_itemsets) 
    new_itemsets_added = False
    for candidate in candidate_itemsets:
        candidate_support = 0
        song_to_list = []
        # Calculate support of the new large itemset genrated by apriori_gen
        for song in candidate:
            song_to_list = song
            candidate_support += large_itemset_support[song_to_list]
        # Add only those itemsets that have support greater than threashold
        if candidate_support > support_threshold:
            large_itemset_support[candidate] = candidate_support
            new_itemsets_added = True
            
print(large_itemset_support)
