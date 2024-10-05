# TNA010 - PageRank Algorithm

## Overview

This project implements the PageRank algorithm, originally developed by Google, to rank web pages based on their importance in a network. The implementation is based on the methods described in _Matrix Methods in Data Mining and Pattern Recognition (2nd Edition)_ by Lars Eldén.

## Algorithm Description

PageRank works by modeling web surfing behavior as a probabilistic process. It assigns a numerical weight (rank) to each webpage based on:

1. The number and quality of links pointing to the page
2. The rank of the pages that link to it

The algorithm uses the following key concepts:

- **Sparse Adjacency Matrix**: Represents the web as a directed graph where each element represents the probability of moving from one page to another
- **Power Method**: An iterative approach to compute the final rank values

## Features

- Reads network data from a text file
- Constructs a sparse matrix representation of the web graph
- Implements multiple solving methods:
  - Eigenvalue decomposition (for small matrices)
  - Standard Power Method
  - Optimized Power Method
- Visualizes results with a bar plot
- Identifies and displays top-ranked pages

## Prerequisites

- MATLAB R2019b or later

## Installation

1. Clone this repository:

```
git clone https://github.com/rasmussvala/TNA010-Page-Ranking.git
```

2. Navigate to the project directory in MATLAB

## Usage

- Run the algorithm by running: PageRank.mlx
- Change data at the top of PageRank.mlx `fileID = fopen('Data/data-course-book-1.txt', 'r');`
