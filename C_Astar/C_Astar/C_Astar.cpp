#define EXPORT __declspec(dllexport)
#include <iostream>
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
string input_file_gol;
string end_state;
string start_state;
string temp_state;
int	length;
const char dirname[4] = { 'U', 'D', 'R', 'L' };
const int oo = 0x3f3f;
struct state
{
	string start;
	string path;
	int ppos;
};

struct anode
{
	int cost;
	int est;
	state s;
};

struct anode_cmp
{
	bool operator() (const anode& a, const anode& b) const
	{
		return (a.cost + a.est) > (b.cost + b.est);
	}
};

struct state_cmp
{
	bool operator() (const state& a, const state& b) const
	{
		if (a.ppos != b.ppos)
			return a.ppos < b.ppos;

		if (a.path != b.path)
			return a.path < b.path;

		return false;
	}
};

bool cleared(const string& cur_start)
{
	for (int i = 0; i < cur_start.size(); ++i) {
		if (cur_start[i] == '$'&&end_state[i] == ' ')
			return false;
	}
	return true;
}

void pre(string temp_state, int *&dist)
{
	int dir[4] = { -1 * global_cols, global_cols, 1, -1 };
	queue<int> q;
	for (int i = 0; i < length; i++)
		dist[i] = -1;
	for (int i = 0; i < length; i++)
	{
		if (input_file_gol[i] == '.') {
			dist[i] = 0;
			q.push(i);
		}
	}
	while (!q.empty())
	{
		int cur_ppos = q.front();
		q.pop();
		for (int d : dir)
		{
			int cpos = cur_ppos + d;
			int npos = cpos + d;
			if (cpos<0 || npos<0 || cpos>length || npos>length)
				continue;
			if (temp_state[cpos] == ' ' && temp_state[npos] == ' '  && dist[cpos] == -1)
			{
				dist[cpos] = 1 + dist[cur_ppos];
				q.push(cpos);
			}
		}
	}
}

int estimate(string cur_state, int *&dist) {
	int est = 0;
	for (int i = 0; i < length; i++) {
		if (cur_state[i] == '$') {
			if (dist[i] == -1)
				return oo;
			est += dist[i];
		}
	}
	return est;
}

void astar(state& initial, int *&dist) {
	int dir[4] = { -1 * global_cols, global_cols, 1, -1 };
	set<string> prev;
	priority_queue<anode, vector<anode>, anode_cmp> q;
	map<state, int, state_cmp> record;
	string end_path;

	anode initial_a;
	initial_a.cost = 0;                               // 代价
	initial_a.est = estimate(initial.start, dist);     // 评估代价
	initial_a.s = initial;

	prev.insert(start_state);
	record[initial] = 0;
	q.push(initial_a);
	while (!q.empty()) {
		anode cur = q.top();
		q.pop();
		if (cur.cost > record[cur.s])
			continue;
		string cur_start = cur.s.start;
		string cur_path = cur.s.path;
		int cur_ppos = cur.s.ppos;
		if (cleared(cur_start)) {
			end_path = cur_path;
			break;
		}
		for (int d = 0; d < 4; d++) {
			state new_state;
			string temp_start = cur_start;
			int cpos = cur_ppos + dir[d];
			int npos = cpos + dir[d];
			if (cpos < 0 || npos < 0 || cpos > length || npos > length)
				continue;
			if (temp_start[cpos] == '$' && temp_start[npos] == ' ') {
				temp_start[cur_ppos] = ' ';
				temp_start[cpos] = '@';
				temp_start[npos] = '$';
				if (prev.find(temp_start) == prev.end()) {
					prev.insert(temp_start);
					new_state.ppos = cpos;
					new_state.start = temp_start;
					new_state.path = cur_path + dirname[d];
					if (!record.count(new_state) || record[new_state] > cur.cost + 1) {
						anode next_a;
						next_a.s = new_state;
						next_a.cost = record[new_state] = cur.cost + 1;
						next_a.est = estimate(new_state.start, dist);
						if (next_a.est < oo)
							q.push(next_a);
					}
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
					if (!record.count(new_state) || record[new_state] > cur.cost + 1) {
						anode next_a;
						next_a.s = new_state;
						next_a.cost = record[new_state] = cur.cost + 1;
						next_a.est = estimate(new_state.start, dist);
						if (next_a.est < oo)
							q.push(next_a);
					}
				}
			}
		}
	}
	solution = end_path;
}


void Start_Astar(string input_file_gol, int cols) {
	state initial;
	global_cols = cols;
	temp_state = "";
	start_state = "";
	end_state = "";
	for (int i = 0; i < input_file_gol.size(); i++) {
		if (input_file_gol[i] == '#')
			temp_state += '#';
		else
			temp_state += ' ';
		if (input_file_gol[i] == '.') {
			start_state += ' ';
			end_state += '.';
		}
		else if (input_file_gol[i] == '*') {
			start_state += '$';
			end_state += '.';
		}
		else if (input_file_gol[i] == '+') {
			start_state += '@';
			end_state += '.';
		}
		else {
			start_state += input_file_gol[i];
			end_state += ' ';
		}
		if (start_state[i] == '@')
			initial.ppos = i;
	}
	initial.start = start_state;
	initial.path = "";
	auto* dist = new int[length];
	pre(temp_state, dist);
	astar(initial, dist);
}

extern "C" {
	EXPORT size_t Astar(char* input_file, int len, int cols) {
		string s;
		length = len;
		for (int i = 0; i < len * 2; i += 2)
			s.push_back(input_file[i]);
		input_file_gol = s;
		Start_Astar(s, cols);
		return solution.size();
	}

	EXPORT void Get_solution(char* return_solution) {
		for (int i = 0; i < solution.size(); i++)
			if (return_solution[i * 2] != '\0')
				return_solution[i * 2] = solution[i];
	}
}