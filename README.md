# Metafiction

Analysis of authors and stories on [fanfiction.net](http://fanfiction.net)

## Usage

Install and run [IPython notebook](http://ipython.org/notebook.html)

Start with `analysis.ipynb`

Author's are discovered by a depth first search starting from a seed author, in my
case [Less Wrong](http://fanfiction.net/u/2269863/Less-Wrong)

A scraper to collect the data can be found [here](https://github.com/grinnbearit/crawler/blob/master/src/crawler/fanfiction/author.clj)
(warning [Clojure](http://clojure.com/)

`wrangling.ipynb` "wrangles" scraped authors into [DataFrames](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)

## DataFrames

### authors

fanfiction authors

<table>
<tr>
<th>key</th>
<th>description</th>
<th>type</th>
</tr>
<tr>
<td><b>id</b></td>
<td>fanfiction author id</td>
<td>string</td>
</tr>
</table>

### stories

fanfiction stories

<table>
<tr>
<th>key</th>
<th>description</th>
<th>type</th>
</tr>
<tr>
<td><b>id</b></td>
<td>fanfiction story id</td>
<td>string</td>
</tr>
<tr>
<td>author</td>
<td>fanfiction author id</td>
<td>string</td>
</tr>
<tr>
<td>categories</td>
<td>story categories</td>
<td>[string]</td>
</tr>
<tr>
<td>chapters</td>
<td>number of chapters</td>
<td>int</td>
</tr>
<tr>
<td>completed</td>
<td>story completed?</td>
<td>bool</td>
</tr>
<tr>
<td>favourites</td>
<td>times favourited</td>
<td>int</td>
</tr>
<tr>
<td>follows</td>
<td>times followed</td>
<td>int</td>
</tr>
<tr>
<td>genres</td>
<td>story genres</td>
<td>[string]</td>
</tr>
<tr>
<td>language</td>
<td>language written in</td>
<td>string</td>
</tr>
<tr>
<td>rating</td>
<td>age rating</td>
<td>string</td>
</tr>
<tr>
<td>submitted</td>
<td>when submitted</td>
<td>datetime</td>
</tr>
<tr>
<td>title</td>
<td>story title</td>
<td>string</td>
</tr>
<tr>
<td>updated</td>
<td>when last updated</td>
<td>datetime</td>
</tr>
<tr>
<td>words</td>
<td>number of words</td>
<td>int</td>
</tr>
</table>

### favourite_authors

mapping of author id to favourite author ids

<table>
<tr>
<th>key</th>
<th>description</th>
<th>type</th>
</tr>
<tr>
<td><b>id</b></td>
<td>fanfiction author id</td>
<td>string</td>
</tr>
<tr>
<td>favourite_author</td>
<td>fanfiction author id</td>
<td>string</td>
</tr>
</table>

### favourite_stories

mapping of author id to favourite story ids

<table>
<tr>
<th>key</th>
<th>description</th>
<th>type</th>
</tr>
<tr>
<td><b>id</b></td>
<td>fanfiction author id</td>
<td>string</td>
</tr>
<tr>
<td>favourite_story</td>
<td>fanfiction story id</td>
<td>string</td>
</tr>
</table>

### genres

indicator matrix mapping for story id to genres

<table>
<tr>
<th>key</th>
<th>description</th>
<th>type</th>
</tr>
<tr>
<td><b>id</b></td>
<td>fanfiction story id</td>
<td>string</td>
</tr>
<tr>
<td>genre 1</td>
<td>story genre</td>
<td>0 or 1</td>
</tr>
<tr>
<td>genre 2</td>
<td>story genre</td>
<td>0 or 1</td>
</tr>
<tr>
<td colspan=3>...</td>
</tr>
<tr>
<td>genre n</td>
<td>story genre</td>
<td>0 or 1</td>
</tr>
</table>

### categories

indicator matrix mapping for story id to categories

<table>
<tr>
<th>key</th>
<th>description</th>
<th>type</th>
</tr>
<tr>
<td><b>id</b></td>
<td>fanfiction story id</td>
<td>string</td>
</tr>
<tr>
<td>category 1</td>
<td>story category</td>
<td>0 or 1</td>
</tr>
<tr>
<td>category 2</td>
<td>story category</td>
<td>0 or 1</td>
</tr>
<tr>
<td colspan=3>...</td>
</tr>
<tr>
<td>category n</td>
<td>story category</td>
<td>0 or 1</td>
</tr>
</table>
