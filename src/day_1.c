#include <stdio.h>

int main() {
    FILE* fp = fopen("dat/day_1.txt", "r");
    bool verbose = true;
    int i = 0;
    int j = 0;
    int k;
    int part_1 = 0;
    int part_2 = 0;
    int rem;
    fscanf(fp, "%d", &i);
    while (! feof (fp) && (j < 1000)) {
        if (verbose) {
            printf("%d %d %d\n", j, i, i / 3 - 2);
        }

        rem = i / 3 - 2;
        k = 0;
        while (rem > 0 && k < 1000) {
                if (verbose) {
                    printf("    %d %d\n", part_2, rem);
                }
                part_2 += rem;
                rem = rem / 3 - 2;
                k++;
            }
        part_1 += i / 3 - 2;
        fscanf(fp, "%d", &i);
        j++;
    }
    printf("Part 1 Fuel: %d\n", part_1);

    j = 0;
    while (rem > 0 && j < 1000) {
        if (verbose) {
            printf("%d %d\n", part_2, rem);
        }
        part_2 += rem;
        rem = rem / 3 - 2;
        j++;
    }
    printf("Part 2 Fuel: %d\n", part_2);
    return 0;
}