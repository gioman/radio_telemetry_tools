pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128 . || true

clean:
	rm -f $(ALL_FILES)
	find -name "*.pyc" -exec rm -f {} \;
	rm -f *.zip

package: clean
	cd .. && rm -f *.zip && zip -r sextante_animove.zip sextante_animove -x \*.pyc \*~ \*.git\* \*Makefile*
	mv ../sextante_animove.zip .

