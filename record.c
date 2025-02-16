#include <stdio.h>
#include "udebugfs.h"
#include <unistd.h>

#define DEBUGFS_PATH "/sys/kernel/debug/repabp/"
#define READ_HISTORY_PATH "/sys/kernel/debug/repabp/read_history"
#define READ_ARRAY_PATH "/dev/repabp_history"

struct read_records_output_t{
    unsigned long long begin_pfn;
    unsigned long long end_pfn;
    unsigned long long history;
};

int run_flag(void){
    int runflag;
    FILE* file;
    file=fopen("./runflag","r");
    fscanf(file,"%d",&runflag);
    fclose(file);
    return runflag;
}
int main(){
    FILE* file;
    int round=0;
    char buffer[64];
    unsigned long long record_amount;

    system("echo 1 > ./record_lock");

    file=fopen("history","w");
    while(run_flag()){
    // while(1){
        round++;
        fprintf(file,"round=%d\n",round);
        // printf("DEBUG\n");
        read_from_debugfs_file_by_bits(buffer,READ_HISTORY_PATH,128);
        sscanf(buffer,"%llu",&record_amount);
        fprintf(file,"record_amount=%llu\n",record_amount);
        if(record_amount!=0){
            int fd;
            struct read_records_output_t* rr_buffer=NULL;
            rr_buffer=mmap_with_debugfs_file(READ_ARRAY_PATH,record_amount*sizeof(struct read_records_output_t),&fd);
            for(int i=0;i<record_amount;i++){
                fprintf(file,"%llu-%llu:%llu\n",rr_buffer[i].begin_pfn,rr_buffer[i].end_pfn,rr_buffer[i].history);
            }
            munmap_with_debugfs_file(fd,rr_buffer,record_amount*sizeof(struct read_records_output_t));
        }
        fflush(file);
        usleep(900000);
    }
    fclose(file);
    
    system("echo 0 > ./record_lock");
}
