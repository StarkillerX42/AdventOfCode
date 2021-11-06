#!/usr/bin/env julia
using Printf

project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
data_file = joinpath(project_dir, "dat/day_3.txt")

fp = open(data_file, "r")
dirs = readline(fp)
@printf("There are %d stops\n", length(dirs))

function generate_locations(directions)
    locations = Array{Int, 2}(undef, length(directions) + 1, 2)
    locations[1, :] = [0, 0]
    for i=1:length(directions)
        # Populdates locations[i + 1]
        if directions[i] == '>'
            locations[i + 1, 1] = locations[i, 1] + 1
            locations[i + 1, 2] = locations[i, 2]
        elseif directions[i] == '<'
            locations[i + 1, 1] = locations[i, 1] - 1
            locations[i + 1, 2] = locations[i, 2]
        elseif directions[i] == '^'
            locations[i + 1, 1] = locations[i, 1]
            locations[i + 1, 2] = locations[i, 2] + 1
        elseif directions[i] == 'v'
            locations[i + 1, 1] = locations[i, 1]
            locations[i + 1, 2] = locations[i, 2] - 1
        else
            @printf("Unparsible direction %s\n", directions[i])
        end
    end
    return locations
end

function count_unique_locations(locations)
    unique_locations = 0
    for i=1:length(locations[:, 1])
        overlap = false
        # Checks if locations[i + 1] is unique
        for j = 1:i - 1
            if locations[j, :] == locations[i, :]
                overlap = true
            end
        end
        if !overlap
            unique_locations += 1
        end
        # print(directions[i], " ", locations[i, :], ", ")  # Warning: death ahead
    end
    return unique_locations
end

locs = generate_locations(dirs)
houses_covered = count_unique_locations(locs)

@printf("Part 1: %d\n", houses_covered)
santa_locs = generate_locations(dirs[1:2:length(dirs)])
bot_locs = generate_locations(dirs[2:2:length(dirs)])
part_2_locs = vcat(santa_locs, bot_locs)
part_2_houses = count_unique_locations(part_2_locs)
@printf("Part 2: %d\n", part_2_houses)
