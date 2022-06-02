#include <string>
#include <string.h>
#include <iostream>
#include <sstream>
using namespace std;

string int_to_str(int val) {
    string str_val;
    stringstream str_strm;
    str_strm << val;
    str_strm >> str_val;
    return str_val;

}
bool check_six_char(int val, int verbose) {
    string str_val = to_string(val);
    if (verbose) {
        cout << "Integer length is " << str_val.length() << endl;
    }
    return str_val.length() == 6;
}


bool check_in_range(int val, int low, int high, int verbose) {
    return val >= low && val <= high;
}


bool check_pair(int val, int verbose) {
    string str_val = to_string(val);
    bool is_pair = false;
    char prev = 'a';
    for (int i=0; i<str_val.length(); i++) {
        if (str_val[i] == prev) {
            is_pair = true;
        }
        prev = str_val[i];
    }
    return is_pair;
}


bool check_always_increase(int val, int verbose) {
    bool is_increasing = true;
    string str_val = to_string(val);
    stringstream str_stream;
    int prev, next;
    str_stream << str_val[0];
    str_stream >> prev;
    for (int i=1; i<str_val.length(); i++) {

        stringstream str_stream;
        str_stream << str_val[i];
        str_stream >> next;
        if (verbose) {
            cout << str_val[i] << " " << prev << " " << next << " " << is_increasing << endl;
        }
        if (!(prev <= next)) {
            is_increasing = false;
        }
        prev = next;
    }
    return is_increasing;
}


bool check_pair_2(int val, int verbose) {
    string str_val = to_string(val);
    bool is_pair = false;
    stringstream match;
    match << "a";
    int len;
    for (int i=0; i<str_val.length(); i++) {
        len = match.str().length();
        if (str_val[i] == match.str().at(len - 1)) {
            match << str_val[i];
        }
        else {
            if (match.str().length() == 2) {
                is_pair = true;
            }
            match.str("");
            match << str_val[i];
        }
    }
    if (match.str().length() == 2) {
        is_pair = true;
    }
    return is_pair;
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

    string range;
    if (!test) {
        range = "158126-624574";
    } else {
        range = "";
    }

    int low;
    int high;
    sscanf(range.c_str(), "%i-%i", &low, &high);

    if (verbose) {
        std::cout << "Range: " << range << " Low: " << low << " High: " << high << endl;
    }


    cout << "Six character: " << check_six_char(low, false) << endl;
    cout << "In range: " << check_in_range(low, low, high, verbose) << endl;
    cout << "Found pair: " << check_pair(112345, verbose) << endl;
    cout << "Increasing: " << check_always_increase(112345, false) << endl; 
    cout << "Found pair 2 Good: " << check_pair_2(111122, verbose) << endl;
    cout << "Found pair 2 Bad: " << check_pair_2(111123, verbose) << endl;

    int part_1 = 0;
    int part_2 = 0;
    for (int i=low; i <= high; i++) {
        if (check_six_char(i, false) && check_in_range(i, low, high, false)
            && check_always_increase(i, false))
            {
                if (check_pair(i, false)) {
                    part_1++;
                }
                if (check_pair_2(i, false)) {
                    part_2++;
                }
            }
    }

    cout << "Part 1: " << part_1 << endl;
    cout << "Part 2: " << part_2 << endl;

    return 0;
}
