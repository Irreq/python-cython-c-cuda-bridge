#include <stdio.h>
#include "kernel.h"

// Dummy param for creating a simple array of BYTES size
#define BYTES 64

extern void cudaExposedWrapper(const int *res, const int *first, const int *last, int n_bytes);

void pythonCudaBridgeWrapper(int *first, int *last, int *res, int n_bytes)
{
    memset(res, 0, n_bytes * sizeof(int));
    cudaExposedWrapper(res, first, last, n_bytes);
}

void python2(int *first, int *second, int *res) {
    *res = *first * *second;
    // *res = 78;
}