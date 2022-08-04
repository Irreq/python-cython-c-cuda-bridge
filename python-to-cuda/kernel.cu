#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include "cuda_runtime.h"
#include <math.h>
#include <stdio.h>

// Thread block size
#define BLOCK_SIZE 256

// Expose function
extern "C" void cudaExposedWrapper(int *res, const int *first, const int *last, int n_bytes);

// Your kernel to be indirectly called from Python
__global__ void multiplyKernel(int *res, const int *a, const int *b, int size)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < size)
    {
        res[i] = a[i] * b[i];
    }
}

// Cuda Wrapper for `multiplyKernel` used by C or Cython code
void cudaExposedWrapper(int *res, const int *first, const int *last, int n_bytes)
{
    // Setup buffers for GPU
    int *dev_res = nullptr;
    int *dev_first = nullptr;
    int *dev_last = nullptr;

    // Allocate memory on GPU for three vectors
    cudaMalloc((void **)&dev_res, n_bytes * sizeof(int));
    cudaMalloc((void **)&dev_first, n_bytes * sizeof(int));
    cudaMalloc((void **)&dev_last, n_bytes * sizeof(int));

    // Copy allocated host memory to device
    cudaMemcpy(dev_first, first, n_bytes * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(dev_last, last, n_bytes * sizeof(int), cudaMemcpyHostToDevice);

    // Compute the result using one thread per element in vector
    // 2 is number of computational blocks and (n_bytes + 1) / 2 is a number of threads in a block
    multiplyKernel<<<2, (n_bytes + 1) / 2>>>(dev_res, dev_first, dev_last, n_bytes);

    // cudaDeviceSynchronize waits for the kernel to finish, and returns
    // any errors encountered during the launch.
    cudaDeviceSynchronize();

    // Copy output vector from GPU buffer to host memory.
    cudaMemcpy(res, dev_res, n_bytes * sizeof(int), cudaMemcpyDeviceToHost);

    // Release allocated memory
    cudaFree(dev_res);
    cudaFree(dev_first);
    cudaFree(dev_last);

    cudaDeviceReset();
}