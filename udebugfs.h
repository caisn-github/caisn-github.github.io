#ifndef __UDEBUGFS_H__
#define __UDEBUGFS_H__
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <fcntl.h>

unsigned long read_from_debugfs_u64(const char* path) {
    unsigned long data;
    FILE *file = fopen(path, "r");
    if (file != NULL) {
        fscanf(file, "%lu", &data);
        fclose(file);
        return data;
    } else {
        perror("无法打开文件");
        exit(1);
    }
}
void write_to_debugfs_u64(const char* path, unsigned long data){
    FILE *file = fopen(path, "w");
    if (file != NULL) {
        fprintf(file, "%ld",data);
        fclose(file);
    } else {
        perror("无法打开文件");
        exit(1);
    }
}
int read_from_debugfs_file_by_bits(unsigned char* buffer, const char* path, int amount){
    FILE *file;
    int ret=-1;

    file = fopen(path, "rb");
    if (file != NULL) {
        ret=fread(buffer, sizeof(char), amount, file);
        fclose(file);
    } else {
        perror("无法打开文件");
        exit(1);
    }
    return ret;
}
void write_to_debugfs_file(const char* path, unsigned long data){
    FILE *file = fopen(path, "w");
    if (file != NULL) {
        fprintf(file, "%ld",data);
        fclose(file);
    } else {
        perror("无法打开文件");
        exit(1);
    }
}
void* mmap_with_debugfs_file(const char* path,unsigned long long size,int* fd){
    *fd = open(path, O_RDONLY);
    if (*fd == -1) {
        perror("Error opening character device");
        return NULL;
    }
    void *mapped_data = mmap(NULL, size, PROT_READ, MAP_SHARED, *fd, 0);
    if (mapped_data == MAP_FAILED) {
        perror("Error mapping memory");
        close(*fd);
        return NULL;
    }
    return mapped_data;
}
void munmap_with_debugfs_file(int fd, void* p,unsigned long long size){
    // Unmap the memory
    if (munmap(p, size) == -1) {
        perror("Error unmapping memory");
    }

    // Close the device file
    close(fd);
}

#endif
