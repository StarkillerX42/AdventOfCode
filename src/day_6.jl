#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


function count_children(fishes :: Array{Int, 1}, i::Int, lim::Int)
    n_children = 0
    if i != lim
        for fish in fishes
            if fish == 0
                n_children += count_children([8], i + 1, lim)
                n_children += count_children([6], i + 1, lim)
                fish = 6
            else
                n_children += count_children([fish - 1], i + 1, lim)
            end
        end
    else
        n_children = length(fishes)
    end
    return n_children
end


function parse_cmdline()
    parser = ArgParseSettings()

    @add_arg_table! parser begin
        "-v", "--verbose"
            help="Verbose debugging"
            action = :count_invocations
        "-t", "--test"
            help="Use test file"
            action = :store_true
        # "count"
            # arg_type=Int
            # required = true
    end
    return parse_args(parser)
end


function main()
    args = parse_cmdline()
    path_parts = split(PROGRAM_FILE, "/")
    day = split(split(path_parts[length(path_parts)], "_")[2], ".")[1]
    project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
    if !args["test"]
        data_path = joinpath(project_dir, "dat/day_" * day * ".txt")
    else
        data_path = joinpath(project_dir, "dat/day_" * day * "_test.txt")
    end
    
    inputs = readline(open(data_path, "r"))
    n_fish = length(split(inputs, ','))
    @printf("There are %d fish\n", n_fish)
    fish_states = Array{Int, 1}(undef, n_fish)
    for (i, f) in enumerate(split(inputs, ','))
        fish_states[i] = parse(Int, f)
    end

    part_1_fishes = copy(fish_states)    
    for i=1:80
        for j=1:length(part_1_fishes)
            if part_1_fishes[j] == 0
                part_1_fishes[j] = 6
                push!(part_1_fishes, 8)
            else
                part_1_fishes[j] -= 1
            end
        end
    end

    @printf("Part 1: %d\n", length(part_1_fishes))

    ages = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    half_pops = []
    println("Populating Table")
    for (i, age) in ProgressBar(enumerate(ages))
        fishes = [age]
        for j=1:128
            for k=1:length(fishes)
                if fishes[k] == 0
                    fishes[k] = 6
                    push!(fishes, 8)
                else
                    fishes[k] -= 1
                end
            end
        end
        push!(half_pops, fishes)
    end

    println("Solving Final State")
    part_2 = 0
    for fish in ProgressBar(fish_states)
        for (i, age) in enumerate(ages)
            if fish == age
                half_state = half_pops[i]
                for half_fish in half_state
                    for (i, age) in enumerate(ages)
                        if half_fish == age
                            part_2 += length(half_pops[i])
                        end
                    end
                end
            end
        end
    end

    @printf("Part 2: %d\n", part_2)

end

main()
