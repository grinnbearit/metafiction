# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Metafiction
# ## Data Analysis

# <codecell>

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
# %matplotlib inline

# <codecell>

from wrangling import authors, stories, favourite_authors, favourite_stories, genres, categories

# <markdowncell>

# ## Similarity

# <markdowncell>

# I need to calculate a similarity measure between two authors/users. 
# 
# Since I care about story preference, I'll use the [Jaccard Index](http://en.wikipedia.org/wiki/Jaccard_index) on favourite story sets.

# <codecell>

def jaccard_index(set1, set2):
    i_count = len(set1.intersection(set2))
    u_count = len(set1.union(set2))
    return 0 if u_count == 0 else i_count/float(u_count)

# <markdowncell>

# ## Scoring Authors
# 
# Comparing author's favourite stories with mine

# <codecell>

def author_similarity(author, my_stories):
    author_stories = set(stories[stories["author"] == author.name].index)
    author_favourites = set(favourite_stories.ix[author.name]) if author.name in favourite_stories else set()
    all_stories = author_stories.union(author_favourites)
    return jaccard_index(all_stories, set(my_stories))

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

authors["similarity"] = authors.apply(author_similarity, axis=1, args=(my_fav_stories,))

# <codecell>

authors.sort("similarity", ascending=False)[:5]

# <markdowncell>

# ## Scoring Stories
# 
# Calculating the weighted average of all stories by author similarity

# <codecell>

# The sum of the similarity of every author who has favourited this story + the writer's similarity
stories["sim_total"] = authors.ix[stories["author"]]["similarity"].values

# The total number of times this story has been favourited + written (1)
stories["sim_count"] = 1

for author in authors.iterrows():
    author_favs = favourite_stories.get(author[0], Series())
    stories.loc[author_favs, "sim_total"] += author[1]["similarity"]
    stories.loc[author_favs, "sim_count"] += 1

stories["sim_score"] = stories["sim_total"].div(stories["sim_count"])

# <markdowncell>

# ### Stories by average score

# <codecell>

stories.sort("sim_score", ascending=False)[:5][["title", "sim_total", "sim_count", "sim_score"]]

# <markdowncell>

# ### Stories by Total Similarity

# <codecell>

stories.sort("sim_total", ascending=False)[:5][["title", "sim_total", "sim_count", "sim_score"]]

# <markdowncell>

# ### Stories by Times Favourited

# <codecell>

stories.sort("sim_count", ascending=False)[:5][["title", "sim_total", "sim_count", "sim_score"]]

