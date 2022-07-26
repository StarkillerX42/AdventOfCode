#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars
using Statistics


function polymerize(in_polymer::Vector{String}, map::Dict{String, String}, verbose::Int=0)
    out_polymer = Vector{String}()
    for (i, char) in enumerate(in_polymer[begin:end-1])
        if verbose >= 2
            println(char)
        end
        parent = char * in_polymer[i + 1]
        push!(out_polymer, char)
        push!(out_polymer, map[parent])
    end
    push!(out_polymer, in_polymer[end])
    return out_polymer
end


function get_partial_score(polymer::Vector{String}, alphabet::Vector{String},
    verbose::Int=0)::Dict{String, Int}
    out = Dict{String, Int}()
    for k in alphabet
        out[k] = count(c -> c == k, polymer[begin:end - 1])
    end
    return out
end


function get_score(polymer::Vector{String},
        alphabet::Vector{String},
        verbose=0::Int)::Int
    max_val = 0
    min_val = length(polymer)
    for char in alphabet
        n = count(c -> c == char, polymer)
        max_val = max(max_val, n)
        min_val = n == 0 ? min_val : min(min_val, n)
        if verbose >= 3
            println(char, ", ", count(c -> c == char, polymer))
        end
    end
    if verbose >= 2
        println("Max: ", max_val, " Min: ", min_val)
    end
    return max_val - min_val
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
    lines = readlines(open(data_path, "r"))

    i_polymer = convert(Vector{String}, split(lines[1], ""))
    polymer = copy(i_polymer)
    mapping = Dict{String, String}()
    for line in lines[3:end]
        if line == ""
            continue
        end
        key, val = split(line, " -> ")
        mapping[key] = val
    end



    alphabet = Vector{String}()
    for k in keys(mapping)
        left, right = convert(Vector{String}, split(k, ""))
        if !(left in alphabet)
            push!(alphabet, left)
        end
        if !(right in alphabet)
            push!(alphabet, right)
        end
    end
    # alphabet = convert(Vector{String}, split("ABCDEFGHIJKLMNOPQRSTUVWXYZ", ""))

    if args["verbose"] >= 1
        println("Starting polymer is ", polymer)
        println("Alphabet length is ", length(alphabet))
    end

    part_1 = 0
    for i in ProgressBar(1:20)
        polymer = polymerize(polymer, mapping)
        if i == 10
            part_1 = get_score(polymer, alphabet, args["verbose"])
        end
    end
    @printf("Part 1: %d\n", part_1)


    value_map = Dict{String, Dict{String, Int}}()
    for k in ProgressBar(keys(mapping))
        k_p = convert(Vector{String}, split(k, ""))
        for _ in 1:20
            k_p = polymerize(k_p, mapping)
        end
        value_map[k] = get_partial_score(k_p, alphabet, args["verbose"])
    end

    part_2_counts = Dict{String, Int}()
    for char in alphabet
        part_2_counts[char] = 0
    end

    for i in ProgressBar(1:length(polymer) - 1)
        parent = polymer[i] * polymer[i + 1]
        for char in alphabet
            part_2_counts[char] += value_map[parent][char]
        end
    end
    part_2_counts[polymer[end]] += 1

    min_val = minimum(collect(values(part_2_counts))[values(part_2_counts) .!= 0])
    max_val = maximum(values(part_2_counts)) 
    part_2 = max_val - min_val

    if args["verbose"] >= 2
        println(part_2_counts)
    end

    @printf("Part 2: %d\n", part_2)

end

main()
