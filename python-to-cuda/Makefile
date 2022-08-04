CC = gcc
DEBUG = -Wall -Werror -v
CFLAGS = -O3 -march=native # $(DEBUG)

CUDA_LIBS = -L/usr/local/cuda/lib64

RM = rm

.PHONY: all

all: cubridge.so

# Cuda Python Bridge
bridge.o:
	$(CC) $(CFLAGS) -I /usr/local/cuda/include -c -o bridge.o bridge.c -lstdc++

# Cuda Kernel
kernel.o:
	nvcc --compiler-options '-fPIC' -c -o kernel.o kernel.cu

cubridge.so: bridge.o kernel.o
	$(CC) $(CFLAGS) -shared -o cubridge.so bridge.o kernel.o $(CUDA_LIBS) -lcudart -lstdc++ -fPIC

.PHONY: clean
clean:
	$(RM) *.so *.o