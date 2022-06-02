CC=gcc
#CFLAGS=
OBJS=
LIBS=


args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

%:
    @:

day:
	@echo $(call args,defaultstring)
	@g++ -o ../bin/day_$(call args,$@) day_$(call args,$@).cpp
	@cd ..; ./bin/day_$(call args,$@) -v -v


