#!/usr/bin/env julia

using ArgParse
using Dates
using JSON
using ProgressBars
using Statistics
using Combinatorics

function parse_cmdline()
    parser = ArgParseSettings()

    @add_arg_table! parser begin
        "-v", "--verbose"
            help="verbose debugging"
            action = :count_invocations
        "-t", "--test"
            help="use test file"
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
        hextext = readline(open(data_path, "r"))
    else
        hextext = "D2FE28"
    end
    bittext = BitArray(undef, length(hextext) * 4)

    for (i, char) in enumerate(hextext)
        if occursin(r"\d", string(char))  # If it's an integer
            v = parse(Int, char)
        else  # If it's a char
            v = Int(char) - Int('A') + 10
        end
        bin_array = reverse(digits(v, base=2, pad=4))
        bittext[(i - 1) * 4 + 1: (i - 1) * 4 + 4] = bin_array
    end
    version = bittext[1:3]
    type_id = bittext[4:6]
    println(type_id, typeof(type_id))
    println(digits(type_id, base=10))
    if type_id == 4
        i = 7
        bin_num = Array{Int}(undef)
        while bittext[i] != 0
            push!(bin_num, bittext[i:i+4])
            i += 4
        end
        push!(bin_num, bittext[i:i+4])
        println(bin_num)
    end


end


main()
