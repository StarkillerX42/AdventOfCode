#!/usr/bin/env julia
using Printf

project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
data_file = joinpath(project_dir, "dat/day_1.txt")

fp = open(data_file, "r")
parenths = readline(fp)

counter = 0
part_2 = 0
for i = 1:length(parenths)
    if parenths[i] == '('
        global counter += 1
    elseif parenths[i] == ')'
        global counter -= 1
    else
        println("Misunderstood input: ", parenths[i])
    end
    if counter < 0 && part_2 == 0
        global part_2 = i
    end
end
@printf("Part 1: %d\n", counter)
@printf("Part 2: %d\n", part_2)
