#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


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
    n_bits = length(inputs)
    l_bits = length(inputs[1])
    bits = Array{Bool, 2}(undef, n_bits, l_bits)
    for (i, line) in enumerate(inputs)
        for (j, ch) in enumerate(line)
            bits[i, j] = parse(Bool, ch)
        end
    end

    gamma_arr = Array{Bool, 1}(undef, l_bits)
    for (i, _) in enumerate(bits[1, :])
        sm = sum(bits[:, i])
        gamma_arr[i] = sm > n_bits // 2
    end

    bcaster = Array{Int, 1}(undef, l_bits)
    for i=l_bits:-1:1
        bcaster[i] = 2^(l_bits - i)
    end

    epsilon = .!gamma_arr

    part_1 = sum(bcaster[epsilon]) * sum(bcaster[gamma_arr])

    @printf("Part 1: %d\n", part_1)

    # Find Oxygen

    oxygen_filt = fill!(Array{Bool, 1}(undef, n_bits), true)
    for i=1:l_bits
        # subset = bits[oxygen_filt, :]
        bcount = sum(bits[oxygen_filt, :][:, i])
        winner = bcount >= length(bits[oxygen_filt, i]) // 2
        for j=1:n_bits
            oxygen_filt[j] = oxygen_filt[j] ? bits[j, i] == winner : oxygen_filt[j]
        end
        if sum(oxygen_filt) == 1
            break
        end
    end

    co2_filt = fill!(Array{Bool, 1}(undef, n_bits), true)
    for i=1:l_bits
        # subset = bits[co2_filt, :]
        bcount = sum(bits[co2_filt, :][:, i])
        winner = bcount < length(bits[co2_filt, i]) // 2
        for j=1:n_bits
            co2_filt[j] = co2_filt[j] ? bits[j, i] == winner : co2_filt[j]
        end

        if sum(co2_filt) == 1
            break
        end
    end

    oxygen = Array{Bool, 1}(undef, l_bits)
    co2 = Array{Bool, 1}(undef, l_bits)
    for i=1:l_bits
        oxygen[i] = bits[oxygen_filt, i][1]
        co2[i] = bits[co2_filt, i][1]
    end

    part_2 = sum(bcaster[oxygen]) * sum(bcaster[co2])
    @printf("Part 2: %d\n", part_2)

end


main()
