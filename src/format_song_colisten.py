# Formatting song colisten file 
print("Formatting song colisten file")
index = 0
with open("../data/song_colisten.txt", "r") as read_file:
    with open("../data/formatted_song_colsiten.txt", "w") as write_file:
        while True:
            line_char = read_file.read(1)
            if not line_char:
                break
            else:
                if line_char == ')':
                    write_file.write("\n")
                    index += 1
                elif line_char == '(' or line_char == ',' or line_char == ']' or line_char == '[':
                    continue
                else:
                    write_file.write(line_char)
print("end")
    