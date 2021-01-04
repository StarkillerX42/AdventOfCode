#include <fstream>
#include <iostream>
#include <string>

using namespace std;


bool verbose = true;


int str2int(basic_string<char> str){
    int len = str.length();
    int i, result=0;
    for(i=0; i<len; i++){

        result = result * 10 + ( str[i] - '0' );

    }
    return result;
}


int main() {
    string file_path = "dat/day_3.txt";
    ifstream in_file(file_path);
    if (!in_file.is_open()) {
        cout << "File cannot be opened:" << file_path << endl;
    }
    else {
        while (!in_file.eof()) {
            string line;
            getline(in_file, line);
            int i, line_len = 0;
            for (i=0; i < line.size(); i++) {
                if (line[i] == ',') {
                    line_len++;
                }
            }
            // Populate instructions and distances
            char instructions[line_len];
            int distances[line_len];
            int top, while_count = 0;
            i = 0;
            while (i <= line_len && while_count < 1000) {
                top = line.find_first_of(',');
                if (top <= line.length()) {
                    instructions[i] = line[0];
                    distances[i] = str2int(line.substr(1, top-1));
                    line = line.substr(top + 1, line.length());
                    i++;
                }

                while_count++;
            }
            int pos[2] = {0, 0};
            for (i=0; i < sizeof(distances)/sizeof(distances[0]); i++) {
                if (instructions[i] == 'U') {
                    pos[0] += distances[i];
                }
                else if (instructions[i] == 'D') {
                    pos[0] -= distances[i];
                }
                else if  (instructions[i] == 'L') {
                    pos[1] -= distances[i];
                }
                else if (instructions[i] == 'R') {
                    pos[1] += distances[i];
                }
                cout << pos[0] << ", " << pos[1] << endl;

            }
        }
    }

    return 0;
}
