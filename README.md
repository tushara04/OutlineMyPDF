Academics and students heavily rely on textbook PDFs, but many PDFs lack an outline with page mapping in the metadata, making navigation quite a pain because then we have to scroll back to the content page to locate sections. Neither is there a reliable online tool for this. This repository provides steps to convert a PDF into OCR and generate outlines for easier navigation in a PDF viewer.

## Setup
Note that the commands that follow are run on my Arch Linux system with nvim text editor but they can similarly be ran on other OSes and systems. I assume you have the basic software like python and git installed already. Reach out for help specific to your system.

1. In your project directory, create a virtual environment and then activate it: 
	```
	python -m venv pdfenv
	source pdfenv/bin/activate
	```

2. Clone the repo to access some files: 
	```
	git clone https://github.com/tushara04/OutlineMyPDF.git
	```

3. Move to the directory:
	```
	cd OutlineMyPDF
	```

4. Then install the packages you'll need:
	```
	pip install -r requirements.txt
	```

## OCR the PDF
If your PDF does not allow text recognition, you need to OCR it before you can generate outlines. Note that you only need this step for added convenience. If you do not want to OCR (for whatever weird reason), then you can manually copy the content page into a text file and clean it as described in the next section.

1. `pip install ocrmypdf`
2. `sudo pacman -S tesseract-data-eng`
3. `ocrmypdf non_OCR_book.pdf OCR_book.pdf`

Make sure the path to the PDF is correct and complete. Requirement for setting up the library differs from OS to OS, so make sure to refer to the documentation cited below [1].

## Outline the PDF
Some manual work has to be done due to the arbitrariness in the format of the content pages of books.

1. Get the PDF page numbers to the start and the end of the table of content: `content_start_page` and `content_end_page`.
2. Go to the printed page 1 of the book and subtract 1 from the PDF page number corresponding to that printed page 1 to get the `offset_value`. 

	i.e. if your printed page 1 is at PDF page 14, then `offset_value = 14-1 = 13`.

3. Then extract the table of content: 
	```
	pdftotext -layout -f content_start_page -l content_end_page "book.pdf" content.txt
	```
This copies *all* the content in the given pages in the exact format as the PDF (hence the need for the next step). Make sure to change `book.pdf` into the correct path of the PDF and to replace the variables `content_start_page` and `content_end_page` with the right values.

4. Open the text file (`nvim content.txt`) and clean it to match the .bmk format.

**Rules for .bmk format [2]**:
1. You may want to remove the "Table of Content" heading, but you can also choose to keep it with page number being `content_start_page`.
2. Each line in the content represents a bookmark item to be mapped to the page number.
3. The title of a section/chapter is separated from its PDF page number by at least 4 dots.
4. Indentation of 2 spaces specify the level of a bookmark.
5. To add custom bookmarks, follow the same format and add anything (as shown in the last line of the example) with the correct PDF page number.

Example (directly taken from [2], but I added the last line and kept just 4 dots):
```
序....1
Chapter 1....4
Chapter 2....5
  2.1 Section 1....6
    2.1.1 SubSection 1....6
    2.1.2 SubSection 2....8
  2.2 Section 2....12
Chapter 3....20
Appendix....36
Anything....<Page Number>
```

When cleaning, make sure to remove headers or footers of a page that appear as result of page change in the PDF, which gets copied exactly when running the step 2 command. Make sure there are no white spaces between dots or between dots and page numbers. Also make sure the indentation is exactly 2 spaces. PDF-Bookmark is sensitive about these conditions. You may use an LLM here to by giving it the content of the content.txt file and the rules and asking to clean it for you; or asking it to write you a script that does the cleaning for you given the rules.

5. bmk format requires the PDF page number mapped to a title. But the printed table of content maps a title to its printed page number. So, run the following command to offset the page numbers and ensure correct mapping.
	```
	python bmk_generator.py content.txt offset_value > content.bmk
	```
	Replace	the `offset_value` variable with the calculation you did earlier.

6. Finally, use the content.bmk file to add the outlines in the PDF of your book. The new PDF will be saved in the current directory but you can put any path.
	```
	pdf-bookmark -p book.pdf -b content.bmk -o book_with_outline.pdf
	```

If anything fails, please raise an issue or let me know directly. I have tested it twice in my system and it works well.

## References
[1] [OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/introduction.html)  

[2] [PDF-Bookmark](https://pypi.org/project/pdf-bookmark/)  

[3] [pdftotext](https://pypi.org/project/pdftotext/)  

[4] Used Chat-GPT to generate the bmk_generator.py script to fix the printed page numbers in the content.txt with the offset value matching the PDF page number. 

All the other work is my own.
