## Constellate Client

Notebook client for Constellate.

See documentation: https://constellate.org/docs/constellate-client

To import and verify installation:
```python
import constellate

dataset = constellate.get_description("0e912814-41d2-82b3-2463-5472700303e3")
print(dataset["search_description"])
```

If the library is installed properly, the following output will be displayed:

>inflation from JSTOR from 1910 - 1920