#define EXPORT __declspec(dllexport)
#include <iostream>
#include <algorithm>
#include <string>
#include <cstring>
#include <cstdio>
#include <map>
#include <queue>
#include <ctime>
#include <set>
using namespace std;

int global_cols;
string solution;
string end_state;
string start_state;
int	length;
int flag = 0;
const char dirname[4] = { 'U', 'D', 'R', 'L' };

struct state
{
	int floor;
	string start;
	string path;
	int ppos;
};
bool cleared(const string& cur_start)
{
	for (int i = 0; i < cur_start.size(); ++i) {
		if (cur_start[i] == '$'&&end_state[i] == ' ')
			return false;
	}
	return true;
}

void dfs(state& initial, int index, int dir[], queue<state> &q, set<string> &visited) {
	if (flag)
		return;
	string cur_start = initial.start;
	string cur_path = initial.path;
	int cur_ppos = initial.ppos;
	int cur_floor = initial.floor;
	if (cleared(cur_start)) {
		solution = initial.path;
		flag = 1;
		return;
	}

	for (int d = index; d < 4; ++d) {
		state new_state;
		string temp_start = cur_start;
		int cpos = cur_ppos + dir[d];
		int npos = cpos + dir[d];
		if (cpos<0 || npos<0 || cpos>length || npos>length)
			continue;
		if (temp_start[cpos] == '$'&&temp_start[npos] == ' ') {
			temp_start[cur_ppos] = ' ';
			temp_start[cpos] = '@';
			temp_start[npos] = '$';
			if (visited.find(temp_start) == visited.end()) {
				visited.insert(temp_start);
				new_state.floor = cur_floor;
				new_state.ppos = cpos;
				new_state.start = temp_start;
				new_state.path = cur_path + dirname[d];
				if (new_state.path.size()>cur_floor) {
					new_state.floor *= 2;
					//                    cout<<new_state.path<<"\n";
					//                    cout<<new_state.floor <<"\n";
					q.push(new_state);
					continue;
				}
				dfs(new_state, 0, dir, q, visited);
			}
		}
		else if (temp_start[cpos] == ' ') {
			temp_start[cur_ppos] = ' ';
			temp_start[cpos] = '@';
			if (visited.find(temp_start) == visited.end()) {
				visited.insert(temp_start);
				new_state.floor = cur_floor;
				new_state.ppos = cpos;
				new_state.start = temp_start;
				new_state.path = cur_path + dirname[d];
				if (new_state.path.size()>cur_floor) {
					new_state.floor *= 2;
					//                    cout<<new_state.path<<"\n";
					//                    cout<<new_state.floor <<"\n";
					q.push(new_state);
					continue;
				}
				dfs(new_state, 0, dir, q, visited);
			}
		}
	}
}


void Start_DFS(string input_file, int cols) {
	state initial;
	global_cols = cols;
	int dir[4] = { -1 * global_cols, global_cols, 1, -1 };
	start_state = "";
	end_state = "";
	flag = 0;
	for (int i = 0; i < input_file.size(); i++) {
		if (input_file[i] == '.') {
			start_state += ' ';
			end_state += '.';
		}
		else if (input_file[i] == '*') {
			start_state += '$';
			end_state += '.';
		}
		else if (input_file[i] == '+') {
			start_state += '@';
			end_state += '.';
		}
		else {
			start_state += input_file[i];
			end_state += ' ';
		}
		if (start_state[i] == '@')
			initial.ppos = i;
	}
	initial.start = start_state;
	initial.path = "";
	initial.floor = 2;
	queue<state> q;
	set<string> visited;
	visited.insert(start_state);
	q.push(initial);
	while (!q.empty()) {
		state cur = q.front();
		q.pop();
		//        cout<<cur.path<<"\n";
		dfs(cur, 0, dir, q, visited);
		if (flag)
			break;
	}
}



extern "C" {
	EXPORT size_t Dfs(char* input_file, int len, int cols, char* return_solution) {
		string s;
		length = len;
		for (int i = 0; i < len * 2; i += 2)
			s.push_back(input_file[i]);
		//clock_t t = clock();
		Start_DFS(s, cols);
		//t = clock() - t;
		//cout << "outer_time" << 1.0*t / CLOCKS_PER_SEC << "\n";
		return solution.size();
	}


	EXPORT void Get_solution(char* return_solution) {
		for (int i = 0; i < solution.size(); i++)
			if (return_solution[i * 2] != '\0')
				return_solution[i * 2] = solution[i];
	}
}
