#include <stdio.h>
#include <string.h>
#include <math.h>
#include <sys/param.h>
#include <stdlib.h>

int verbose = 1;


struct Path {
    int id;
    int n_steps;
    char directions[5000];
    int distances[5000];
    int positions[5000][2];
};


void get_instructions(int line_no, char fname[256], struct Path *path){
    FILE *fp = fopen(fname, "r");
    char line[5000];
    int line_iter = 0;
    while(line_iter <= line_no) {
        fscanf(fp, "%s\n", line);
        // printf("%s\n", line);
        line_iter++;
        // printf("Next line\n");
    }
    int n_steps = 1;
    int i;
    for(i=0; i<strlen(line); i++) {
        // printf("%c\n", line[i]);
        if (line[i] == ',') {
            n_steps++;
            // printf("\n");
        }
    }
    printf("Player %d takes %d steps\n", line_no, n_steps);
    path->n_steps = n_steps;
    char dirs[n_steps + 1];
    int positions[n_steps + 1][2];
    char direction;
    int distance;
    char test;
    i = 0;
    char *step = strtok(line, ",");
    positions[0][0] = 0;
    positions[0][1] = 0;
    while (step) {
        // printf("%d: %d, %d\n", i, positions[i][0], positions[i][1]);
        sscanf(step, "%c%d,", &direction, &distance);
        // printf("%c %d\n", direction, distance);

        switch (direction) {
            case 'U':
                positions[i+1][0] = positions[i][0];
                positions[i+1][1] = positions[i][1] + distance;
                // printf("Up: %d, %d\n", positions[i+1][0], positions[i+1][1]);
                break;
            case 'D':
                positions[i+1][0] = positions[i][0];
                positions[i+1][1] = positions[i][1] - distance;
                // printf("Down: %d, %d\n", positions[i+1][0], positions[i+1][1]);
                break;
            case 'L':
                positions[i+1][1] = positions[i][1];
                positions[i+1][0] = positions[i][0] - distance;
                // printf("Left: %d, %d\n", positions[i+1][0], positions[i+1][1]);
                break;
            case 'R':
                positions[i+1][1] = positions[i][1];
                positions[i+1][0] = positions[i][0] + distance;
                // printf("Right: %d, %d\n", positions[i+1][0], positions[i+1][1]);
                break;
            default:
                break;
        }
        dirs[i] = direction;
        i++;
        step = strtok(NULL, ",");
    }
    // printf("%s\n", line);
    // for (i=0; i<n_steps; i++) {
        // printf("%c\n", dirs[i]);
    // }
    strcpy(path->directions, dirs);
    for(i=0; i<n_steps+1;i++) {
        path->positions[i][0] = positions[i][0];
        path->positions[i][1] = positions[i][1];
    }
    // path->positions = positions;
}


int manhattan(int a, int b) {
    int sum = abs(a) + abs(b);
    return sum;
}


int check_crossing(int a0[2], int a1[2], int b0[2], int b1[2]) {
    /*This is also called a bounding box check*/
    
    int b_x_crosses_a = ((a0[0] <= b0[0]) && (a0[0] >= b1[0])) || ((a0[0] >= b0[0] && a0[0] <= b1[0]));
    int b_y_in_a = ((b0[1] <= a0[1]) && (b0[1] >= a1[1])) || ((b0[1] >= a0[1]) && (b0[1] <= a1[1]));
    int a_vert_crossed = b_x_crosses_a && b_y_in_a;
    int a_x_crosses_b = ((b0[0] <= a0[0]) && (b0[0] >= a1[0])) || ((b0[0] >= a0[0] && b0[0] <= a1[0]));
    int a_y_in_b = ((a0[1] <= b0[1]) && (a0[1] >= b1[1])) || ((a0[1] >= b0[1]) && (a0[1] <= b1[1]));
    int a_horiz_crossed = a_x_crosses_b && a_y_in_b;
    if (verbose >= 2) {
        printf("Positions are cross check:\n\t (%d, %d)->(%d, %d)\n\t (%d, %d)->(%d, %d)\n",
            a0[0], a0[1], a1[0], a1[1],
            b0[0], b0[1], b1[0], b1[1]);
        printf("a_horiz_crossed = %d, a_vert_crossed = %d\n", a_horiz_crossed, a_vert_crossed);
    }
    return a_vert_crossed || a_horiz_crossed;
}


void print_full_path(struct Path path) {
    int i;
    for (i=0; i<=path.n_steps; i++) {
        printf("%d, %d\n", path.positions[i][0], path.positions[i][1]);
    }
}


int find_closest_crossing(struct Path path1, struct Path path2) {
    int closest_hit = 10000000;
    int i, j;
    for (i=0; i<path2.n_steps;i++) {
        if (verbose >= 2) {
            printf("i: %d\n", i);
        }
        for (j=0; j<path1.n_steps; j++) {
            if (verbose >= 2) {
                printf("    j: %d\n", j);
            }
            if (!((path2.positions[j][0] == 0) && (path2.positions[j][1] == 0))) {
                if ((path2.directions[j] == 'U' || path2.directions[j] == 'D')
                    && (path1.directions[i] == 'L' || path1.directions[i] == 'R')) {
                    if (check_crossing(path1.positions[j],
                        path1.positions[j+1], path2.positions[i],
                        path2.positions[i+1])) {
                        // if (verbose) {
                            printf("Collision at %d, %d\n", path2.positions[i][0], path1.positions[j][1]);
                        // }
                        closest_hit = MIN(closest_hit, manhattan(path2.positions[i][0], path1.positions[j][1]));
                    }
                }
                else if ((path2.directions[j] == 'L' || path2.directions[j] == 'R')
                    && (path1.directions[i] == 'U' || path1.directions[j])) {
                    if (check_crossing(path1.positions[j],
                        path1.positions[j+1], path2.positions[i], path2.positions[i+1])) {
                        // if (verbose) {
                            printf("Collision at %d, %d\n", path1.positions[j][0], path2.positions[i][1]);
                        // }
                        closest_hit = MIN(closest_hit, manhattan(path1.positions[j][0], path2.positions[i][1]));
                    }
                }
            }
            else {
                if (verbose >= 2) {
                    printf("Skipping because it involves 0, 0\n");
                }
            }
        }
    }
    printf("Closest crossing: %d\n", closest_hit);
    return closest_hit;
}


int main() {
    printf("Verbosity: %d\n", verbose);
    char file_path[256] = "dat/day_3.txt";
    struct Path path1;
    struct Path path2;
    path1.id = 0;
    path2.id = 1;
    get_instructions(path1.id, file_path, &path1);
    get_instructions(path2.id, file_path, &path2);
    // print_full_path(path1);
    int lowest = find_closest_crossing(path1, path2);
    
    return 0;
}
