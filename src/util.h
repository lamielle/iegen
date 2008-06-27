/*! \file
 
    util.h

    Declarations of general utility macros and functions.
*/

#define MALLOC(p, typ, sz)  { if (!(p = (typ *)malloc((sz) * sizeof(typ)))) { \
                                    printf("MALLOC: No more space!!\n"); exit(1); } }

#define FREE(x, typ, sz)  {if (sz != 0 && x !=NULL) free(x);}

