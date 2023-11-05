"""
In this question, you are asked to provide the most commonly used tags for book lists. 
Going through the [__list.json__](https://www.kaggle.com/datasets/opalskies/large-books-metadata-dataset-50-mill-entries) file, you'll notice that each list has a list of tags attached, and we want to see what are the <ins>most popular tags</ins> across all of the lists. 
Please report the __top 5__ most frequently used tags and the number of times they appear in the lists.
"""
#Solution:
#First we import the jsonlines module. We do this since we want to read the json file line by line and take only the tags from each line.
#We also import the time module to measure the time it takes to run the script.
#Finally, we import the Counter class from the collections module. We do this since we want to count the number of occurrences of each tag.
import time
import jsonlines
from collections import Counter

#Here we start counting the time it takes to run the script.
start_time = time.time()

#Here we create a list to store the tags of each line. It is important to note that some lines do not have tags, so we must check for this.
with jsonlines.open('./data/list.json', 'r') as jsonl_f:
    tags_list = [obj.get("tags") for obj in jsonl_f if obj.get("tags") != None]

#Here we flatten the list of lists into a list.
tags_list = [tag for sublist in tags_list for tag in sublist]

#Here we create a counter object to count the number of occurrences of each tag.
tags_ocurrences = Counter(tags_list)

#Here we print the top 5 most frequently used tags and the number of times they appear in the lists as a Markdown table.
print("| tag | #usage |")
print("| --- | --- |")
#The .most_common method returns a list of tuples, where each tuple contains the tag and the number of times it appears in the lists.
for tag, count in tags_ocurrences.most_common(5):
    print(f"| {tag} | {count} |")

#Here we print the time it took to run the script.
print(f"{time.time() - start_time} seconds")

