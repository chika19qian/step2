import sys, time
import collections
# source venv/bin/activate
import numpy as np
import pandas as pd
from pandas import Series


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        q = collections.deque()
        visited = {}
        # find the ID of start and visit all the items
        start_id = [k for k, v in self.titles.items() if v == start][0]
        q.append(start_id)
        visited[start_id] = start_id
        while q:
            node = q.popleft()
            for child in self.links[node]:
                if child not in visited:
                    visited[child] = node
                    q.append(child)
        # find the path
        path_num = []
        path = []
        goal_id = [k for k, v in self.titles.items() if v == goal][0]
        node = goal_id
        while not node == start_id:
            path_num.append(node)
            node = visited[node]
        path_num.append(start_id)
        path_num.reverse()
        for i in path_num:
            path.append(self.titles[i])
        print("The shortest path from %s to %s is:" % (start, goal))
        print(path)

    # Helped by CHATGPT
    def find_most_popular_pages(self):
        num_pages = len(self.titles)
        initial_value = 1.0
        original_page_rank = np.full(num_pages, initial_value)
        new_page_rank = np.zeros(num_pages)

        # calculate the sum of page rank
        initial_sum = original_page_rank.sum()
        print(f"Initial PageRank sum: {initial_sum}")

        # map page ids to indices
        id_to_index = {id: index for index, id in enumerate(self.titles.keys())}
        index_to_id = {index: id for id, index in id_to_index.items()}

        # Create an array for the number of links each page has
        links_count = np.zeros(num_pages)
        for child_id, child_link in self.links.items():
            child_index = id_to_index[child_id]
            links_count[child_index] = len(child_link)

        converged = False
        iteration_count = 0
        damping_factor = 0.85

        while not converged:
            new_page_rank.fill(0)
            give_all = 0.15 * original_page_rank.sum() / num_pages

            for child_id, child_link in self.links.items():
                child_index = id_to_index[child_id]
                rank = original_page_rank[child_index]
                if links_count[child_index] == 0:
                    give_neighbor = damping_factor * rank / num_pages
                    new_page_rank += give_neighbor
                else:
                    give_neighbor = damping_factor * rank / links_count[child_index]
                    for neighbor in child_link:
                        neighbor_index = id_to_index[neighbor]
                        new_page_rank[neighbor_index] += give_neighbor

            new_page_rank += give_all

            converged = np.allclose(original_page_rank, new_page_rank, atol=0.05)
            original_page_rank = new_page_rank.copy()
            iteration_count += 1

        page_rank = sorted([(index_to_id[i], rank) for i, rank in enumerate(original_page_rank)], key=lambda x: x[1], reverse=True)
        
        with open('most_popular_pages.txt', 'w') as f:
            if len(page_rank) > 10:
                for i in range(10):
                    line = f"ID: {page_rank[i][0]}, Title: {self.titles[page_rank[i][0]]}, PageRank: {page_rank[i][1]}\n"
                    f.write(line)
                    print(line.strip())  
            else:
                for pr in page_rank:
                    line = f"ID: {pr[0]}, Title: {self.titles[pr[0]]}, PageRank: {pr[1]}\n"
                    f.write(line)
                    print(line.strip())  

        # check if the sum of the page rank is the same
        total_rank = original_page_rank.sum()
        print(f"Final PageRank sum: {total_rank}, Iterations: {iteration_count}")



    # Do something more interesting!!
    def find_most_longest_continuous_titles(self):
        longest = {}
        for title in self.titles.values():
            max_count = 1
            count = 1
            for i in range(1, len(title)):
                if title[i] == title[i - 1]:
                    count += 1
                else:
                    if count >= max_count:
                        max_count = count
                    count = 1
            longest[title] = max_count
        longest = sorted(longest.items(), key=lambda x:x[1], reverse=True)
        with open('longest_continuous_titles.txt', 'w') as f:
            print(*longest, sep='\n',file=f)




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    #wikipedia.find_longest_titles()
    #wikipedia.find_most_linked_pages()
    #wikipedia.find_shortest_path("A", "F")
    #wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
    #wikipedia.find_most_longest_continuous_titles()
