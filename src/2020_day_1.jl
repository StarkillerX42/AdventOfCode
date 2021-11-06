println("Hello")
fp = open(joinpath(pwd(), "dat/2020_day_1.txt"), "r");
input_str = readlines(fp)
input = Array{Int64}(undef, length(input_str));
for j = 1:length(input_str)
    if input_str[j] != ""
        input[j] = parse(Int64, input_str[j])
    end
end

part_1 = NaN
for i = 1:length(input)
    for j = 1:length(input)
        if i != j
            if input[i] + input[j] == 2020
                global part_1 = input[i] * input[j]
            end
        end
    end
end

println("Part 1: ", part_1)

part_2 = NaN
for i = 1:length(input)
    for j = 1:length(input)
        for k = 1:length(input)
                if (input[i] + input[j] + input[k]) == 2020
                    global part_2 = input[i] * input[j] * input[k]
                end
        end
    end
end

println("Part 2: ", part_2)