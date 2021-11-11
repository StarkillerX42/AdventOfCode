#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON


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


function handler(json_obj)
    total_1 = 0
    total_2 = 0
    null = 0
    if typeof(json_obj) == Dict{String, Any}
        if "red" in values(json_obj)
            for key in keys(json_obj)
                tmp,  null = handler(json_obj[key])
                total_1 += tmp
            end
        else
            for key in keys(json_obj)
                null, tmp = handler(json_obj[key])
                total_1 += null
                total_2 += tmp
            end
        end
    elseif typeof(json_obj) == Array{Any, 1}
        for val in json_obj
            tmp, null = handler(val)
            total_1 += tmp
            total_2 += null
        end
    elseif typeof(json_obj) == Int
        total_1 += json_obj
        total_2 += json_obj
    elseif typeof(json_obj) == String
    else
        throw(error("Could not understand input of type ", typeof(json_obj)))
    end
    return total_1, total_2
end


function main()
    args = parse_cmdline()
    path_parts = split(PROGRAM_FILE, "/")
    day = split(split(path_parts[length(path_parts)], "_")[2], ".")[1]
    project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
    if !args["test"]
        data_path = joinpath(project_dir, "dat/day_" * day * ".json")
    else
        data_path = joinpath(project_dir, "dat/day_" * day * "_test.json")
    end
    data = String(read(open(data_path, "r")))
    js = JSON.parse(data)

    part_1, part_2 = handler(js)

    @printf("Part 1: %d\n", part_1)
    @printf("Part 2: %d\n", part_2)
end

main()
