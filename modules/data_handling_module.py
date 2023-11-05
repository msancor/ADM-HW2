#Here we import the necessary libraries
import pandas as pd
import numpy as np
from typing import List, Tuple
from collections import Counter
import jsonlines

#Here we set the maximum number of columns to display when printing a dataframe
pd.set_option('display.max_columns', None)

#Here we default the chained assignment warning to None. We dothis to avoid the SettingWithCopyWarning warning (specifically in the ChatGPT functions)
pd.options.mode.chained_assignment = None 

def get_data(dataset_name:str, upload_all: bool = False, columns: list = None, dtype: dict = None, chunksize:int=100) -> pd.DataFrame:
    """
    Function that reads a json file and returns a dataframe with the data.

    Args:
        dataset_name (str): Name of the dataset.
        upload_all (bool, optional): If True, all the data is uploaded. Defaults to False.
        columns (list, optional): List of columns to drop. Defaults to None.
        dtype (dict, optional): Dictionary with the data types of the columns. Defaults to None.
        chunksize (int, optional): Number of rows to read. Defaults to 10000.

    Returns:
        dataset (pd.DataFrame): Dataframe with the dataset.
    """
   #Here we read the json file in chunks from the json file depending on the dataset name
    if dataset_name == "authors":
        chunks= pd.read_json('./data/lighter_authors.json', dtype=dtype, lines=True, chunksize=chunksize)
    elif dataset_name == "books":
        chunks = pd.read_json('./data/lighter_books.json', dtype=dtype, lines=True,  chunksize=chunksize)
    #If the dataset name is not valid, we raise an error
    else:
        assert False, f"Dataset name {dataset_name} is not valid. Please choose between 'authors' and 'books'."

    #Here we create an empty dataframe
    dataset = pd.DataFrame()

    #Here we iterate over the chunks
    for chunk in chunks:
        #If the columns argument is not None, we drop the columns
        if columns is not None:
            chunk.drop(columns=columns, axis=1, inplace=True)
        
        #Here we concatenate the chunks
        dataset = pd.concat([dataset, chunk])

        #If we don't want to upload all the data, we break the loop in order to upload only the first chunk
        if upload_all== False:
            break
    #In this last step we convert all the empty values to NaN
    return dataset.replace('', np.nan)

def get_worst_books_list() -> list:
    with jsonlines.open('./data/list.json', 'r') as jsonl_f:
        for object in jsonl_f:
            if object.get("title") == "The Worst Books of All Time":
                return object.get("books")

def set_column_as_index(dataset: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Function that sets a column as the index of a dataframe.

    Args:
        dataset (pd.DataFrame): Dataframe with the dataset.
        column_name (str): Name of the column to set as index.

    Returns:
        dataset (pd.DataFrame): Dataframe with the dataset.
    """
    #Here we set the column as index ONLY if it is unique
    if dataset[column_name].is_unique:
        dataset.set_index(column_name, inplace=True)
    else:
        print(f"The {column_name} column is not unique. The index will not be set.")
    
    return dataset


def sort_dataset_by_column(dataset: pd.DataFrame, column_name: List[str], number_of_rows: int = 10, key: callable = None, ascending: bool=False) -> pd.DataFrame:
    """
    Function that returns a dataset sorted by a column.

    Args:
        dataset (pd.DataFrame): Dataframe with dataset.
        column_name (str): Name of the column to sort by.
        number_of_rows (int, optional): Number of rows to return. Defaults to 10.
        key (callable, optional): Function to apply to the column values. Defaults to None.
        ascending (bool, optional): If True, the sorting is ascending. Defaults to False.

    Returns:
        authors_dataset (pd.DataFrame): Dataframe with the authors dataset.
    """
    
    #Here we sort the dataset by the number of works in descending order.
    dataset = dataset.sort_values(by=column_name, key = key, ascending=ascending)
    #Here we return the first n rows
    return dataset.head(number_of_rows)

def count_column_values(dataframe_column: pd.Series, limit: int = 10, general_name: str = "other") -> pd.Series:
    """
    Function that counts the values of a column until a limit and summarizes the rest as "general_name".

    Args:
        dataframe_column (pd.Series): Dataframe column.
        limit (int, optional): Number of rows to return. Defaults to 10.
        general_name (str, optional): Name of the general category. Defaults to "other".

    Returns:
        dataframe_column_counts (pd.Series): Dataframe column with the counts.
    """
    #Here we count the values of the column and store them in a dictionary
    dataframe_column_counts = dict(dataframe_column.value_counts())

    #Here we create a list of labels of the count keys and substitute the values of the last n keys with the general name
    labels = list(dataframe_column_counts.keys())[:limit]
    labels.append(general_name)

    #Here we create a list of values of the count keys and substitute the values of the last n keys with the sum of these values
    values = list(dataframe_column_counts.values())[:limit]
    values.append(sum(list(dataframe_column_counts.values())[limit:]))

    #Here we return the labels and values lists
    return labels, values

def standardize_time_column_to_period(dataset: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Function that standardizes a column with dates to a period format.

    Args:
        dataset (pd.DataFrame): Dataframe with dataset.
        column_name (str): Name of the column to standardize. It can have string values in format "YYYY", "YYYY-MM" or "YYYY-MM-DD".

    Returns:
        dataset (pd.DataFrame): Dataframe with the dataset.
    """

    #Here we assert that the column is a string column
    assert dataset[column_name].dtype == "object", f"The {column_name} column is not a string column."

    #Finally we convert the column to a daily period column. This is done using the pd.Period function
    dataset[column_name] = dataset[column_name].apply(lambda x: pd.Period(x, freq='D'))

    #Here we return the dataset
    return dataset

def historical_data(books_dataset:pd.DataFrame, column_name: str, year: int) -> pd.DataFrame:
    """
    Function that returns a dataframe with historical data for a given year for the books dataset.

    Args:
        books_dataset (pd.DataFrame): Dataframe with the books dataset.
        column_name (str): Name of the column to use. It has to be a Pandas Period column.
        year (int): Year to use.

    Returns:
        pd.DataFrame: Dataframe with the historical data.
    """

    #Here we assert that the column is a period column
    assert books_dataset[column_name].dtype == "period[D]", f"The {column_name} column is not a Pandas Period column."

    #Here we create a dataset with the books of the given year
    yearly_books_dataset = books_dataset[books_dataset[column_name].dt.year == year]

    #Here we calculate the total number of books and total number of pages of the year
    book_number = len(yearly_books_dataset)
    pages_number = yearly_books_dataset.num_pages.sum()
    #Here we calculate the most prolific month of the year. To do this, we count the number of books per month and get the index of the maximum value
    prolific_month = yearly_books_dataset[column_name].dt.month.value_counts().idxmax()

    #Here we get the longest book of the year. To do this, we get the maximum value of the num_pages column and get the title of the book with that value
    longest_book = yearly_books_dataset[yearly_books_dataset.num_pages == yearly_books_dataset.num_pages.max()].title.tolist()[0]
    
    #Here we return a dataframe with the historical data
    return pd.DataFrame({
        "Year": [int(year)],
        "Total Number of Books": [book_number],
        "Total Number of Pages": [int(pages_number)] ,
        "Most Prolific Month": [prolific_month],
        "Longest Book": [longest_book]
    })


def historical_dataframe(books_dataset:pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Function that returns a dataframe with historical data for all the years for the books dataset.

    Args:
        books_dataset (pd.DataFrame): Dataframe with the books dataset.
        column_name (str): Name of the column to use.

    Returns:
        historical_dataframe (pd.DataFrame): Dataframe with the historical data.
    """

    #Here we assert that the column is a period column
    assert books_dataset[column_name].dtype == "period[D]", f"The {column_name} column is not a Pandas Period column."

    #Here we obtain all the years that appear in the column. We use the unique() function to get the unique values
    years = np.sort(books_dataset[column_name].dt.year.unique())

    #Here we create an empty dataframe
    historical_dataframe = pd.DataFrame()

    #Here we iterate over the years and concatenate the historical data for each year
    for year in years:
        historical_dataframe = pd.concat([historical_dataframe, historical_data(books_dataset, column_name, year)])
    
    #Finally we set the year column as index
    historical_dataframe.set_index("Year", inplace=True)

    #Here we return the historical dataframe
    return historical_dataframe


def get_yearly_stats(books_df, year):
    """
    Function that returns a dictionary with information about the books published in a given year (Made by ChatGPT)

    Args:
        books_df (pd.DataFrame): Dataframe with the books dataset.
        year (int): Year to use.

    Returns:
        dict: Dictionary with the information.
    """
    # Filter books published in the specified year
    year_filter = books_df['original_publication_date'].dt.year == year
    books_in_year = books_df[year_filter]

    if books_in_year.empty:
        return {
            "Total Number of Books": 0,
            "Total Number of Pages": 0,
            "Most Prolific Month": None,
            "Longest Book": None
        }

    # Calculate the total number of books published in the year
    total_books = len(books_in_year)

    # Calculate the total number of pages written in the year
    total_pages = books_in_year['num_pages'].sum()

    # Extract the month and year from the publication date
    books_in_year['month'] = books_in_year['original_publication_date'].dt.month

    # Find the most prolific month in terms of book publications
    most_prolific_month = books_in_year['month'].value_counts().idxmax()

    # Find the longest book written in the year
    longest_book = books_in_year.loc[books_in_year['num_pages'].idxmax()]['title']

    return {
        "Total Number of Books": total_books,
        "Total Number of Pages": total_pages,
        "Most Prolific Month": most_prolific_month,
        "Longest Book": longest_book
    }

def build_yearly_stats_dataframe(books_df):
    """
    Function that returns a dataframe with information about the books published in each year (Made by ChatGPT)

    Args:
        books_df (pd.DataFrame): Dataframe with the books dataset.

    Returns:
        yearly_stats_df (pd.DataFrame): Dataframe with the information.
    """
    # Extract unique years from the "original_publication_date" column
    unique_years = books_df['original_publication_date'].dt.year.unique()

    # Create a list of dictionaries to store yearly statistics
    yearly_stats_list = []

    # Calculate and populate statistics for each year
    for year in unique_years:
        yearly_stats = get_yearly_stats(books_df, year)
        yearly_stats['Year'] = year
        yearly_stats_list.append(yearly_stats)

    # Convert the list of dictionaries to a DataFrame
    yearly_stats_df = pd.DataFrame(yearly_stats_list)
    yearly_stats_df.set_index('Year', inplace=True)

    return yearly_stats_df

def build_dict_of_books(books_dataframe: pd.DataFrame, author_ids: list)-> dict:
    """
    Function that returns a dictionary with the book names of the authors in the author_ids list.

    Args:
        books_dataframe (pd.DataFrame): Dataframe with the books dataset.
        author_ids (list): List with the author ids.

    Returns:
        dict_of_books (dict): Dictionary with the book names of the authors in the author_ids list.
    """
    #Here we define a new filtered dataframe containing only books of the authors in the author_ids list
    #We use the isin() function in order to obtain True when the author_id is in the author_ids list and False otherwise
    filtered_books_dataframe = books_dataframe[books_dataframe.author_id.isin(author_ids)]

    #Here we create the dictionary of books using the groupby() function. This function groups the dataframe by the author_id column
    #Then we apply the list() function to the title column of the grouped dataframe in order to get a list of the book names of each author
    #Finally we convert the grouped dataframe to a dictionary using the to_dict() function
    dict_of_books = filtered_books_dataframe.groupby("author_id")["title"].apply(list).to_dict()

    #Here we return the dictionary of books
    return dict_of_books

def get_average_time_gap(dates_list: List[pd.Period]) -> float:
    """
    Function that returns the average time gap between subsequent dates.

    Args:
        dates_list (List[pd.Period]): List of dates.

    Returns:
        float: Average time gap between subsequent dates.
    """
    #Here we create a list with pairs of subsequent dates
    pairs_list = zip(dates_list[:-1], dates_list[1:])
    #Here we calculate the time gap between subsequent dates by converting the dates to timestamps and subtracting them
    time_gaps_list = [(pd.Timestamp(date2.to_timestamp()) - pd.Timestamp(date1.to_timestamp())).days for date1, date2 in pairs_list]
    #Here we calculate the average time gap
    average_time_gap = sum(time_gaps_list)/len(time_gaps_list)
    #Here we return the average time gap
    return average_time_gap

def get_cumulative_date_values(dates_list: List[pd.Period]) -> List[Tuple[int]]:
    """
    Function that returns a list of pairs with a year and the cumulative number of books published until that year.

    Args:
        dates_list (List[pd.Period]): List of dates.

    Returns:
        List[Tuple[int]]: List of pairs with a year and the cumulative number of books published until that year.

    """
    #First we count the number of occurrences of each year for the dates in the dates_list
    years_counter = Counter([date.year for date in dates_list])

    #Here we create a list of pairs with a year and the cumulative number of books published until that year
    #First we create a year list with the sorted unique years that appear in the dates_list
    year_list = sorted(list(set([date.year for date in dates_list])))
    cumulative_values_list = []
    #Then we create a list of pairs with a year and the cumulative number of books published until that year
    total_books = 0
    for year in year_list:
        total_books += years_counter[year]
        cumulative_values_list.append((year, total_books))


    #Here we return the cumulative values list
    return cumulative_values_list

def get_ratings_above_limit_ratio(average_rating_dist: str, limit: int = 4) -> float:
    """
    Function that returns the ratio of ratings above a limit.

    Args:
        average_rating_dist (str): Average rating distribution.
        limit (int, optional): Limit to use. Defaults to 4.

    Returns:
        float: Ratio of ratings above a limit.
    """
    #First we assert that the limit is between 1 and 5
    assert 1 <= limit <= 5, f"The limit must be between 1 and 5. The limit {limit} is not valid."

    #Then we parse the average rating distribution string
    items = average_rating_dist.split('|')
    #Now we create a list with the numbers of ratings above the limit until 5 which is the maximum rating
    ratings_above_limit_list = [str(i) for i in range(limit, 6)]

    #Here we initialize the sum of ratings above the limit
    ratings_above_limit_sum = 0

    #Here we iterate over the values and extract the number of ratings above the limit
    for item in items:
        rating, count = item.split(':')
        if rating in ratings_above_limit_list:
            ratings_above_limit_sum += int(count)
        elif rating == "total":
            total_ratings = int(count)

    if int(total_ratings) == 0:
        return 0
    
    #Finally we return the ratio of ratings above the limit
    return ratings_above_limit_sum/total_ratings










