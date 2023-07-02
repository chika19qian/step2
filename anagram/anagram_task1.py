#sort dictionary
new_dictionary = []
with open('words.txt','r') as f:
    wordlist = f.read().splitlines()

for word in wordlist:
    original = word
    changed = ''.join(sorted(word))
    new_dictionary.append((changed,original))

new_dictionary = sorted(new_dictionary, key = lambda x:x[0])


#find anagram
def find_anagram(random_word):
    sorted_random_word = ''.join(sorted(random_word))

    #binary-search
    left = 0
    right = len(new_dictionary)-1
    while left <= right:
        mid = (left+right)//2
        if sorted_random_word == new_dictionary[right][0]:
            mid = right
            break
        elif sorted_random_word == new_dictionary[left][0]:
            mid = left
            break
        elif sorted_random_word < new_dictionary[mid][0]:
            right = mid - 1
        else:
            left = mid + 1
    sorted_dic = new_dictionary[mid][0]
    # can't find anagram
    if sorted_random_word != sorted_dic:
        return "can't find anagram"    
    # check if it has several anagrams
    anagrams = [new_dictionary[mid][1]]
    find_left = mid - 1
    find_right = mid + 1
    while new_dictionary[find_left][0] == sorted_dic:
        anagrams.append(new_dictionary[find_left][1])
        find_left -= 1
    while new_dictionary[find_right][0] == sorted_dic:
        anagrams.append(new_dictionary[find_right][1])
        find_right += 1

    return anagrams

# Test-case
#print(find_anagram("a"))
#print(find_anagram("cdaaemic"))
#print(find_anagram("cta"))
#print(find_anagram(""))
#print(find_anagram("djksnalfbi"))

