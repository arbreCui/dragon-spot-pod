/* UNREADY, Source-only B IO isolation. This is not build admission. */
#ifndef AXMAT_FRESH_IO_H
#define AXMAT_FRESH_IO_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

/* No SCI/FIL input path is passed here. Only owned output/cache paths are. */
static void axmat_fresh_io(char *path, size_t capacity)
{
    const char *dir = getenv("SPOT_AXMAT_OBSERVATION_DIRECTORY");
    const char *flag = getenv("SPOT_AXMAT_OBSERVATION");
    size_t n, i, used;
    char name[73], routed[73];
    struct stat info;
    if (!dir || !flag || strcmp(flag,"ADMITTED_SOURCE_ONLY") != 0) goto invalid;
    n = strlen(dir);
    if (n < 1 || n > 12) goto invalid;
    for (i=0; i<n; ++i)
        if (!((dir[i]>='a' && dir[i]<='z') || (dir[i]>='A' && dir[i]<='Z') ||
              (dir[i]>='0' && dir[i]<='9') || dir[i]=='_' || dir[i]=='-')) goto invalid;
    if (lstat(dir,&info) != 0 || !S_ISDIR(info.st_mode) || info.st_uid != getuid()) goto invalid;
    if (strlen(path) >= sizeof(name)) goto invalid;
    strcpy(name,path);
    /* Existing exact owned prefix is accepted, never an arbitrary pathname. */
    if (strncmp(name,dir,n)==0 && name[n]=='/') {
        memmove(name,name+n+1,strlen(name+n+1)+1);
    } else if (name[0]=='.' && name[1]=='/') {
        memmove(name,name+2,strlen(name+2)+1);
    }
    used=strlen(name);
    if (!used || strcmp(name,".")==0 || strcmp(name,"..")==0) goto invalid;
    for (i=0;i<used;++i)
        if (!((name[i]>='a' && name[i]<='z') || (name[i]>='A' && name[i]<='Z') ||
              (name[i]>='0' && name[i]<='9') || name[i]=='_' || name[i]=='-' || name[i]=='.')) goto invalid;
    if (n+1+used > 72 || n+1+used >= capacity) goto invalid;
    snprintf(routed,sizeof(routed),"%s/%s",dir,name);
    strcpy(path,routed);
    return;
invalid:
    fprintf(stderr,"AXMAT fresh IO: missing/unsafe exact owned directory or output basename\n");
    abort();
}
/* Destruction/modification may only name a path already bound to this IO root. */
static void axmat_bound_fresh_io(const char *path)
{
    char routed[73];
    if (strlen(path)>=sizeof(routed)) abort();
    strcpy(routed,path);
    axmat_fresh_io(routed,sizeof(routed));
    if (strcmp(path,routed)!=0) {
        fprintf(stderr,"AXMAT fresh IO: refusing unbound existing write/delete path\n");
        abort();
    }
}
#endif
