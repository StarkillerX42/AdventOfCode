#include <iostream>
#include <vector>
using namespace std;


void modify_vector(vector <int> &x, int in_val){
    cout << "x is at " << &x << endl;
    cout << x[0] << endl;
    cout << in_val << endl;
    x[0] = in_val;
}


int main() {
    vector <int> inputs;
    inputs.push_back(1);
    inputs.push_back(2);
    cout << "inputs[0]= " << inputs[0] << endl;
    cout << "inputs is at " << &inputs << endl;
    cout << "inputs[0] is at " << &inputs[0] << endl;
    modify_vector(inputs, 10);
    cout << "inputs[0]= " << inputs[0] << endl;
    cout << "inputs.at(0)= " << inputs.at(0) << endl;
    cout << &inputs << endl;
    int c_arr[2] = {1, 0};
    cout << "c_arr is at " << &c_arr << endl;

    cout << "c_arr[0] is at" << &c_arr[0] << endl;
    int x = 1;
    int * y;
    y = &x;
    // int z = take_pointer(&x);
    cout << x << ", " << &x << endl;
    cout << y << ", " << &y << endl;
    // cout << z << ", " << &z << endl;

    return 0;
}