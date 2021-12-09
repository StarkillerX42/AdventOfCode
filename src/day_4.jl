#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


function check_match(board, verbose)
    l_board = size(board)[1]
    match = false
    for i=1:l_board  # Horizontal line
        if all(board[i, :])
            match = true
        end
    end
    if verbose >= 2
        print(match, ", ")
    end
    for i=1:l_board  # Vertical line
        if all(board[:, i])
            match = true
        end
    end
    if verbose >= 2
        print(match, ", ")
    end

    # diag = true
    # for i = 1:l_board  # Top left to bottom right diagonal
    #     if !board[i, i]
    #         diag = false
    #     end
    # end
    # match = diag ? diag : match
    # if verbose >= 2
    #     print(match, ", ")
    # end

    # diag = true
    # for i = 1:l_board  # Bottom left to top right diagonal
    #     if !board[l_board - i + 1, i]
    #         diag = false
    #     end
    # end   
    # if verbose >= 2
    #     print(match, '\n')
    # end
    # match = diag ? diag : match
    return match
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
    numbers = [parse(Int, x) for x in split(inputs[1], ',')]

    boards = []
    newlines = 0
    board = Array{Int, 2}(undef, 5, 5)
    j = 1
    for i=2:length(inputs)
        if inputs[i] == ""
            board = Array{Int, 2}(undef, 5, 5)
            push!(boards, board)
            j = 1
        else
            board[j, :] = [parse(Int, x) for x in split(inputs[i])]
            j += 1
        end
    end
    println("N Boards: ", length(boards))
    n_boards = length(boards)
    l_board = 5
    w_board = 5

    matches = fill!(Array{Bool, 3}(undef, length(boards), 5, 5), false)
    part_1 = 0
    part_2 = 0
    part_2_filt = fill!(Array{Bool, 1}(undef, length(boards)), false)
    for (i, num) in enumerate(numbers)
        for j=1:n_boards
            for k=1:l_board
                for el=1:w_board
                    if boards[j][k, el] == num
                        matches[j, k, el] = true
                    end
                end
            end
            if !part_2_filt[j]
                if check_match(matches[j, :, :], args["verbose"])
                    if args["verbose"] >= 1
                        println("Found match at i=", i, " and j=", j)
                        println(matches[j, :, :])
                        println(boards[j])
                        println(sum(boards[j][!=(1).(matches[j, :, :])]))
                    end
                    if part_1 == 0
                        part_1 = sum(boards[j][!=(1).(matches[j, :, :])]) * num
                    end
                end
            end
            if !part_2_filt[j]
                if check_match(matches[j, :, :], args["verbose"])
                    part_2 = sum(boards[j][!=(1).(matches[j, :, :])]) * num
                    part_2_filt[j] = true
                end
            end
        end
    end

    @printf("Part 1: %d\n", part_1)
    @printf("Part 1: %d\n", part_2)
end


main()
