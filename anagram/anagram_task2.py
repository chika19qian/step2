import itertools

#sort dictionary
def sort_dic():
    new_dictionary = []
    with open('words.txt','r') as f:
        wordlist = f.read().splitlines()

    for word in wordlist:
        original = word
        changed = ''.join(sorted(word))
        new_dictionary.append((changed,original))

    new_dictionary = sorted(new_dictionary, key = lambda x:x[0])
    return new_dictionary

#count dictionary
def count(w):
    dicti = {"original":w}
    score = 0
    for i in w:
        if i in ['j', 'k', 'q', 'x', 'z']:
            score += 4
        elif i in ['b', 'f', 'g', 'p', 'v', 'w', 'y']:
            score += 3
        elif i in ['c', 'd', 'l', 'm', 'u']:
            score += 2
        else:
            score += 1
        
        if i not in dicti:
            dicti[i] = 1
        else:
            dicti[i] += 1
    dicti['scores'] = score

    return dicti

def count_dic():
    new_dictionary = []
    with open('words.txt','r') as f:
        wordlist = f.read().splitlines()

    for w in wordlist:   
        new_dictionary.append(count(w))
    new_dictionary = sorted(new_dictionary, key=lambda x:x['scores'], reverse = True) 
    return new_dictionary


# binary_search for short words
def binary_search(sorted_random_word,new_dictionary):
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
        return  ""
    # check if it has several anagrams
    anagrams = [new_dictionary[mid][1]]
    find_left = mid - 1
    find_right = mid + 1
    while find_left > 0 and new_dictionary[find_left][0] == sorted_dic :
        anagrams.append(new_dictionary[find_left][1])
        find_left -= 1
    while find_right < len(new_dictionary)-1 and new_dictionary[find_right][0] == sorted_dic :
        anagrams.append(new_dictionary[find_right][1])
        find_right += 1

    return anagrams

#when word_lenth<13
def anagram_short(random_word,new_dictionary):
    result = []
    for i in range(1,len(random_word)+1): 
        w_com = itertools.combinations(random_word,i)
        for j in w_com:
            sorted_random_word = ''.join(sorted(j))
            result.append(binary_search(sorted_random_word,new_dictionary))
    result = list(itertools.chain.from_iterable(result))
    return max(result, key=len)

#when word_lenth>=13
def anagram_long(random_word,new_dictionary):
    counted_word = count(random_word)
    
    isanagram = False
    for di in new_dictionary:
        for key in di:
            if key == 'original' or key == 'scores':
                continue
            elif key not in list(counted_word.keys()) or di[key] > counted_word[key]:
                isanagram = False
                break
            else:
                isanagram = True
        if isanagram == True:
            result = di['original']
            break

    return result
           


# Test

#read test files
#test_file = "small.txt"
#test_file = "medium.txt"
test_file = "large.txt"
with open(test_file,'r') as f:
    random_word_list = f.read().splitlines()
answer = []

new_dictionary = count_dic()
for w in random_word_list:
    w = list(w)
    answer.append(anagram_long(w,new_dictionary))

with open('large_answer.txt', 'w') as f:
    print(*answer, sep='\n',file=f)


#if word_lenth < 13:
'''
new_dictionary = sort_dic()
for w in random_word_list:
    w = list(w)
    answer.append(anagram_short(w,new_dictionary))
'''
'''
#if word_lenth >= 13:
new_dictionary = count_dic()
for w in random_word_list:
    w = list(w)
    answer.append(anagram_long(w,new_dictionary))

with open('small_answer.txt', 'w') as f:
    print(*answer, sep='\n',file=f)
'''