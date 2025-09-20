import typer
import os
import pandas as pd
import numpy as np
import itertools 
import seaborn as sns
import matplotlib.pyplot as plt

from itertools import combinations
from matplotlib.colors import ListedColormap, BoundaryNorm



def count_hamming(

    file_w_sequences: str = typer.Option(
        "",
        "--file_w_sequences",
        "-f",
        help='a .txt file containing all sequences for which hamming distances are to be calculated. The file must have only one column, with a header (can be any header, but "Sequence" is preffered).',
    ), 

    figsize_x: str = typer.Option(
        "10",
        "--figsize_x",
        "-x",
        help="The size of the x-axis of the distance matrix. Increase to get prettier plots when you have many sequences in your input file.",
    ),

    figsize_y: str = typer.Option(
        "8",
        "--figsize_y",
        "-y",
        help="The size of the y-axis of the distance matrix. Increase to get prettier plots when you have many sequences in your input file.",
    )
):
    """
    This command takes a .txt file with a list of sequences, calculates hamming distances between all sequences and visualizes all hamming distances with a distance matrix.\n
    """

    # ARGUMENTS CHECK

    # Check that the mandatory input (.txt file) is provided.
    if not file_w_sequences:
        typer.echo(
            """\nYou need to specify --file_w_sequences / -f parameter:\n
                    -> a txt file with one column and a header (e.g. 'Sequence'), have one sequence on each row.\n 
            """
        )
        raise typer.Exit()

    # Check that file exists
    if not os.path.isfile(file_w_sequences):
        typer.secho(
            f'File "{file_w_sequences}" does not exist.\nPlease check .txt file name/path!\n',
            fg=typer.colors.BRIGHT_RED,
        )
        raise typer.Exit(code=1)


    # Try reading the input file
    try:
        input_sequences = pd.read_csv(file_w_sequences, 
                                delimiter='\t')

    except:
        typer.secho(
            f'\nInput .txt file "{file_w_sequences}" does not have the expected format!\nThe .txt file should have a header and each row should hold a sequence.\n',
            fg=typer.colors.BRIGHT_RED
            )
        typer.secho(
            f'\nYour input .txt file "{file_w_sequences}" looks like:\n'
            )
        with open(file_w_sequences, "r") as f:
            print(f.read())

        raise typer.Exit(code=1)
    
    # Rename header
    input_sequences = input_sequences.rename(
        columns={input_sequences.columns[0]: "Sequence"}
    )

    # Check if all sequences (all rows, excluding the header) have the same length
    sequence_lengths = input_sequences['Sequence'].apply(len)

    if not sequence_lengths.nunique() == 1:
        typer.secho(
            f'Not all sequences are the same length! Lengths found: {sequence_lengths.unique()}\n',
            fg=typer.colors.BRIGHT_RED,
        )
        raise typer.Exit(code=1)


    # Once all checks are passed, write all sequnces to a list
    # create libraries list using libraries CSV file
    sequence_list = input_sequences["Sequence"].to_list()


    # --- Count Hamming distance ---
    def hamming_distance(str1, str2):
        '''This function should only be used on strings of equal length.'''
        return sum(c1 != c2 for c1, c2 in zip(str1, str2))

    # ------------ Format sequences to later easily plot the distance matrix ----------
    def get_distance_list(list1, list2):
        sequence_pairs = list(itertools.product(list1, list2))
        distances = [hamming_distance(seq[0], seq[1]) for seq in sequence_pairs]

        # Sets up an empty grid where each cell [i, j] will store the Hamming distance between list1[i] and list2[j]
        distance_matrix = np.zeros((len(list1), len(list2)))
        print(distance_matrix)
        
        # Populate the grid
        for i in range(len(list1)):
            for j in range(len(list2)):
                distance_matrix[i, j] = distances[i * len(list2) + j]
        
        return distance_matrix


    # ------------ Generate ditance matrix with hamming distances ------------

    # Generate combinations and distances
    distance_matrix = get_distance_list(sequence_list, sequence_list)
    print(distance_matrix)

    # ------------ Plot distance matrix ------------

    # Step 1: Get unique values in the matrix
    unique_vals = np.unique(distance_matrix)
    n_colors = len(unique_vals)

    # Step 2: Create colormap and boundaries dynamically
    colors = sns.color_palette("viridis", n_colors=n_colors)
    cmap = ListedColormap(colors)

    # Step 3: Create boundaries between values
    bounds = np.append(unique_vals, unique_vals[-1] + 1)  # e.g., [0, 1, 2, 3] → boundaries for [0-1), [1-2), ...
    norm = BoundaryNorm(bounds, cmap.N)

    # Step 4: Plot
    plt.figure(figsize=(int(figsize_x), 
                        int(figsize_y)))
    
    sns.heatmap(distance_matrix, annot=True, cmap=cmap, norm=norm,
                xticklabels=sequence_list, yticklabels=sequence_list,
                cbar_kws={"ticks": unique_vals},
                square=True)
    
    plt.title("Hamming Distance Matrix", weight='bold', pad=15)
    plt.xlabel("Sequence in List 2")
    plt.ylabel("Sequence in List 1")
    # Tick label aesthetics
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.savefig("hamming_distance_matrix.png", dpi=300)


    # Convert the distance matrix to a pandas DataFrame
    df = pd.DataFrame(distance_matrix, index=sequence_list, columns=sequence_list)

    # --- View and Save ---
    # View
    print(df)

    # Save
    df.to_csv("distance_matrix.csv", header=True, sep=',')
    typer.secho(
        f'\nLibrary mapping info written to distance_matrix.csv file!\n',
        fg=typer.colors.GREEN,
    )

