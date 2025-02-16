#include <iostream>
#include <fstream>
#include <thread>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <atomic>
#include <sstream>
#include <mutex>
#include <set>
using namespace std;

unsigned long long convert_str_to_u64(string s){
    stringstream ss;
    ss<<s;
    unsigned long long result;
    ss>>result;
    return result;
}

struct record_t{
    unsigned long long left_pfn;
    unsigned long long right_pfn;
    unsigned long long heat;
};
vector<vector<struct record_t>> records;
int main() {
    // ifstream input=ifstream("../history");
    ifstream input=ifstream("../401.bzip2.history");
    ofstream output=ofstream("./plot_matrix");
    vector<struct record_t> tmp_group;
    unsigned long long max_pfn=0;
    while(!input.eof()){
        string s;
        input >> s;
        if(s.find("round=")!=-1){
            int x=convert_str_to_u64(s.substr(6));
            if(x>1){
                records.push_back(tmp_group);
                tmp_group.clear();
            }
        }
        if(s.find("record_amount=")!=-1){
            int n=convert_str_to_u64(s.substr(14));
            for(int i=0;i<n;i++){
                input >> s;
                int split1_index=s.find("-");
                int split2_index=s.find(":");
                unsigned long long left_pfn=convert_str_to_u64(s.substr(0,split1_index));
                unsigned long long right_pfn=convert_str_to_u64(s.substr(split1_index+1,split2_index-split1_index-1));
                max_pfn=max(max_pfn,right_pfn);
                unsigned long long history=convert_str_to_u64(s.substr(split2_index+1));
                int heat=0;
                for(int j=0;j<5;j++){
                    heat<<=1;
                    if(history&1){
                        heat|=1;
                    }
                    history>>=1;
                }
                struct record_t tmp_record;
                tmp_record.left_pfn=left_pfn;
                tmp_record.right_pfn=right_pfn;
                tmp_record.heat=heat;
                tmp_group.push_back(tmp_record);
            }
        }
    }
    input.close();
    records.push_back(tmp_group);
    tmp_group.clear();
    cout<<records.size()<<endl;
    for(unsigned long long y=0;y<max_pfn;y++){
        cout<<"["<<y<<"/"<<max_pfn<<"]"<<endl;
        for(int x=0;x<records.size();x++){
            int heat=0;
            if(records[x].size()>=1){
                if(y<records[x][0].left_pfn){
                    heat=0;
                } else if (y>=records[x][records[x].size()-1].right_pfn){
                    heat=0;
                } else{
                    for(int j=0;j<records[x].size();j++){
                        if(records[x][j].left_pfn<=y && y<records[x][j].right_pfn){
                            heat=records[x][j].heat;
                            break;
                        }
                        if(records[x][j].right_pfn<=y){
                            break;
                        }
                    }
                }
            }            
            output<<heat<<" ";
        }
        output<<endl;
    }
    output.close();
    cout<<"x:"<<records.size()<<" y:"<<max_pfn<<endl;
}