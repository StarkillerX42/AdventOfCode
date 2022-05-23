#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars
using Statistics


function fold_x(arr::Array, val::Int, verbose::Int=0)
    if verbose >= 1
        display(arr)
        println("Original Array")
        println("Folding along x= ", val, " with shape ", size(arr))
    end
    new_arr = Array{Bool, 2}(undef, val, size(arr)[2])
    new_arr[1:1:val, :] = arr[1:1:val, :]
    for i=1:val - 1
        if verbose >= 2
            println(val, ", ", i)
        end
        for j=1:size(arr)[2]
            new_arr[val - i, j] = new_arr[val - i, j] || arr[val + i, j]
        end
    end
    if verbose >= 1
        display(new_arr)
        println("Final Array with shape ", size(arr))
    end
    return new_arr
end


function fold_y(arr::Array, val::Int, verbose::Int=0)
    if verbose >= 1
        display(transpose(arr))
        println("Original Array")
        println("Folding along y= ", val, " with shape ", size(arr))
    end
    new_arr = Array{Bool, 2}(undef, size(arr)[1], val)
    new_arr[:, 1:1:val] = arr[:, 1:1:val]
    for j=1:size(arr)[1]
        for i=1:val - 1
            if verbose >= 2
                println(val, ", ", val - i, ", ", val + i, ", ", new_arr[j, val - i], ", ", arr[j, val + i], " = ", new_arr[j, val - i] || arr[j, val + i])
            end
            new_arr[j, val - i] = new_arr[j, val - i] || arr[j, val + i]
        end
    end
    if verbose >= 1
        display(transpose(new_arr))
        println("Final Array with shape ", size(new_arr))
    end
    return new_arr
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

    n_x = 0
    n_y = 0
    n_instr = 0
    for line in lines
        if ',' in line
            x, y = split(line, ',')
            x = parse(Int, x)
            y = parse(Int, y)
            n_x = max(n_x, x + 1)
            n_y = max(n_y, y + 1)
        elseif '=' in line
            n_instr += 1
            ax, n = split(split(line, ' ')[end], '=')
            if ax == "x"
                n_x = max(n_x, parse(Int, n) * 2 + 1)
            end
            if ax == "y"
                n_y = max(n_y, parse(Int, n) * 2 + 1)
            end
        end
    end

    println(n_x, "x", n_y, ", ", n_instr)
    points = Array{Bool, 2}(undef, n_x, n_y)
    points[:, :] .= 0
    instr_ax = Array{String, 1}(undef, n_instr)
    instr_val = Array{Int, 1}(undef, n_instr)

    i_instr = 1
    for (i, line) in enumerate(lines)
        if ',' in line
            x, y = split(line, ',')
            x = parse(Int, x)
            y = parse(Int, y)
            points[x + 1, y + 1] = true
        elseif '=' in line
            ax, n = split(split(line, ' ')[end], '=')
            instr_ax[i_instr] = ax
            instr_val[i_instr] = parse(Int, n) + 1
            i_instr += 1
        end
    end

    if args["verbose"] >= 1
        display(transpose(points))
        println()
    end

    part_1 = 0
    for i=1:length(instr_ax)
        println(instr_val[i], instr_ax[i], size(points))
        if instr_ax[i] == "x"
            points = fold_x(points, instr_val[i], args["verbose"])
        elseif instr_ax[i] == "y"
            points = fold_y(points, instr_val[i], args["verbose"])
        end
        if i == 1
            part_1 = length(findall(==(1), points))
        end
    end
    display(transpose(points))
    println()
    @printf("Part 1: %d\n", part_1)
    for i=1:size(points)[2]
        for j=1:size(points)[1]
            print(points[j, i] ? "\u25A0" : "\u25A1")
        end
        print('\n')
    end


end


main()
