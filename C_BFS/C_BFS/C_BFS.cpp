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

struct state
{
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




void bfs(state& initial)
{
	int dir[4] = { -1 * global_cols, global_cols, 1, -1 };
	const char dirname[4] = { 'U', 'D', 'R', 'L' };
	set<string> prev;
	queue<state> q;
	string end_path;
	//clock_t t = clock();
	prev.insert(start_state);
	q.push(initial);
	while (!q.empty())
	{
		string cur_start = q.front().start;
		string cur_path = q.front().path;
		int cur_ppos = q.front().ppos;
		q.pop();
		if (cleared(cur_start))
		{
			end_path = cur_path;
			break;
		}
		for (int d = 0; d < 4; d++)
		{
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
				if (prev.find(temp_start) == prev.end()) {
					prev.insert(temp_start);
					new_state.ppos = cpos;
					new_state.start = temp_start;
					new_state.path = cur_path + dirname[d];
					q.push(new_state);
				}
			}
			else if (temp_start[cpos] == ' ') {
				temp_start[cur_ppos] = ' ';
				temp_start[cpos] = '@';
				if (prev.find(temp_start) == prev.end()) {
					prev.insert(temp_start);
					new_state.ppos = cpos;
					new_state.start = temp_start;
					new_state.path = cur_path + dirname[d];
					q.push(new_state);
				}
			}
		}
	}
	//t = clock() - t;
	//cout << "main_time" << 1.0*t / CLOCKS_PER_SEC << "\n";
	//cout << end_path << "\n";
	solution = end_path;
	
}




void Start_BFS(string input_file, int cols) {
	state initial;
	global_cols = cols;
	start_state = "";
	end_state = "";
	for (int i = 0; i < input_file.size(); i++) {
		if (input_file[i] == '.') {
			start_state += ' ';
			end_state += '.';
		}
		else if(input_file[i] == '*'){
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
	bfs(initial);
}

extern "C" {
	EXPORT size_t Bfs(char* input_file, int len, int cols, char* return_solution) {
		string s;
		length = len;
		for (int i = 0; i < len * 2; i += 2)
			s.push_back(input_file[i]);
		//clock_t t = clock();
		Start_BFS(s, cols);
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