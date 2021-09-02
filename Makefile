# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
GITHUBOUT			= docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile watch github

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

watch:
	@sphinx-autobuild --port 5001 $(SOURCEDIR) $(BUILDDIR)

github:
	@sphinx-apidoc -o source/opennem opennem
	@make html
	@cp -a $(BUILDDIR)/html/. $(GITHUBOUT)
	@git add docs/
	@git diff-index --quiet HEAD || git commit -m "AUTO: builddocs"
