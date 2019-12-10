#include <ibex.h>

#include <vector>
#include <queue>

// some variables to test the different algorithms
//#define POST 1
//#define FIND_PATTERN 1
#define DECOMPOSE 1

// Macro variables to set the values of the maximal length of a
// pattern (NB_K) and the maximal number of splittings of the
// state-space (NB_D)
#define NB_K 1  // 3
#define NB_D 10 // 20

using namespace ibex;

// Data type for sampled switched systems
typedef struct {
	double period;
	std::vector<Function*> dynamics;
	int nb_dynamics;
}sampledSwitchedSystem;

typedef struct {
	IntervalVector *Yinit;
	Affine2Vector *Ycurrent;
	std::vector<int> pattern;  
} node;


// Post operator
IntervalVector post(const sampledSwitchedSystem& sys, const IntervalVector W,
		const std::vector<int> pattern) {

	Affine2Vector y0 = Affine2Vector(W);

	std::vector<int>::const_iterator it = pattern.begin();
	for (; it != pattern.end(); it++)
	{
		ivp_ode mode = ivp_ode(*(sys.dynamics[*it]), 0.0, y0);
		simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
		simu.run_simulation();
		y0=*(simu.list_solution_j.back().box_jnh_aff);
	}
	return y0.itv();
}

// A process to compute the successor of binary word of a given length 
bool nextPattern(std::vector<int>& pattern)
{
	for (int i = pattern.size() - 1; i >= 0; i-- )
	{
		pattern[i] += 1 ;
		if ( pattern[i] > 15 )
		{
			pattern[i] = 0 ;
			continue ;
		}
		return true ;
	}
	return false;
}

// Unfolding verifies constraint crossing
bool constraint(const sampledSwitchedSystem& sys, const IntervalVector W, const IntervalVector B,
	const IntervalVector S, const std::vector<int> pattern) {

	Affine2Vector y1 = Affine2Vector(W);

	std::vector<int>::const_iterator it = pattern.begin();
	for (; it != pattern.end(); it++) {
		ivp_ode mode = ivp_ode(*(sys.dynamics[*it]), 0.0, y1);
		simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
		simu.run_simulation();
		if (simu.has_crossed(B) )
		{
			return false;
		}
		if (!simu.stayed_in(S))
		{
			return false;
		}
	}
	return true;
}


// Search for a pattern of maximal length k which can prove the
// invariance
bool findPattern (const sampledSwitchedSystem& sys, const IntervalVector W,
		const IntervalVector R, const IntervalVector B,
		const IntervalVector S, unsigned int k,
		std::vector<int>&  res_pattern) {

	std::cerr << "\tINIT = " << W << std::endl;
	for (unsigned int i = 1; i <= k; i++) 
	{
	std::vector<int> pattern(i, 0);
	do {
		std::vector<int>::const_iterator it = pattern.begin();
		std::cerr << "\tPATTERN = (";
		for (; it != pattern.end(); it++) {
			std::cerr << *it << " " ;
		}
		std::cerr << ")" << std::endl;
		IntervalVector res = post(sys, W, pattern);
		std::cerr << "Post(" << W << ") = " << res << " AND R = " << R << std::endl;
		if (res.is_subset(R) && constraint(sys,W,B,S,pattern))
		{
			std::cerr << "\tPATTERN FOUND !!!" << std::endl;
			res_pattern = pattern;
			return true;
		}
	} while (nextPattern(pattern));
	}
	return false;
}


//find a pattern with new algo 
bool findPattern2 (const sampledSwitchedSystem& sys, const IntervalVector W,
		const IntervalVector R, const IntervalVector B,
		const IntervalVector S, unsigned int k,
		std::vector<int>&  res_pattern) {

node node_init;
node_init.Yinit = new IntervalVector(W);
node_init.Ycurrent = new Affine2Vector(W,true);
node_init.pattern = std::vector<int>();

std::list<node> list_node;
std::list <std::pair <IntervalVector,std::vector<int> > > list_sol;

list_node.push_back(node_init);

int nb_pattern = sys.nb_dynamics;

while(!list_node.empty())
{   
//std::cout << "size of list : " << list_node.size() << std::endl; 
node node_current = list_node.front();
list_node.pop_front();

for (int i=0; i < nb_pattern; i++)
{  
	if (node_current.pattern.empty())
std::cout << "current pattern : " << i << std::endl;
	else
std::cout << "current pattern : " << node_current.pattern << " + " << i << std::endl;
	
	ivp_ode mode = ivp_ode(*(sys.dynamics[i]), 0.0, *node_current.Ycurrent);
	simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
	simu.run_simulation();
		
	bool fin_R = simu.finished_in(R);
	bool stay_S = simu.stayed_in(S);
	bool cross_B = simu.has_crossed(B);
	bool out_S = simu.go_out(S);
	bool fin_B = simu.finished_in(B);
	
	if (fin_R && stay_S && !cross_B)
	{
std::cout << "sol found !" << std::endl;
node_current.pattern.push_back(i);

res_pattern = node_current.pattern;

return true;
	}
	else 
	{
if (out_S || fin_B) //not only the last may be in obstacles...
{
	std::cout << "Wrong direction !" << std::endl;
	//nop
}
else 
{
	if (stay_S && !cross_B)
	{
	if (node_current.pattern.size()+1 < k)
	{
		std::cout << "Increment of pattern !" << std::endl;	      

		node new_node;
		new_node.Yinit = new IntervalVector(*node_current.Yinit);
		new_node.Ycurrent = new Affine2Vector(simu.get_last());
		
		std::vector<int> new_pattern (node_current.pattern);
		new_pattern.push_back(i);
		new_node.pattern = new_pattern;
		list_node.push_back(new_node);	      

	}
	}
}
	}
}

}
return false;
}


// The main algorithm of minimator
bool decompose (const sampledSwitchedSystem& sys, const IntervalVector W,
	const IntervalVector R, const IntervalVector B,
	const IntervalVector S, unsigned int k, unsigned int d,
	std::vector<std::pair<IntervalVector, std::vector<int> > >& result) {

	std::vector<int> res_pattern;

	// q is a queue of sub-state-space to explore to prove the invariance
	std::queue<IntervalVector> q;
	q.push (W);

	unsigned int nbStep = d;

	while (!q.empty() && nbStep > 0) {
		IntervalVector current = q.front ();
		q.pop();
		bool flag = findPattern (sys, current, R, B, S, k, res_pattern);
		if (flag) {
			// Validated result, we keep it in the vector of results
			result.push_back (std::pair< IntervalVector, std::vector<int> > (current, res_pattern));
		}
		else {
				//if (current.diam().max() > 0.5)
				//{
			LargestFirst bbb(0.1,0.5);
			std::pair<IntervalVector,IntervalVector> p = bbb.bisect(current);
			q.push (p.first);
			q.push (p.second);
			nbStep--;
				//}
		}
	}

	if (nbStep <= 0)
	{
		return false;
	}
	else
	{
		return true;
	}
}

int main(){


	Variable x(2);
    //IntervalVector W(2);
    //W[0] = Interval(40,100);
    //W[1] = Interval(0,300);

    //Interval Ti(20, 40); // It include valve mode = OFF and ON
    Interval Te(0, 30);
    Interval I(0, 850);

    //double period = 15*60; // not works with 100

    IntervalVector x0(2);        
    x0[0] = Interval(23.0, 23.2);
    x0[1] = Interval(0.1, 0.13);   // Initial Volumen

	Function m1 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 
	8.403225763080125e-07*I/x[1] + 
	0.00048018432931886426/x[1], 0.001*(0.1-x[1]) ) );

/*
	Function m2 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 
		8.403225763080125e-07*I/x[1] + 
	0.00048018432931886426/x[1], 0.001*(0.2-x[1]) ) );

	Function m3 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 
	8.403225763080125e-07*I/x[1] + 
	0.00048018432931886426/x[1], 0.001*(0.3-x[1]) ) );

	Function m4 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 
	8.403225763080125e-07*I/x[1], 
	0.001*(0.1-x[1]) ) );

	Function m5 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 
	8.403225763080125e-07*I/x[1], 
	0.001*(0.2-x[1]) ) );

	Function m6 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 
	8.403225763080125e-07*I/x[1], 
	0.001*(0.3-x[1]) ) );
*/

	sampledSwitchedSystem sys;

	sys.period = 15*60; 
	sys.dynamics.push_back(&m1);

	/*

	sys.dynamics.push_back(&m2);
	sys.dynamics.push_back(&m3);
	sys.dynamics.push_back(&m4);
	sys.dynamics.push_back(&m5);
	sys.dynamics.push_back(&m6);
	
	*/

	sys.nb_dynamics = 1;

	IntervalVector R(2);           // Objectif
	R[0] = Interval(20,40); // (20,22)
	R[1] = Interval(0.1,0.3); // (20,22) 
	//R[2] = Interval(20,22);
	//R[3] = Interval(20,22);


	#ifdef FIND_PATTERN
	IntervalVector current = v3;

	std::vector<int> res_pattern;
	unsigned int k = NB_K;
	bool flag = findPattern (sys, current, R, B, k, res_pattern);
	if (flag) {
	std::cerr << "pattern found = (";
	std::vector<int>::const_iterator it = res_pattern.begin();
	for (; it != res_pattern.end(); it++) {
		std::cerr << *it << " ";
	}
	std::cerr << ") for " << current << std::endl;
	}	
	else {	
	std::cerr << "No pattern found for " << current << std::endl;
	}
	#endif

	#ifdef DECOMPOSE

	IntervalVector W(2);              // ensemble de depart
	W[0]= Interval(25,30);  // (20,22)
	W[1]= Interval(0.1,0.3);  // (20,22)
	//W[2]= Interval(20,22);
	//W[3]= Interval(20,22);

	IntervalVector B(2);               // zone interdite
	B[0] = Interval(10,20); //0.0,1.0
	B[1] = Interval(0.0,0.1); // 0.0,1.0
	//B[2] = Interval(0.0,1.0);
	//B[3] = Interval(0.0,1.0);

	IntervalVector S(2);
	S[0] = Interval(0,80);
	S[1] = Interval(0.1,0.3);
	//S[2] = Interval(19,23);
	//S[3] = Interval(19,23);



	std::list<IntervalVector> list_W;
	list_W.push_back(W);

	//file for solutions
	std::ofstream file("./result_solar_water_heating.txt", std::ios::out | std::ios::trunc);

	while(!list_W.empty())
	{
	IntervalVector current_W = list_W.front();
	list_W.pop_front();

	if (current_W.diam().max() > 0.6)
	{
		LargestFirst bbb(0.1,0.5);

		std::pair<IntervalVector,IntervalVector> p = bbb.bisect(current_W);
		list_W.push_back(p.first);
		list_W.push_back(p.second);
		continue;
	}


	std::cout << "taille list_W : " << list_W.size() << std::endl;

	std::vector< std::pair<IntervalVector, std::vector<int> > > result;
	unsigned int k = NB_K;
	unsigned int d = NB_D;

	bool flag = decompose(sys, current_W, R, B, S, k, d, result);

	if (result.empty())
	{
		std::cerr << "No solution with k = " << k << " and d = " << d << std::endl;
		file << current_W << " : no sol" << std::endl;
	}
	else 
	{
		if (flag)
		{
			std::cerr << "Complete result -> PROOF" << std::endl;
		}
		else 
		{
			std::cerr << "Incomplete result" << std::endl;
		}

		// Display result
		std::vector< std::pair<IntervalVector, std::vector<int> > >::const_iterator it = result.begin();
		for (; it != result.end(); it++) {
		file << "zon = str2zon2(\"" ;
		file << it->first << "\"); \n if is_in_zonotope(X,zon) \t \n pattern = [";

		std::vector<int>::const_iterator it_pat = (it->second).begin();
		for (; it_pat != (it->second).end(); it_pat++) {
			file << *it_pat << " ";
		}
		file << "]; \n endif" << std::endl;
		}
	}
	}
	file.close();

	#endif
	return 0;

}
