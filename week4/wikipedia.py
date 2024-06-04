import sys, time
import collections
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


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        num_pages = len(self.titles)
        original_page_rank = np.ones(num_pages)
        new_initial_page_rank = np.zeros(num_pages)
        print("初始值",original_page_rank, new_initial_page_rank)

        # count the sum of the initial page rank
        initial_sum = original_page_rank.sum()
        print("Initial PageRank sum: %f" % (initial_sum))

        # add ID as the index of the numpy array
        id_list = list(self.titles.keys())
        original_page_rank = Series(original_page_rank, index = id_list)
        print("加入id后ori",original_page_rank)
        new_initial_page_rank = Series(new_initial_page_rank, index = id_list)
        print("加入id后new",new_initial_page_rank)

        # iterate until converged
        converged = False
        iteration_count = 0

        while not converged:
            begin = time.time()
            give_all = 0
            new_page_rank = new_initial_page_rank.copy()

            for child_id, child_link in self.links.items():
                if len(child_link) == 0:
                    give_all = original_page_rank[child_id] / num_pages
                else:
                    give_neighbor = 0.85 * original_page_rank[child_id] / len(child_link)
                    give_all += 0.15 * original_page_rank[child_id] / num_pages
                for neighbor in child_link:
                    new_page_rank[neighbor] += give_neighbor
            give_all = 0.15 * original_page_rank.sum() / num_pages
            new_page_rank += give_all

            converged = np.allclose(original_page_rank, new_page_rank, atol=0.05)
            original_page_rank = new_page_rank
            iteration_count += 1
            end = time.time()
        print("%d %.6f" % (iteration_count, end - begin))

        page_rank = np.sort(original_page_rank)[::-1]
        
        if len(page_rank) > 10:
            page_rank = page_rank[:10]
        print(page_rank)

        # check if the sum of the page rank is the same
        total_rank = original_page_rank.sum()
        print(f"Final PageRank sum: {total_rank}")



    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


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
