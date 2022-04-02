#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars
using Statistics


function cut_from_line(line:: String, i:: Int, j:: Int)
    
    if i > 1 & j < length(line)
        return line[begin:i - 1] * line[j + 1:end]
    end

end


function reduce_line(line:: String)
    count = 0
    cond = true
    while cond
        i = 1
        prev_length = length(line)
        while i < length(line)
            if line[i] == '(' && line[i + 1] == ')'
                line = cut_from_line(line, i, i+1)
            elseif line[i] == '{' && line[i + 1] == '}'
                line = cut_from_line(line, i, i+1)
            elseif line[i] == '[' && line[i + 1] == ']'
                line = cut_from_line(line, i, i+1)
            elseif line[i] == '<' && line[i + 1] == '>'
                line = cut_from_line(line, i, i+1)
            else
                i += 1
            end
        end
        count += 1
        cond = count < 100 && length(line) != prev_length
    end
    return line
end


function score_corruption(line::String)
    for chr in line
        if chr == ')'
            return 3
        elseif chr == ']'
            return 57
        elseif chr == '}'
            return 1197
        elseif chr == '>'
            return 25137
        end
    end
    return 0
end


function score_completion(line::String, verbose=0)
    score = 0
    for chr in line[end:-1:begin]
        if chr == '('
            score *= 5
            score += 1
        elseif chr == '['
            score *= 5
            score += 2
        elseif chr == '{'
            score *= 5
            score += 3
        elseif chr == '<'
            score *= 5
            score += 4
        end
    end
    return score

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
    lines = readlines(open(data_path, "r"))
    part_1 = 0
    part_2_scores = []
    for line in lines
        reduced = reduce_line(line)
        corruption = score_corruption(reduced)
        part_1 += corruption
        if args["verbose"] >= 1
            println(line, " -> ", reduced, " Score: ", corruption)
        end
        if corruption == 0
            completer = score_completion(reduced, args["verbose"])
            append!(part_2_scores, completer)
        end
    end
    @printf("Part 1: %d\n", part_1)
    part_2 = median(part_2_scores)
    @printf("Part 2: %d\n", part_2)
end

main()
