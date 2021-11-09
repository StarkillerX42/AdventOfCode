#!/usr/bin/env julia
using Printf
using ArgParse


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
    
    fp = open(data_path, "r")
    santas_list = readlines(fp)
    part_1 = 0
    literals = 0
    memories = 0
    reencoded = 0
    for name in santas_list
        i = 1
        characters = 0
        reenc = 0
        while i <= length(name)
            if name[i] == '"'
                i += 1
                reenc += 3
            elseif name[i] == '\\'
                i += 1
                reenc += 2
                if name[i] == '"'
                    i += 1
                    characters += 1
                    reenc += 2
                elseif name[i] == '\\'
                    i += 1
                    characters += 1
                    reenc += 2
                elseif name[i] == 'x'
                    i += 3
                    characters += 1
                    reenc += 3
                else
                    @printf("Could not process escape character %c in %s", name[i], name)
                end
            else
                i += 1
                characters += 1
                reenc += 1
            end
        end
        if args["verbose"] >= 1
            println("String: ", name, " length: ", i - 1, " characters: ", characters)
        end
        literals += i - 1
        memories += characters
        reencoded += reenc
    end
    part_1 = literals - memories
    part_2 = reencoded - literals
    @printf("Part 1: %d\n", part_1)
    @printf("Part 1: %d\n", part_2)
end


main()
