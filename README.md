# Contiguous Memory Allocation in Linux

This project introduces contiguous memory allocation, a memory-management
concept in which a process or kernel request is assigned one uninterrupted
region of memory. It covers the basic allocation strategies and explains how
the idea relates to memory management in Linux.

## What is contiguous allocation?

Memory is divided into free and occupied regions. When a request arrives, the
allocator searches for a free region large enough to hold it. Common strategies
include:

- **First fit:** choose the first region that is large enough.
- **Best fit:** choose the smallest region that can satisfy the request.
- **Worst fit:** choose the largest available region.

When a region is larger than the request, the unused part remains available for
later allocations. Over time, free space can become split into small holes.
This is **external fragmentation**: the total free memory may be sufficient,
but no single free region is large enough for a request. Coalescing adjacent
free regions and compaction can help, though compaction requires moving data
and is not always possible.

## How this relates to Linux

Classic first-fit, best-fit, and worst-fit allocation are useful for learning
and simulation, but Linux does not generally allocate process memory by
searching for one large contiguous physical region. Processes use virtual
address spaces, and their pages can map to physical frames located in different
parts of RAM.

The Linux kernel does need contiguous physical pages for some purposes. Its
**buddy allocator** manages physical memory in power-of-two-sized blocks (an
order-*n* block contains 2^*n* pages). It can split larger blocks to satisfy
smaller requests and merge free buddy blocks back together. Fragmentation can
make large contiguous requests harder to satisfy.

Kernel interfaces also have different contiguity properties: `kmalloc`
typically returns physically contiguous memory for supported sizes, while
`vmalloc` provides virtually contiguous memory that may be backed by physically
scattered pages. The **Contiguous Memory Allocator (CMA)** reserves memory that
can be used for movable allocations and reclaimed when a device later needs a
contiguous region, such as for certain DMA operations.

## Learning goals

- Simulate allocation and deallocation with first fit, best fit, and worst fit.
- Track free and occupied regions and calculate external fragmentation.
- Compare how allocation order affects memory usage.
- Distinguish contiguous virtual memory from contiguous physical memory in
  Linux.

This is an educational overview; the classic allocation strategies are models
for understanding the concepts, not a description of Linux's complete memory
management implementation.
