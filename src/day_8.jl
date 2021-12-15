#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


function count_occurances(str_arr:: Array{String}, alphabet :: Array{Char}) :: Array{Int}
    counts = fill!(Array{Int, 1}(undef, length(alphabet)), 0)
    for word in str_arr
        for chr in word
            for (i, mtch) in enumerate(alphabet)
                if mtch == chr
                    counts[i] += 1
                end
            end
        end
    end
    return counts
end


function string_sort(inp::String, alphabet::Array{Char})
    out = ""
    for chr in alphabet
        if chr in inp
            out *= chr
        end
    end
    return out
end


function decode(inp, cmap::Dict{Char, Char}, display::Dict{String, Char}, alphabet::Array{Char})
    out_str = ""
    for word in inp
        dec_word = ""
        for chr in word
            dec_word *= cmap[chr]
        end
        dec_word = string_sort(dec_word, alphabet)
        out_str *= display[dec_word]
    end

    out = parse(Int, out_str)
    return out
end


function solve_mapping(scrambled, alphabet::Array{Char}) :: Dict{Char, Char}
    cmap = Dict{Char, Char}()
    one = ""
    seven = ""
    four = ""
    counts = count_occurances(scrambled, alphabet)
    # Max counts is 9, for f
    cmap[alphabet[findmax(counts)[2]]] = 'f'
    # Min counts is 4 for e
    cmap[alphabet[findmin(counts)[2]]] = 'e'
    # 6 counts is b
    cmap[alphabet[counts .== 6][1]] = 'b'

    # Identifying words 
    for word in scrambled
        if length(word) == 2
            one = word
        elseif length(word) == 3
            seven = word
        elseif length(word) == 4
            four = word
        end
    end

    to_a = '0'
    for c in seven
        if !(c in one)
            to_a = c
            cmap[c] = 'a'
        end
    end
    # 8 occurances, but not a, must be c
    cmap[alphabet[(counts .== 8) .& (alphabet .!= to_a)][1]] = 'c'

    for chr in four
        if !(chr in keys(cmap))
            cmap[chr] = 'd'
        end
    end

    for chr in alphabet
        if !(chr in keys(cmap))
            cmap[chr] = 'g'
        end
    end

    return cmap
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
    
    inputs = readlines(open(data_path, "r"))
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    display_dict = Dict("abcefg" => '0', "cf" => '1', "acdeg" => '2', "acdfg" => '3',
        "bcdf" => '4', "abdfg" => '5', "abdefg" => '6', "acf" => '7', "abcdefg" => '8',
        "abcdfg" => '9')

    cypher = Array{String, 2}(undef, length(inputs), 10)
    info = Array{String, 2}(undef, length(inputs), 4)
    part_1 = 0
    for (i, line) in enumerate(inputs)
        left, right = split(line, " | ")
        for (j, word) in enumerate(split(left))
            cypher[i, j] = word
        end
        for (j, key) in enumerate(split(right))
            if length(key) in [2, 3, 4, 7]
                part_1 += 1
            end
            info[i, j] = string_sort(String(key), alphabet)
        end
    end

    part_2 = 0
    mappings = Array{Dict{Char, Char}, 1}(undef, length(inputs))
    for i=1:length(inputs)
        mappings[i] = solve_mapping(cypher[i, :], alphabet)
        part_2 += decode(info[i, :], mappings[i], display_dict, alphabet)
    end

    @printf("Part 1: %d\n", part_1)
    @printf("Part 2: %d\n", part_2)

end

main()
