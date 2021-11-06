CC=gcc
#CFLAGS=
OBJS=
LIBS=

all: make_all run_all

make_all: make_1 make_2 make_3

run_all: run_1 run_2 run_3

day_1:
	(make make_1 run_1)

day_2:
	(make make_2 run_2)

day_3:
	(make make_3 run_3)

make_1:
	g++ -o ../bin/day_1 day_1.cpp $(OBJS) $(LIBS)

make_2:
	g++ -o ../bin/day_2 day_2.cpp $(OBJS) $(LIBS)

make_3:
	$(CC) -o ../bin/day_3 day_3.c $(OBJS) $(LIBS)

run_1:
	(echo "\nDay 1"; cd ..; ./bin/day_1)

run_2:
	(echo "\nDay 2"; cd ..; ./bin/day_2)

run_3:
	(echo "\nDay 3"; cd ..; ./bin/day_3)


