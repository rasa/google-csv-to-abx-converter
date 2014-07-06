CSVS=$(wildcard *.csv)

ABXS=$(CSVS:.csv=.abx)


UNAME_O := $(shell uname -o)
ifeq ($(UNAME_O),Cygwin)
	ADDRESS_BOOK_DIR="$(shell cygpath -m $$USERPROFILE)/Documents/DYMO Label/Address Books"
else
	ADDRESS_BOOK_DIR=""
endif

%.abx: %.csv
	rm -f "$<.tmp"
	iconv -f UTF-16 -t UTF-8  "$<" >"$<.tmp"
	python google-contacts-to-abx.py "$<.tmp" "$@"
	-test -d ${ADDRESS_BOOK_DIR} && \
	cd ${ADDRESS_BOOK_DIR} && \
		test -f "$@" && \
		cp -p --force --backup=numbered --suffix=abx "$@" "$@.backup.abx"
	-test -d ${ADDRESS_BOOK_DIR} && \
		cp -p "$@" ${ADDRESS_BOOK_DIR}
	rm -f "$<.tmp"

.PHONY: all
all:	$(ABXS)

clean:
	rm -f $(ABXS) *.tmp

debug:
	echo CSVS=$(CSVS)
	echo ABXS=$(ABXS)
