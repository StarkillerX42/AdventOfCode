#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


function get_quality(ingredients_mat, ns, verbose::Int=0)
    quals = ingredients_mat * ns
    if verbose >= 1
        println("Qualities: ", quals)
    end
    if any(i -> i < 0, quals)
        return false, prod(quals)
    else
        return true, prod(quals)
    end
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
    ingredients = Matrix{Int}(undef, 4, length(inputs))
    names = Array{String, 1}(undef, length(inputs))
    cals = Array{Int, 1}(undef, length(inputs))
    # ingredients = Dict{String, Dict}()

    for (i, line) in enumerate(inputs)
        words = split(line)
        name = words[1][1:end-1]
        names[i] = name
        for j = 1:4
            ingredients[j, i] = parse(Int, words[j*2+1][1:end-1])
        end
        cals[i] = parse(Int, words[11])
    end
    if args["verbose"] >= 1
        println(ingredients)
    end
    guess = Vector([20, 25, 25, 30])
    # guess = Vector([97, 1, 1, 1])

    count = 0
    while count < 1000000
        is_good, best = get_quality(ingredients, guess)
        i_save = 0
        j_save = 0
        for i = 1:4
            for j= 1:4
                if i != j && guess[i] > 1
                    test = copy(guess)
                    test[i] -= 1
                    test[j] += 1
                    is_good, test_score = get_quality(ingredients, test, args["verbose"])
                    if test_score == 0
                        println("Error: Stuck at zero with guess ", test)
                    end
                    if test_score > 0 && !is_good
                        test_score = -test_score
                    end
                    if test_score > best
                        if args["verbose"] >= 2
                            println("New best guess: ", test)
                        end
                        best = max(best, test_score)
                        i_save = i
                        j_save = j
                    end
                    if test_score > best && !is_good
                        println("Negative value encountered: ", test)
                    end
                end
            end
        end
        count += 1
        if i_save == 0 && j_save == 0
            break
        else
            guess[i_save] -= 1
            guess[j_save] += 1
        end
    end
    is_good, part_1 = get_quality(ingredients, guess, args["verbose"])

    if is_good
        @printf("Part 1: %d\nSolved in %d loops\n", part_1, count)
    else
        @printf("Bad Part 1: %d\nSolved in %d loops\n", part_1, count)
    end

    best = 0
    best_guess = [0, 0, 0, 0]
    for i = ProgressBar(1:100)
        for j = 1:100
            for k = 1:100
                for m = 1:100
                    guess = [i, j, k, m]
                    if sum(guess) == 100 && transpose(guess) * cals == 500
                        
                        is_good, test_score = get_quality(ingredients, guess, args["verbose"])
                        if test_score > 0 && !is_good
                            test_score = -test_score
                        end
                        # if args["verbose"] >= 1
                            # println("Testing ", guess, " score: ", test_score, " is_good: ", is_good)
                        # end
                        if test_score > best
                            if args["verbose"] >= 2
                                println("New best guess: ", test)
                            end
                            best_guess = copy(guess)
                            best = max(best, test_score)
                        end
                    end
                end
            end
        end
    end
    is_good, part_2 = get_quality(ingredients, best_guess, args["verbose"])

    if is_good
        @printf("Part 2: %d\n", part_2)
    else
        @printf("Bad Part 2: %d\n", part_2)
    end

    return 0
end

main()
