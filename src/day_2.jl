#!/usr/bin/env julia
using Printf

project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
data_file = joinpath(project_dir, "dat/day_2.txt")

fp = open(data_file, "r")
packages = readlines(fp)

total_area = 0
total_ribbon = 0

for i=1:length(packages)
    wi, le, he = split(packages[i], 'x')
    wi = parse(Int, wi)
    le = parse(Int, le)
    he = parse(Int, he)
    face1 = wi * le
    face2 = le * he
    face3 = wi * he
    small = min(face1, face2, face3)
    area = 2 * (face1 + face2 + face3) + small
    global total_area += area

    lengths = [wi, le, he]
    bow = prod(lengths)
    deleteat!(lengths, findmax(lengths)[2])
    perim = 2 * sum(lengths)
    global total_ribbon += bow + perim
end

@printf("Part 1: %d\n", total_area)
@printf("Part 2: %d\n", total_ribbon)
