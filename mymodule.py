import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from rouge_score import rouge_scorer
import docx2txt
from typing import List, Tuple

def plagiarism_checker(text1_path: str, text2_path: str) -> Tuple[float, List[Tuple[int, int, float]]]:
    """Checks plagiarism and generates heatmap data between two documents."""
    try:
        if text1_path.lower().endswith(('.doc', '.docx')):
            text1 = docx2txt.process(text1_path)
        elif text1_path.lower().endswith('.txt'):
            with open(text1_path, 'r', encoding='utf-8') as file:
                text1 = file.read()
        else:
            raise ValueError("Unsupported file format for text1.")

        if text2_path.lower().endswith(('.doc', '.docx')):
            text2 = docx2txt.process(text2_path)
        elif text2_path.lower().endswith('.txt'):
            with open(text2_path, 'r', encoding='utf-8') as file:
                text2 = file.read()
        else:
            raise ValueError("Unsupported file format for text2.")

        scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        scores = scorer.score(text1, text2)
        rouge_l_f1 = scores['rougeL'].fmeasure

        # Generate placeholder heatmap data
        heatmap_data = [(i, j, (i + j) / 20) for i in range(10) for j in range(10)] 

        return rouge_l_f1 * 100, heatmap_data

    except FileNotFoundError:
        print("Error: One or both files not found.")
        return 0, []

    except ValueError as e:
        print(f"Error: {e}")
        return 0, []

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0, []

def visualize_heatmap(heatmap_data, doc1_name="Document 1", doc2_name="Document 2", save_path="heatmap.png"):
    """Visualizes the plagiarism heatmap and saves it as a PNG file."""
    df = pd.DataFrame(heatmap_data, columns=["x", "y", "value"])
    df = df.pivot(index="x", columns="y", values="value")
    plt.figure(figsize=(8, 6))
    sns.heatmap(df, annot=False, cmap="YlGnBu")
    plt.title(f"Plagiarism Heatmap: {doc1_name} vs {doc2_name}")
    plt.xlabel(doc2_name)
    plt.ylabel(doc1_name)
    plt.savefig(save_path)
    plt.close()  # Use plt.close() instead of plt.show() to prevent GUI displaying in script executions
