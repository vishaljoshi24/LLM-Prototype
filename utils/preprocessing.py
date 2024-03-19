import glob


def pdf_preprocessing(folder_path='files/tabletopresources'):
    # Iterating through each file in the folder
    for file in glob.glob(folder_path + "/*.pdf"):
        print(file)


if __name__ == "__main__":
    pdf_preprocessing()
