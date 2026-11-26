# Contiguous Memory Allocation Simulator

A Python command-line simulator demonstrating how an Operating System manages contiguous physical memory partitions, handles dynamic allocation strategies, and resolves external fragmentation.

## Features
* **Dynamic Partitioning:** Splits free memory holes on exact or partial fits instead of fixed-size partitions.
* **Allocation Algorithms:** Supports **First-Fit**, **Best-Fit**, and **Worst-Fit** placement strategies.
* **Automatic Coalescing:** Merges adjacent free blocks immediately upon process deallocation to prevent false fragmentation.
* **Memory Compaction:** Relocates active processes to the beginning of physical memory to combine scattered holes into a single contiguous block.
* **Visual Memory Map:** Prints an ASCII memory strip, partition address table, and live external fragmentation metrics (`Total Free - Largest Hole`).
* **Automated Walkthrough:** Built-in demo illustrating how external fragmentation blocks allocation and how compaction resolves it.

---

## Core Architecture & Key Functions

### `Block` (Dataclass)
Represents a contiguous memory partition with:
* `start_addr` (`int`): Starting physical address in KB.
* `size` (`int`): Size of the partition in KB.
* `is_free` (`bool`): Allocation status (`True` for hole, `False` for active process).
* `pid` (`str`): Process identifier (defaults to `"FREE"`).

### `ContiguousMemorySimulator` Methods

| Function | Description |
| :--- | :--- |
| `__init__(total_memory=1024)` | Initializes physical memory as a single contiguous free block of `total_memory` KB. |
| `allocate_mem(pid, req_size, algo)` | Allocates memory to `pid` using **First-Fit (`1`)**, **Best-Fit (`2`)**, or **Worst-Fit (`3`)**. Splits holes when `block.size > req_size` and diagnoses external fragmentation vs. insufficient memory on failure. |
| `free_mem(pid)` | Marks all blocks held by `pid` as free and automatically triggers `coalesce()`. |
| `coalesce()` |

### `Results` 
<img width="1212" height="1538" alt="image" src="https://github.com/user-attachments/assets/d560e811-434c-44df-8abf-11c4483be471" />
<img width="1180" height="1446" alt="image" src="https://github.com/user-attachments/assets/affa2199-7284-4fc8-84bd-63e0a5f2dc8c" />

