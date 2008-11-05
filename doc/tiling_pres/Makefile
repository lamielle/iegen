all: pres
pres:
	pdflatex iegen-presentation
	pdflatex iegen-presentation
#	bibtex iegen-presentation
#	bibtex iegen-presentation
#	pdflatex iegen-presentation

view: pres
	acroread iegen-presentation.pdf && pdfaction --ctrlw --altl

clean:
	rm -f *.aux *.log *.bbl *.blg *.nav *.out *.snm *.toc

depclean: clean
	rm -f *.pdf *.dvi
