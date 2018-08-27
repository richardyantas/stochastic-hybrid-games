F=main

${F}.pdf: ${F}.tex main.bib *.tex
	pdflatex ${F}
	bibtex ${F}
	pdflatex ${F}
	pdflatex ${F}

.PHONY : view
view: ${F}.pdf
	if [ $(USER) = mt ]; then xpdf ${F}.pdf; else evince ${F}.pdf; fi &

.PHONY : clean
clean:
	rm -f ${F}.pdf ${F}.aux ${F}.bbl ${F}.blg ${F}.log ${F}.toc ${F}.idx
