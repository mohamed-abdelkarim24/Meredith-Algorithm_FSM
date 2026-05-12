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
            
            //assigning states and cnds by looping through all input's next state 
            //(asking user to enter the number of inputs will be just beneficial for the gui part).....
            for(int j = 0 ;j<it->second.size();j++){
            //assigning states based upon O/Ps
            if (it->second[j].output != it2->second[j].output){
            c.state = 0;break;
            }
            //assigning states based upon nextstates
            else if (it->second[j].nextState == it2->second[j].nextState){
                if(c.cnds.empty()){
                    c.state = 2;
                }
                continue;
            }

            //assigning cnds for unequal nextstates
            else{
                c.state = 1;
                //adding condition to cnds
                char a = it->second[j].nextState;
                char b = it2->second[j].nextState;
                if(a>b)swap(a,b);
            
                if (a != b)
                    c.cnds.push_back({a, b});
            }
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

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);

    int numStates, numInputs;
    string type; // mealy or moore

    
    if (!(cin >> type >> numInputs >> numStates))
        return 0;
    
    numInputs = pow(2,numInputs);

    for (int i = 0; i < numStates; i++)
    {
        char stateName;
        cin >> stateName;

        if (type == "moore")
        {
            int stateOutput;
            vector<char> nextStates(numInputs);

            for (int j = 0; j < numInputs; j++)
                cin >> nextStates[j];
            cin >> stateOutput;

            for (int j = 0; j < numInputs; j++)
            {
                states[stateName].push_back({nextStates[j], stateOutput});
            }
        }
        else
        {
            vector<char> nexts(numInputs);
            for (int j = 0; j < numInputs; j++)
                cin >> nexts[j]; 

            for (int j = 0; j < numInputs; j++)
            {
                int out;
                cin >> out;                                   
                states[stateName].push_back({nexts[j], out}); 
            }
        }
    }

    vector<pair<char, char>> result = FSM(states);

    vector<set<char>> equivalenceClasses;

    for (auto pairIt = result.begin(); pairIt != result.end(); pairIt++)
    {
        int firstGroupIdx = -1;
        int secondGroupIdx = -1;

        for (auto groupIt = equivalenceClasses.begin(); groupIt != equivalenceClasses.end(); groupIt++)
        {
            //getting current index based on the iterator position
            int currentIdx = distance(equivalenceClasses.begin(), groupIt);

            if (groupIt->count(pairIt->first))
                firstGroupIdx = currentIdx;

            if (groupIt->count(pairIt->second))
                secondGroupIdx = currentIdx;
            
        }

        if (firstGroupIdx == -1 && secondGroupIdx == -1)// neither state is in a group yet
            equivalenceClasses.push_back({pairIt->first, pairIt->second});
        
        else if (firstGroupIdx != -1 && secondGroupIdx == -1)// only the first state exists
            equivalenceClasses[firstGroupIdx].insert(pairIt->second);

        else if (firstGroupIdx == -1 && secondGroupIdx != -1) // only the second state exists
            equivalenceClasses[secondGroupIdx].insert(pairIt->first);
        
        else if (firstGroupIdx != secondGroupIdx)// both exist in Different groups ---> merge them
        {
            equivalenceClasses[firstGroupIdx].insert(equivalenceClasses[secondGroupIdx].begin(),equivalenceClasses[secondGroupIdx].end());
            // remove the redundant group
            equivalenceClasses.erase(equivalenceClasses.begin() + secondGroupIdx);
        }
    }

    // final output for the Python gui 
    for (auto groupIt = equivalenceClasses.begin(); groupIt != equivalenceClasses.end(); groupIt++)
    {
        for (auto stateIt = groupIt->begin(); stateIt != groupIt->end(); stateIt++)
        {
            cout << *stateIt << " ";
        }
        cout << "\n";
    }

    return 0;
}