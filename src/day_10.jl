#!/usr/bin/env julia

using Printf
using ArgParse
using Dates


function look_and_say(in::String)
    counter = 1
    previous = in[1]
    out = ""
    for i=2:length(in)
        if in[i] == previous
            counter += 1
        else
            out *= string(counter) * previous
            counter = 1
        end
        previous = in[i]
    end
    out *= string(counter) * previous
    return out
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
        "count"
            arg_type=Int
            required = true
    end
    return parse_args(parser)
end


function main()
    args = parse_cmdline()
    path_parts = split(PROGRAM_FILE, "/")
    day = split(split(path_parts[length(path_parts)], "_")[2], ".")[1]
    project_dir = dirname(dirname(abspath(PROGRAM_FILE)))

    if args["test"]
        in = "1"
    else
        in = "3113322113"
    end
    now = Dates.now()
    for i in range(1, step=1, length=args["count"])
        new = Dates.now()
        if args["verbose"] >= 1
            println("Step ", i, ", Previous loop = ", Dates.canonicalize(new - now))
            println("Length is ", length(in))
        end
        now = new
        in = look_and_say(in)
        # @printf("%140s\n", in)
    end

    @printf("Part 1: %s\n", length(in))
end


main()
