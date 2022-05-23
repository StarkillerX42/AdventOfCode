#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars
using Statistics


function find_paths_1(conns, history, verbose=0)
    paths = []
    for nexts in conns[history[end]]
        if !islowercase(nexts[1]) || !(nexts in history) && history[end] != "end"
            new_paths = find_paths_1(conns, vcat(history, nexts))
            for p in new_paths
                if !(p in paths)
                    push!(paths, p)
                end
            end
        elseif history[end] =="end"
            push!(paths, history)
        end
    end
    return paths
end


function find_paths_2(conns, history, verbose=0)
    paths = []
    for nexts in conns[history[end]]
        if history == ["start"]
            println(nexts)
        end
        if nexts == "start"
            continue
        end
        if verbose >= 1
            print("Next, ", nexts, " for path ", history, "\n")
        end
        if history[end] == "end"
            push!(paths, history)
        elseif islowercase(nexts[1]) && nexts != "start" && nexts != "end"
            revisit = false
            for p in history
                if islowercase(p[1]) && count(==(p), history) > 1
                    revisit = true
                end
            end
            if verbose >= 2
                println(revisit)
            end
            if !revisit || !(nexts in history)
                new_paths = find_paths_2(conns, vcat(history, nexts), verbose)
                for p in new_paths
                    if !(p in paths)
                        if verbose >= 2
                            print("Appending ", p, "\n")
                        end
                        push!(paths, p)
                    end
                end
            end
        else
            new_paths = find_paths_2(conns, vcat(history, nexts), verbose)
            for p in new_paths
                if !(p in paths)
                    if verbose >= 2
                        print("Appending ", p, "\n")
                    end
                    push!(paths, p)
                end
            end
        end
    end

    return paths
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
    connections = Dict{String, Array{String}}()
    for line in lines
        p1, p2 = split(line, '-')
        if !(p1 in keys(connections))
            connections[p1] = [p2]
        else
            push!(connections[p1], p2)
        end
        if !(p2 in keys(connections))
            connections[p2] = [p1]
        else
            push!(connections[p2], p1)
        end
    end
    println(connections["start"])
    paths = find_paths_1(connections, ["start"], args["verbose"])
    if args["verbose"] >= 1
        println(join(paths, "\n"))
    end
    @printf("Part 1: %d\n", length(paths))

    paths_2 = find_paths_2(connections, ["start"], args["verbose"])

    if args["verbose"] >= 1
        println(join(paths_2, "\n"))
    end
    @printf("Part 2: %d\n", length(paths_2))


end


main()
