<style>
  h1 {
    color: #3794FF;
    background-color: #00232B;
    border: hidden;
    font-size: 3em;
    text-align: center;
    padding-top: 25px;
    padding-bottom: 25px;
    margin: 0px;
  }
  h2 {
    font-size: 2em;
    margin-top: 20px;
    margin-bottom: 10px;
  }
  h3, h4 {
    font-size: 1.5em;
    margin-top: 20px;
    margin-bottom: 20px;
  } 
  summary {
    font-size: 1.15em;
    font-weight: 600;
    margin-top: 20px;
    padding-bottom: 20px;
    line-height: 1.25;
  }
  ul {
    font-size: 1.15em;
    padding-top: 20px;
    padding-bottom: 10px;
  }
  ol {
    font-size: 1.15em;
    padding-bottom: 20px;
  }
  table {
    width: 100%;
    align: center;
    padding: 10 10 10 10;
    margin: 10 10 10 10;
    background-color: #00232B;
  }
  th {
    display: none;
  }
  tr {
    border: hidden;
    padding: 0 0 0 0;
    margin: 0 0 0 0;
  }
  td {
    border: hidden;
    padding: 0 0 0 0;
    margin: 0 0 0 0;
  }
  p {
    padding-left: 20px;
    padding-top: 10px;
    padding-bottom: 20px;
  }
  hr {
    margin-top: 0px;
  }
  blockquote {
    padding-bottom: 5px;
  }
</style>

# DataCake

| _                          | _               | _                              | _                   |                       _ |                      _ |                _                 |
| -------------------------- | --------------- | ------------------------------ | ------------------- | ---------------------- | --------------------- | ------------------------------: |
| [![PyPI Badge]][PyPI Link] | ![PyPI Version] | [![GitHub Badge]][GitHub Link] | ![GitHub Commits]   |   ![GitHub Open Issues] |   ![GitHub Open Pulls] |  [![Python Made]][Python Link]   |
| ![PyPI Month Downloads]    | ![PyPI Status]  | ![GitHub Hits]                 | ![GitHub Downloads] | ![GitHub Closed Issues] | ![GitHub Closed Pulls] | [![Codeium Built]][Codeium Link] |

## Table of Contents
> ### [Introduction](#an-introduction)
> 1. [Features](#features-checklist)
> 2. [Motivation](#my-motivation)
> ___
> ### [Data](#the-data)
> 2. [A Sample](#a-sample)
> 3. [Some Questions](#some-questions)
> 4. [Some Answers](#some-answers)
> 5. [The Context](#the-context)
> ___
> ### [Ingredients](#the-ingredients)
> 6. [Flattening](#flattening)
> 7. [Scattering](#scattering)
> 8. [Spattering](#spattering)
> ___
> ### [Algorithms](#the-implementation)
> 9. []()
> 10. [Index Bucketing](#index-bucket)
> ___
> ### [Cake](#the-cake)
> 11. []()

$~$

## An Introduction
> ### Features Checklist
> ___
> - [ ] `1. Flattens Deeply Nested Data`
> 
> *"How flat are we talking? It'll make your data flatter than a pancake!"*
> ___
> - [ ] `2. Without Unnecessarily Duplicating Data`
>
> *"So, I get the whole cake and nothing but the cake? No more and no less!"*
> ___
> - [ ] `3. With No Loss of Information`
> 
> *"You can have your cake and eat it too? Every bit of it!"*
> ___
> - [ ] `4. Using MongoDB-Style Syntax`
> 
> *"Is it a piece of cake? You can bet your buns!"*
> ___
> - [ ] `5. Integrated with Numpy and Numba`
> 
> *"Is that a cherry on top? Why yes it is!"*

$~$

## The Data
To illustrate DataCake's features, I'll be utilizing a small sample from the [SQuAD][1] dataset.
___
> <details>
> <summary id="a-sample">
> A Sample
> </summary>
>
> ```py
> #####
> # Simplified Sample of the SQuAD Dataset
> # - Don't worry about analyzing this too much
> # - We will break it down step-by-step
> #####
> data: dict = {
>   "qas": [{
>     "question": "In what country is Normandy located?",
>     "answers": [{
>       "text": "France",
>       "answer_start": 159
>     }],
>     "is_impossible": False
>   }, {
>     "question": "When were the Normans in Normandy?",
>     "answers": [{
>       "text": "10th and 11th centuries",
>       "answer_start": 94
>     }, {
>       "text": "in the 10th and 11th centuries",
>       "answer_start": 87
>     }],
>     "is_impossible": False
>   }, {
>     "question": "From which countries did the Norse originate?",
>     "answers": [{
>       "text": "Denmark, Iceland and Norway",
>       "answer_start": 256
>     }],
>     "is_impossible": False
>   }, {
>     "question": "Who was the Norse leader?",
>     "answers": [{
>       "text": "Rollo",
>       "answer_start": 308
>     }],
>     "is_impossible": False
>   }, {
>     "question": "What century did the Normans first gain their separate identity?",
>     "answers": [{
>       "text": "10th century",
>       "answer_start": 671
>     }, {
>       "text": "the first half of the 10th century",
>       "answer_start": 649
>     }, {
>     "is_impossible": False
>     }]
>   }, {
>     "plausible_answers": [{
>       "text": "Normans",
>       "answer_start": 4
>     }],
>     "question": "Who gave their name to Normandy in the 1000's and 1100's",
>     "answers": [],
>     "is_impossible": True
>   }, {
>     "plausible_answers": [{
>       "text": "Normandy",
>       "answer_start": 137
>     }],
>     "question": "What is France a region of?",
>     "answers": [],
>     "is_impossible": True
>   }],
>   "context": "The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. They were descended from Norse (\"Norman\" comes from \"Norseman\") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries."
> }
> ```
>
> </details>
___
> <details>
> <summary id="some-questions">
> Some Questions
> </summary>
>
> ```py
> #####
> # List of Sample Questions and If Answering is Impossible
> # - For our needs, impossible questions are not desirable
> #####
> questions = [{
>   "question": "In what country is Normandy located?",
>   "is_impossible": False
> }, {
>   "question": "When were the Normans in Normandy?",
>   "is_impossible": False
> }, {
>   "question": "From which countries did the Norse originate?",
>   "is_impossible": False
> }, {
>   "question": "Who was the Norse leader?",
>   "is_impossible": False
> }, {
>   "question": "What century did the Normans first gain their separate identity?",
>   "is_impossible": False
> }, {
>   "question": "Who gave their name to Normandy in the 1000's and 1100's?",
>   "is_impossible": True
> }, {
>   "question": "What is France a region of?",
>   "is_impossible": True
> }]
> ```
> 
> </details>
___
> <details>
> <summary id="some-answers">
> Some Answers
> </summary>
>
> ```py
> ##### - Answers
> # Here we have lists of answers from the possible questions.
> # Note that some questions have multiple correct answers.
> # Each answer also has its beginning index found in the context.
> # We want each of these answers, but we can get rid of the indexes.
> # Each answer needs to be associated to its appropriate question.
> # This needs to be done without any unnecessary duplication.
> 
> answers = [
>   # In what country is Normandy located?
>   [{
>     "text": "France",
>     "answer_start": 159
>   }],
>   # When were the Normans in Normandy?
>   [{
>     "text": "10th and 11th centuries",
>     "answer_start": 94
>   }, {
>     "text": "in the 10th and 11th centuries",
>     "answer_start": 87
>   }],
>   # From which countries did the Norse originate?
>   [{
>     "text": "Denmark, Iceland and Norway",
>     "answer_start": 256
>   }],
>   # Who was the Norse leader?
>   [{
>     "text": "Rollo",
>     "answer_start": 308
>   }],
>   # What century did the Normans first gain their separate identity?
>   [{
>     "text": "10th century",
>     "answer_start": 671
>   }, {
>     "text": "the first half of the 10th century",
>     "answer_start": 649
>   }]
> ]
> ```
>
> ```py
> ##### - Plausible Answers
> # These are the plausible answers given with the impossible questions.
> # They do not adequately answer their questions.
> # We only want good answers extracted from the context.
>
> plausible = [
>   # Who gave their name to Normandy in the 1000's and 1100's?
>   [{
>     "text": "Normans",
>     "answer_start": 4
>   }],
>   # What is France a region of?
>   [{
>     "text": "Normandy",
>     "answer_start": 137
>   }]
> ]
> ```
>
> </details>
___
> <details>
> <summary id="the-context">
> The Context
> </summary>
>
> ```py
> ##### - The Context
> # This is where all of the questions and answers are derived from.
> # Each record of data will need to access it.
> # We want to do this without any unnecessary duplication.
> 
> context = "The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. They were descended from Norse (\"Norman\" comes from \"Norseman\") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries."
> ```
> 
> </details>

$~$
$~$

## The Ingredients
Need to write something.
___
> <details>
> <summary id="flattening">
> Flattening
> </summary>
>
> ```py
> ##### - Ingredients After Flattening
> # This is a sample of the special keys from the sample data.
> # Ingredients begin to take shape after the first flattening step.
> # The integer values represent indexes as they are derived from the data.
> # The string values represent the features derived from the data.
> # Each data value has an tuple of these ingredient keys.
> data = { "data": [{
>   "qas": [{
>     "question": "In what country is Normandy located?", ((0, "data"), (0, "qas"), (0, "question"))
>     "answers": [{
>       "text": "France", ((0, "data"), (0, "qas"), (0, "answers"), (0, "text"))
>       "answer_start": 159 ((0, "data"), (0, "qas"), (0, "answers"), (0, "answer_start"))
>     }],
>     "is_impossible": False ((0, "data"), (0, "qas"), (0, "is_impossible"))
>   }, {
>     "question": "When were the Normans in Normandy?",
>     "answers": [{
>       "text": "10th and 11th centuries",
>       "answer_start": 94
>     }, {
>       "text": "in the 10th and 11th centuries",
>       "answer_start": 87
>     }],
>     "is_impossible": False
>   }, {
>     "question": "From which countries did the Norse originate?",
>     "answers": [{
>       "text": "Denmark, Iceland and Norway",
>       "answer_start": 256
>     }],
>     "is_impossible": False
>   }, {
>     "question": "Who was the Norse leader?",
>     "answers": [{
>       "text": "Rollo",
>       "answer_start": 308
>     }],
>     "is_impossible": False
>   }, {
>     "question": "What century did the Normans first gain their separate identity?",
>     "answers": [{
>       "text": "10th century",
>       "answer_start": 671
>     }, {
>       "text": "the first half of the 10th century",
>       "answer_start": 649
>     }, {
>     "is_impossible": False
>     }]
>   }, {
>     "plausible_answers": [{
>       "text": "Normans",
>       "answer_start": 4
>     }],
>     "question": "Who gave their name to Normandy in the 1000's and 1100's",
>     "answers": [],
>     "is_impossible": True
>   }, {
>     "plausible_answers": [{
>       "text": "Normandy",
>       "answer_start": 137
>     }],
>     "question": "What is France a region of?",
>     "answers": [],
>     "is_impossible": True
>   }],
>   "context": "The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. They were descended from Norse (\"Norman\" comes from \"Norseman\") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries." ((0, "data"), (-1, "context"))
> }]}
> ingredients: list[tuple[int, str]] = [
>   ((-1, "context"),),
>   ((0, "paragraphs"), (0, "questions"), (0, "q")),
>   ((0, "paragraphs"), (0, "questions"), (0, "a")),
>   ((0, "paragraphs"), (0, "questions"), (1, "q")),
>   ((0, "paragraphs"), (0, "questions"), (1, "a")),
>   ((0, "paragraphs"), (1, "questions"), (0, "q")),
>   ((0, "paragraphs"), (1, "questions"), (0, "a")),
>   ((0, "paragraphs"), (1, "questions"), (1, "q")),
>   ((0, "paragraphs"), (1, "questions"), (1, "a")),
>   ((0, "paragraphs"), (2, "questions"), (0, "q")),
>   ((0, "paragraphs"), (2, "questions"), (0, "a")),
>   ((0, "paragraphs"), (2, "questions"), (1, "q")),
>   ((0, "paragraphs"), (2, "questions"), (1, "a")),
> ]
> ```
>
> </details>

[Back to Top](#datacake)

[Codeium Link]: https://codeium.com
[Codeium Built]: https://codeium.com/badges/main

[Python Link]: https://www.python.org/
[Python Made]: https://img.shields.io/badge/made_with-Python-1F425F

[GitHub Link]: https://github.com/JeffMII/DataCake
[GitHub Badge]: https://img.shields.io/badge/project-GitHub-green
[GitHub Hits]: https://img.shields.io/github/search/JeffMII/DataCake/goto
[GitHub Release]: https://img.shields.io/github/v/release/JeffMII/DataCake
[GitHub Commits]: https://img.shields.io/github/last-commit/JeffMII/DataCake/main
[GitHub Downloads]: https://img.shields.io/github/downloads/JeffMII/DataCake/total
[GitHub Open Issues]: https://img.shields.io/github/issues/JeffMII/DataCake
[GitHub Closed Issues]: https://img.shields.io/github/issues-closed/JeffMII/DataCake
[GitHub Open Pulls]: https://img.shields.io/github/issues-pr/JeffMII/DataCake
[GitHub Closed Pulls]: https://img.shields.io/github/issues-pr-closed/JeffMII/DataCake
[GitHub License]: https://img.shields.io/github/license/JeffMII/DataCake

[PyPI Link]: https://pypi.org/project/datacake/
[PyPI Badge]: https://img.shields.io/badge/package-PyPI-blue
[PyPI Version]: https://img.shields.io/pypi/v/datacake
[PyPI Status]: https://img.shields.io/pypi/status/ansicolortags.svg
[PyPI Format]: https://img.shields.io/pypi/format/datacake
[PyPI Month Downloads]: https://img.shields.io/pypi/dm/datacake
[PyPI Week Downloads]: https://img.shields.io/pypi/dw/datacake
[PyPI Day Downloads]: https://img.shields.io/pypi/dd/datacake
[PyPI License]: https://img.shields.io/pypi/l/datacake

[SQuAD Badge]: https://img.shields.io/badge/examples_from-SQuAD_2.0-8A2BE2
[SQuAD Link]: https://rajpurkar.github.io/SQuAD-explorer/

--------------

https://dl.ucsc.cmb.ac.lk/jspui/handle/123456789/4216

- Motivation from NIH Preliminary Data Post-Submission Update
- Challenges
  1. Skewness
     - Load Balancing Problem
     - Not Very Well Explored
  2. Programming Mismatch
  3. Information Loss
  4. Partitioning
     - Data Distribution Problem
     - Data Duplication Problem
- Solutions
  1. Shredding
  2. Flatten
     - Map
     - FlatMap
     - Filter
- New Approach: Index Bucketing
  - Overview
    1. Trees
    2. Branches
    3. Leaves
 - Setup
    1. Nested Data to Tree
    2. Branches know their leaves
    3. Leaves know their branches
    4. 

- Flattening Evaluations
  - Index Bucketing
  - Recursive Mapping
  - Pandas Explosion

