#include <bits/stdc++.h>
using namespace std;

struct cell{
    pair<char,char> name;
    vector<pair<char , char>> cnds; // cnds
    int state;// 0-->wrong , 1-->cnds , 2-->right
};

struct transition
{
    char nextState;
    int output;
};
map<char,vector<transition>> states;

vector<pair<char , char>> FSM(map<char , vector<transition>> states){
    vector<pair<char, char>> equivalants; //equivalent pairs(the return)
    vector<cell> table; //tringular table
    map<pair<char , char> , int> tablestates;
    
    int sz = states.size();      //How many lines are there in the table
    auto it = states.begin();    //points to first line and its aim is to be used in the outer loop
    auto it2 = next(it);         //points to second line and its aim is to be used in the inner loop

    //forming the tringular table <<< O(n^2) >>>
    for(int i = 0;i<sz;i++){
        for (int j = i+1;j<sz;j++){
            cell c;   //cell initialization
            c.name = {it->first , it2->first}; //assigning name
            
            //assigning states based upon O/Ps
            if (it->second[0].output != it2->second[0].output || it->second[1].output != it2->second[1].output)
            c.state = 0;

            //assigning states based upon nextstates
            else if (it->second[0].nextState == it2->second[0].nextState && it->second[1].nextState == it2->second[1].nextState){
                c.state = 2;
            }

            //assigning cnds for unequal nextstates
            else{
                c.state = 1;
                //adding condition to cnds
                char a = it->second[0].nextState;
                char b = it2->second[0].nextState;
                if(a>b)swap(a,b);
            
                if (a != b)
                    c.cnds.push_back({a, b});

                a = it->second[1].nextState;
                b = it2->second[1].nextState;
                if (a > b)swap(a, b);

                if (a != b)
                    c.cnds.push_back({a, b});
            }

            table.push_back(c);
            tablestates[c.name] = c.state;

            it2 = next(it2);//ready for the next state
        }

        //updating iterators for the next loop
        it = next(it);
        it2 = next(it);
    }
    //end of table formation
    
    
    bool change = true; 
    while(change){
        change = false;
        for(auto it = table.begin();it != table.end();it++){
            if(it->state == 1){
                for(auto it2 = it->cnds.begin(); it2 != it->cnds.end(); it2++){
                    if(tablestates[*it2] == 0) {
                        it->cnds.erase(it2);
                        change = true;
                        it->state = 0;
                        tablestates[it->name] = 0;
                        break;
                    }
                    else if (tablestates[*it2] == 2){
                        it->cnds.erase(it2);
                        change = true;
                        if (it->cnds.empty())
                        {
                            it->state = 2;
                            tablestates[it->name] = 2;
                        }
                        break;
                    }
                }

            }

        }
    }

    for (auto it = table.begin(); it != table.end(); it++)
    {
        if (it->state != 0) //if it has conditions so it is right too , so 1 or 2 are good to go
        { 
            equivalants.push_back(it->name);
        }
    }

    return equivalants;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    int numStates;
    
    if (!(cin >> numStates))
        return 0;

    for (int i = 0; i < numStates; i++)
    {
        char stateName, next0, next1;
        int out0, out1;
        
        cin >> stateName >> next0 >> out0 >> next1 >> out1;

        states[stateName].push_back({next0, out0});
        states[stateName].push_back({next1, out1});
    }

    vector<pair<char, char>> result = FSM(states);

    for (auto const &p : result)
    {
        cout << p.first << " " << p.second << endl;
    }
    return 0;
}