# GCIDE XML Dictionary Parser

**The GNU Collaborative International Dictionary of English (GCIDE)** is a free dictionary derived from _Webster's Revised Unabridged Dictionary 1913_. GCIDE is created by Patrick J. Cassidy and is maintained by volunteers from around the world. Though GCIDE corpus files use a special markup that requires the **gcider** utility, Michael Dyck converted these corpus files into [XML](https://www.ibiblio.org/webster/).

Using the XML files, this program parses the data using Python. This project is an extension of [gcide-dictionary-json](https://github.com/aviaryan/gcide-dictionary-json) by [Avi Aryan](https://github.com/aviaryan)

## Output Files

The formatted dictionary json files, arranged alphabetically are inside the [chapters](chapters/) folder. The all-in-one dictionary file is [dictionary.json](dictionary.json). Words that are included in the dictionary is inside [words.txt](words.txt).

The basic structure of the json files look like the following:
```json
{
    "word1": [
        {
            "pos": "Part of Speech",
            "definition": "Some definition",
            "sentences": ["Some Sentence", "Another sentence"]
        },
        {
            "pos": "Another Part of Speech",
            "definition": "Another definition",
            "sentences": ["Some Sentence"]
        }
    ],
    "word2": [
        {
            "pos": "Part of Speech",
            "definition": "Some definition",
            "sentences": []
        }
    ]
}
```
