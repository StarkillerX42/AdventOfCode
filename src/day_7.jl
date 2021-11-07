#!/usr/bin/env julia
using Printf
using Scanf
using ArgParse
using Formatting

function parse_cmdline()
    parser = ArgParseSettings()

    @add_arg_table! parser begin
        "-v", "--verbose"
            help="Verbose debugging"
            action = :count_invocations
        "-t", "--test"
            help="Use test file"
            action = :store_true
    end
    return parse_args(parser)
end


function process_instructions(directions, verbose=0)
    if verbose >= 1
        println("Decomposing instructions")
    end
    directions = copy(directions)
    assignments = Dict(["1" => 1])
    # println(typeof(assignments))
    count = 0
    while length(directions) > 0 && count < 1000
        for (i, instruction) in enumerate(directions)
            if verbose >= 2
                println(instruction)
            end
            left, right = split(instruction, " -> ")
            if occursin("AND", left)
                first, last = split(left, " AND ")
                if haskey(assignments, first) && haskey(assignments, last)
                    assignments[right] = assignments[first] & assignments[last]
                    deleteat!(directions, i)
                end
            elseif occursin("NOT", left)
                key = match(r"[a-z]{2}|[a-z]{1}", left)
                if key === nothing
                    throw(error("Couldn't parse regex for " * left))
                end
                if haskey(assignments, key.match)
                    assignments[right] = ~assignments[key.match]
                    deleteat!(directions, i)
                end
            elseif occursin("AND", left)
                first, last = split(left, " AND ")
                if haskey(assignments, first) && haskey(assignments, last)
                    assignments[right] = assignments[first] & assignments[last]
                    deleteat!(directions, i)
                end
            elseif occursin("OR", left)
                first, last = split(left, " OR ")
                if haskey(assignments, first) && haskey(assignments, last)
                    assignments[right] = assignments[first] | assignments[last]
                    deleteat!(directions, i)
                end
            elseif occursin("RSHIFT", left)
                first, last = split(left, " RSHIFT ")
                if haskey(assignments, first)
                    assignments[right] = assignments[first] >>> parse(Int, last)
                    deleteat!(directions, i)
                end
            elseif occursin("LSHIFT", left)
                first, last = split(left, " LSHIFT ")
                if haskey(assignments, first)
                    assignments[right] = assignments[first] << parse(Int, last)
                    deleteat!(directions, i)
                end
            else
                if occursin(r"\d", left)
                    val = parse(Int, left)
                    assignments[right] = val
                    deleteat!(directions, i)
                else
                    try
                        if haskey(assignments, left)
                            assignments[right] = assignments[left]
                            deleteat!(directions, i)
                        end
                    catch err
                        println("Could not parse instruction: ", instruction, " with error: ", err)
                    end
                end
            end
        end
        count += 1
        if verbose >= 1
            println(count, ", ", length(directions))
        end
    end
    if verbose >= 2
        println(assignments)
    end
    return assignments

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
    
    fp = open(data_path, "r")
    instructions  = readlines(fp)
    part_1 = process_instructions(instructions)
    
    @printf("Part 1: %d\n", part_1["a"])

    instructions_2 = []
    for (i, instruction) in enumerate(instructions)
        if split(instruction, "-> ")[2] == "b"
            push!(instructions_2, string(part_1["a"]) * " -> b")
        else
            push!(instructions_2, instruction)
        end
    end

    part_2 = process_instructions(instructions_2)

    @printf("Part 2: %d\n", part_2["a"])


end

main()
