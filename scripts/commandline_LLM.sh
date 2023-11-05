#!/bin/bash
#Script that extracts the top 5 series from the series.json file regarding their total book count and displays them as a table (ChatGPT implementation)

# Replace 'input.jsonl' with your actual input file path.
input_file="./data/series.json"

# Extract and print the top 5 book series with the greatest total_books_count.
jq -s 'map({id, title, total_book_count: (.works | map(.books_count | tonumber) | add)}) | sort_by(.total_book_count) | reverse | .[:5]' "$input_file" | jq -r '["id", "title", "total_book_count"], (.[] | [.id, .title, .total_book_count]) | @csv' | csview -s Markdown
