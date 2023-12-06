"""
Wrapper to display Constellate charts in Jupyter.

Takes a query or dataset id and returns a bar chart display document counts over time.

The Constellate query syntax is documented here: https://constellate.org/docs/constellate-search-syntax

Examples:

>>> charts.documents_over_time({"keyword": "sailing"})
>>> charts.categories_over_time("4999901a-fa17-31da-cfe5-2abf3a429df7")
>>> charts.keyphrases("4999901a-fa17-31da-cfe5-2abf3a429df7")
>>> charts.word_cloud({"keyword": "taxes", "start": 1800, "end": 1900})
>>> charts.term_frequency({"keyword": "taxes"}, terms=["income", "state"])
>>> charts.category_treemap({"docType": "chapter"}, height=1200)

Pass in `url_only=True` to just get the URL for a visualization:
>>> charts.documents_over_time({"keyword": "sailing"}, url_only=True)

"""

try:
    from IPython.core.display import display, HTML
except ImportError as e:
    raise ImportError(
        "Import Error: A working installation of Jupyter notebooks is required to use this feature."
    )


from urllib.parse import urlencode

site_root = "https://constellate.org"
chart_path = site_root + "/charts/%s/?%s"


def _query(qdict):
    return urlencode(qdict, True)


def _render(chart, qdict, terms=None, width="800", height="600", url_only=False):
    if isinstance(qdict, str):
        qdict = {"did": qdict}
    if (terms is not None) and (terms != []):
        qdict["unigrams"] = ",".join([t.lower() for t in terms])
    q = _query(qdict)
    url = chart_path % (chart, q)
    if url_only is True:
        return url
    else:
        return display(
            HTML(
                '<iframe src="%s" height="%s" width="%s" frameborder="0"/><br/><pre>%s</pre>'
                % (url, height, width, url)
            )
        )


def documents_over_time(query, **kwargs):
    return _render("documents-over-time", query, **kwargs)


def categories_over_time(query, **kwargs):
    return _render("categories-over-time", query, **kwargs)


def keyphrases(query, **kwargs):
    return _render("keyphrases", query, **kwargs)


def word_cloud(query, **kwargs):
    return _render("word-cloud", query, **kwargs)


def term_frequency(query, terms, **kwargs):
    return _render("term-frequency", query, terms=terms, **kwargs)


def category_treemap(query, **kwargs):
    return _render("category-treemap", query, **kwargs)
