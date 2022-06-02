#include <string>
#include <string.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <fstream>
#include <algorithm>
using namespace std;


void draw_image(vector <vector <int>> image) {
    for (auto const &row: image) {
        for (auto const &value: row) {
            if (value) {
            cout << "\u2B1C";
            } else {
                cout << "\u2B1B";
            }
        }
        cout << endl;
    }
}


int main(int argc, char *argv[]) { 
    int verbose=0;
    int test=0;
    char **ptr;
    for (ptr=argv; *ptr !=NULL ; ptr++) {

        if (!strcmp(*ptr, "-v")){
            verbose++;
        }
        if (!strcmp(*ptr, "-t")){
            test = 1;
        }
    }
    if (verbose >= 1) {
        cout << "Verbosity: " << verbose << endl;
        cout <<"Testing: " << test << endl;
    }

    string file_path;
    int nx, ny;
    if (test) {
        file_path = "dat/day_8_test.txt";
        nx = 2;
        ny = 2;
    } else {
        file_path = "dat/day_8.txt";
        nx = 25;
        ny = 6;
    }


    int next_int;
    string image_str;
    string line;
    stringstream sline;
    ifstream inputs(file_path);
    if (inputs.is_open()) {
        while (inputs.good()){
            getline(inputs, line);
            if (line.size() > 0) {
                image_str = line;
            }
        }
    }
    int n_lyr = image_str.size() / nx / ny;
    if (verbose >= 2) {
        cout << image_str << endl;
    }
    if (verbose) {
        cout << "Image is " << image_str.size() << " long with " << n_lyr;
        cout << " layer shape " << nx << "x" << ny << endl;
    }

    vector <int> flat_image;
    int x;
    int zero_count = 0;
    vector <int> zero_counts;
    stringstream ss;
    int min_zeros=999;
    for (int i=0; i<image_str.size(); i++) {
        if (i % (nx * ny) == 0 && i != 0) {
            zero_counts.push_back(zero_count);
            min_zeros = min(min_zeros, zero_count);
            zero_count = 0;
        }
        x = (int)(image_str[i]) - '0';
        // cout << x << " : ";
        if (x == 0) {
            // cout << "+ : ";
            zero_count++;
        }
        flat_image.push_back(x);
    }
    zero_counts.push_back(zero_count);
    min_zeros = min(min_zeros, zero_count);

    int row_low, row_high;
    for (int i=0; i<zero_counts.size(); i++) {
        if (zero_counts.at(i) == min_zeros) {
            row_low = i * nx * ny;
            row_high = (i + 1) * nx * ny;
            if (verbose) {
                cout << "Layer " << i + 1 << " has the least zeros" << endl;
                cout << "Counting from " << row_low << " to " << row_high << endl;
            }

        }
    }

    int n_ones = 0, n_twos = 0;
    for (int i=row_low; i < row_high; i++) {
        switch (flat_image.at(i)) {
            case 1: 
                n_ones++;
                break;
            case 2:
                n_twos++;
                break;
            default:
                break;
        }
    }
    int part_1 = n_ones * n_twos;
    cout << "Part 1: " << part_1 << endl;
    vector <vector <int>> image;
    int j = 0, k = 0;
    for (int i=0; i < flat_image.size(); i++) {
        j =  i % nx; 
        k = (i / nx) % ny;
        if (verbose >= 2) {
            cout << i << ", " << j << ", " << k << "->" << flat_image.at(i) << endl;
        }
        if (i < nx * ny) {
            if (j == 0) {
                image.push_back({});
            }
            image[k].push_back(flat_image.at(i));
        } else {
           if (image[k][j] == 2) {
               image[k][j] = flat_image.at(i);
           }
        }
        if (i == nx * ny - 1) {
            draw_image(image);
        }
    }
    cout << "Part 2:" << endl;
    draw_image(image);
}