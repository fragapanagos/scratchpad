# target names
TGT := tgt
LIST := list

all: ${TGT}

${TGT}: ${LIST}
	touch `cat ${LIST}`
	date > $@ 

${LIST}: foo1.out foo2.out
	mv $@.ref $@
	echo "${LIST} contains: `cat $@`"

foo1%out foo2%out: foo%in
	echo "foo1.out foo2.out" >> ${LIST}.ref

foo.in:
	touch foo.in

clean:
	rm -f foo.in
	rm -f foo1.out foo2.out
	rm -f ${LIST} ${LIST}.ref
	rm -f tgt

clean_lists:
	rm -f ${LIST} ${LIST}.ref

.INTERMEDIATE: ${LIST}
.PHONY: all clean clean_lists
