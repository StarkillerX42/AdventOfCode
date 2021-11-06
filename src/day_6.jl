#!/usr/bin/env julia
using Printf
using Scanf
using ArgParse


function parse_cmdline()
    parser = ArgParseSettings()

    @add_arg_table! parser begin
        "-v", "--verbose"
            help="Verbose debugging"
            action = :store_true
        "-t", "--test"
            help="Use test file"
            action = :store_true
    end
    return parse_args(parser)
end


function bitflip_array_rect(array, lowx, lowy, highx, highy)
    for i=lowx + 1:highx + 1
        for j=lowy + 1:highy + 1
            array[i, j] = !array[i, j]
        end
    end
end


function main()
    args = parse_cmdline()
    verbose = args["verbose"]

    project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
    if args["test"]
        data_file = joinpath(project_dir, "dat/day_6_test.txt")
    else
        data_file = joinpath(project_dir, "dat/day_6.txt")
    end

    fp = open(data_file, "r")
    instructions = readlines(fp)

    light_grid = fill!(Array{Bool, 2}(undef, 1000, 1000), false)
    light_grid_2 = fill!(Array{Int, 2}(undef, 1000, 1000), 0)
    startx, starty, endx, endy = Ref{Int}(0), Ref{Int}(0), Ref{Int}(0), Ref{Int}(0)
    # println(light_grid)
    for i=1:length(instructions)
        if verbose
            println(instructions[i])
        end
        if occursin("toggle", instructions[i])
            val = ccall(:sscanf, Cint, (Ptr{UInt8}, Ptr{UInt8}, Ptr{Cvoid}...),
                instructions[i], "toggle %d,%d through %d,%d", startx, starty,
                endx, endy)
            if val == C_NULL
                println("Instruction returned sscanf error: ", instructions[i])
            end
            bitflip_array_rect(light_grid, startx[], starty[], endx[], endy[])
            part_2_val = 2

        elseif occursin("turn on", instructions[i])
            val = ccall(:sscanf, Cint, (Ptr{UInt8}, Ptr{UInt8}, Ptr{Cvoid}...),
                instructions[i], "turn on %d,%d through %d,%d", startx, starty,
                endx, endy)
            if val == C_NULL
                println("Instruction returned sscanf error: ", instructions[i])
            end
            filler = fill!(Array{Bool, 2}(undef, endx[] - startx[] + 1,
                endy[] - starty[] + 1), true)
            light_grid[startx[] + 1: endx[] + 1,
                starty[] + 1: endy[] + 1] = filler
            part_2_val = 1


        elseif occursin("turn off", instructions[i])
            val = ccall(:sscanf, Cint, (Ptr{UInt8}, Ptr{UInt8}, Ptr{Cvoid}...),
                instructions[i], "turn off %d,%d through %d,%d", startx, starty,
                endx, endy)
            if val == C_NULL
                println("Instruction returned sscanf error: ", instructions[i])
            end
            filler = fill!(Array{Bool, 2}(undef, endx[] - startx[] + 1,
                endy[] - starty[] + 1), false)
            light_grid[startx[] + 1: endx[] + 1,
                starty[] + 1: endy[] + 1] = filler
            part_2_val = -1

        else
            @printf("Could not interpret instruction %s\n", instructions[i])
        end

        filler = fill!(Array{Int, 2}(undef, endx[] - startx[] + 1,
            endy[] - starty[] + 1), part_2_val)
        light_grid_2[startx[] + 1: endx[] + 1,
            starty[] + 1: endy[] + 1] += filler
        for j=1:size(light_grid_2)[1]
            for k=1:size(light_grid_2)[2]
                if light_grid_2[j, k] < 0
                    light_grid_2[j, k] = 0
                end
            end
        end

    end

    part_1 = sum(light_grid)
    @printf("Part 1: %d\n", part_1)
    part_2 = sum(light_grid_2)
    @printf("Part 2: %d\n", part_2)
end

main()
