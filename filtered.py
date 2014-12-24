# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Metafiction
# ## Filtered Data Analysis

# <codecell>

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
# %matplotlib inline

# <codecell>

from wrangling import authors, stories, favourite_authors, favourite_stories, genres, categories

# <markdowncell>

# ## Subset Similarity
# 
# I'm not interested in all stories, just certain genres and categories.
# 
# It would nice to be able to only focus on those

# <codecell>

def jaccard_index(set1, set2):
    i_count = len(set1.intersection(set2))
    u_count = len(set1.union(set2))
    return 0 if u_count == 0 else i_count/float(u_count)

# <codecell>

from collections import namedtuple
Metafiction = namedtuple("Metafiction", ["authors", "stories", "favourite_authors", 
                                         "favourite_stories", "genres", "categories"])

def story_subset(genres_list=None, categories_list=None):
    """returns stor matching these genres and categories
    
    None implies no filter"""
     
    g_stories = genres if genres_list == None else genres[genres_list]
    c_stories = categories if categories_list == None else categories[categories_list]
    
    g_story_set = set(genres.index if genres_list == None else genres[g_stories.sum(axis=1) > 0].index)
    c_story_set = set(categories.index if categories_list == None else categories[c_stories.sum(axis=1) > 0].index)
    
    return g_story_set.intersection(c_story_set)
    

def metafiction_subset(ids=[]):
    """returns a Metafiction object containing datasets that only refer to the passed story ids"""
    f_stories = stories.ix[ids]
    f_authors = authors.ix[f_stories["author"].drop_duplicates()]
    f_fav_stories = favourite_stories[favourite_stories.isin(ids)]
    f_fav_authors = favourite_authors[favourite_authors.isin(f_authors.index)]
    f_genres = genres.ix[ids][genres.columns[genres.ix[ids].sum() > 0]]
    f_categories = categories.ix[ids][categories.columns[categories.ix[ids].sum() > 0]]
    
    return Metafiction(authors=f_authors, stories=f_stories, favourite_authors=f_fav_authors,
                       favourite_stories=f_fav_stories, genres=f_genres, categories=f_categories)

# <markdowncell>

# An `author_similarity` that accepts a passed metafiction object

# <codecell>

def author_similarity(author, my_stories, mfobj):
    author_stories = set(mfobj.stories[mfobj.stories["author"] == author.name].index)
    author_favourites = set(mfobj.favourite_stories.ix[author.name]) if author.name in mfobj.favourite_stories else set()
    all_stories = author_stories.union(author_favourites)
    return jaccard_index(all_stories, my_stories)

# <markdowncell>

# Stories about __Harry Potter__, __Naruto__ and __Pokemon__

# <codecell>

story_ids = story_subset(categories_list=[u"Harry Potter", u"Naruto", u"Pokémon"])
mfobj = metafiction_subset(story_ids)

# <codecell>

my_fav_stories = ["8096183", # Harry Potter and the Natural 20
                  "9794740", # Pokemon, The Origin of Species
                  "9311012", # Lighting up the Dark
                  "5782108", # Harry Potter and the Methods of Rationality
                  "7354757", # The Game of Champions
                  "5193644", # Time Braid
                  "3695087", # Larceny, Lechery and Luna Lovegood
                  "9669819", # The Two Year Emperor
                  ]

# <codecell>

filtered_favs = set(my_fav_stories).intersection(story_ids)
filtered_favs

# <markdowncell>

# ## Scoring Authors

# <codecell>

auth_sim_series = mfobj.authors.apply(author_similarity, axis=1, args=(filtered_favs, mfobj))
auth_sim_series.name = "similarity"
auth_sim = mfobj.authors.join(auth_sim_series)

# <codecell>

auth_sim.sort("similarity", ascending=False)[:5]

# <markdowncell>

# ## Scoring Stories

# <codecell>

story_sim_values = DataFrame(index=mfobj.stories.index, columns=["sim_total", "sim_count", "similarity"])

# the writer's similarity + count
story_sim_values["sim_total"] = auth_sim.ix[mfobj.stories.ix[story_sim_values.index]["author"].values]["similarity"].values
story_sim_values["sim_count"] = 1

for author in auth_sim.iterrows():
    author_favs = mfobj.favourite_stories.get(author[0], Series())
    story_sim_values.loc[author_favs, "sim_total"] += author[1]["similarity"]
    story_sim_values.loc[author_favs, "sim_count"] += 1
    
story_sim_values["similarity"] = story_sim_values["sim_total"].div(story_sim_values["sim_count"])
story_sim = mfobj.stories.join(story_sim_values)

# <markdowncell>

# ## Stories by similarity

# <codecell>

story_sim.sort("similarity", ascending=False)[:5][["title", "sim_total", "sim_count", "similarity"]]

# <markdowncell>

# ## Stories by total similarity

# <codecell>

story_sim.sort("sim_total", ascending=False)[:5][["title", "sim_total", "sim_count", "similarity"]]

# <markdowncell>

# ## Stories by times favourited

# <codecell>

story_sim.sort("sim_count", ascending=False)[:5][["title", "sim_total", "sim_count", "similarity"]]

