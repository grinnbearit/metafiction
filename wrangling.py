# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Metafiction
# ## Data Wrangling

# <codecell>

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
# %matplotlib inline

# <codecell>

import json

metafiction = [json.loads(x) for x in open("metafiction.dat")]
len(metafiction)

# <markdowncell>

# ### authors

# <codecell>

author_list = [{"author": rec["id"], "name": rec["name"]} for rec in metafiction]

len(author_list)

# <codecell>

for record in metafiction:
    for story in record["favourite-stories"]:
        author_list.append({"author": story["author"]})
    for author in record["favourite-authors"]:
        author_list.append({"author": author})

len(author_list)

# <codecell>

authors = DataFrame(author_list)
authors.drop_duplicates(["author"], inplace=True)
authors.set_index(["author"], inplace=True)

len(authors)

# <codecell>

authors.ix[[0]]

# <markdowncell>

# ## stories

# <codecell>

story_list = []

for record in metafiction:
    story_list.extend(record["author-stories"])
    story_list.extend(record["favourite-stories"])

len(story_list)

# <codecell>

stories = DataFrame(story_list)

## rename columns
columns = stories.columns.values
columns[3] = u"is_complete"
columns[4] = u"submitted"
columns[5] = u"updated"
columns[9] = u"story"
stories.columns = columns 

stories.drop_duplicates(["story"], inplace=True)
stories.set_index("story", inplace=True)
stories["submitted"] = stories["submitted"].astype("datetime64")
stories["updated"] = stories["updated"].astype("datetime64")

len(stories)

# <codecell>

stories.ix[[0]]

# <markdowncell>

# ## favourites

# <codecell>

favourite_author_list = []
favourite_story_list = []

for record in metafiction:
    for author in record["favourite-authors"]:
        favourite_author_list.append({"author": record["id"],
                                      "favourite_author": author})
    for story in record["favourite-stories"]:
        favourite_story_list.append({"author": record["id"],
                                     "favourite_story": story["id"]})
        
(len(favourite_author_list), len(favourite_story_list))

# <codecell>

favourite_authors = DataFrame(favourite_author_list)
favourite_authors.set_index("author", inplace=True)
favourite_authors = favourite_authors["favourite_author"]

favourite_stories = DataFrame(favourite_story_list)
favourite_stories.set_index("author", inplace=True)
favourite_stories = favourite_stories["favourite_story"]

# <codecell>

favourite_authors.ix[[0]]

# <codecell>

favourite_stories.ix[[0]]

# <markdowncell>

# ## genres and categories

# <codecell>

genre_list = sorted(set.union(*[set(g) for g in stories["genres"]]))
genres = DataFrame(data=np.zeros((len(stories), len(genre_list))), columns=genre_list, index=stories.index)

category_list = sorted(set.union(*[set(c) for c in stories["categories"]]))
categories = DataFrame(data=np.zeros((len(stories), len(category_list))), columns=category_list, index=stories.index)

for story in stories.index:
    genres.ix[story, stories.ix[story, "genres"]] = 1
    categories.ix[story, stories.ix[story, "categories"]] = 1

# <codecell>

genres.ix[[0]]

# <codecell>

categories.ix[[0]]

