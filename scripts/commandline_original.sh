#!/bin/bash
#Script that extracts the top 5 series from the series.json file regarding their total book count and displays them as a Markdown table
#To be able to run this script, you need to install jq and csview

#Here we define the input file. This absolute path is only valid for the original repository, change it accordingly if you use this script in your own repository
input_file="./data/series.json"

#Step 1: We sort the json file in reverse by the total book count using jq and extract the first 5 entries
#The jq -s option reads the entire input stream into a large array and then applies the filter to it
#The map function is used to extract the book count from each work and add them together after converting them to numbers
#The sort_by function sorts the array by the total book count
#In the end, we format the output to only contain the id, title and total book count of the series and extract the first 5 entries using map and slicing
formatted_data=$(jq -s 'sort_by(.works | map(.books_count | tonumber) | add)|reverse| map({"id": .id, "title": .title, "total_book_count": .works | map(.books_count | tonumber) | add})|.[:5]' "$input_file")

# Step 2: We convert the data to csv format using jq adding a header row
#The echo command is used to pipe the formatted data into jq
#The jq -r option is used to output raw strings
#The jq @csv function converts the data to csv format
csv_data=$(echo "$formatted_data" | jq -r '["id", "title", "total_book_count"],(.[]|[.id, .title, .total_book_count]) | @csv')

# Step 3: We use csview to display the csv data as a Markdown table
echo "$csv_data" | csview -s Markdown
