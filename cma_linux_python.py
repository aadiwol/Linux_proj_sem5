#!/usr/bin/env python3
"""
Contiguous Memory Allocation Simulator in Python
Supports First-Fit, Best-Fit, Worst-Fit, Coalescing, and Compaction
"""

from dataclasses import dataclass
from typing import List
import time


@dataclass
class Block:
    start_addr: int
    size: int
    is_free: bool = True
    pid: str = "FREE"


class ContiguousMemorySimulator:
    def __init__(self, total_memory: int = 1024):
        self.total_memory = total_memory
        self.memory: List[Block] = [Block(0, total_memory, True, "FREE")]

    def coalesce(self) -> None:
        """Merge adjacent free blocks to prevent false fragmentation."""
        i = 0
        while i < len(self.memory) - 1:
            if self.memory[i].is_free and self.memory[i + 1].is_free:
                self.memory[i].size += self.memory[i + 1].size
                self.memory.pop(i + 1)
            else:
                i += 1

    def allocate_mem(self, pid: str, req_size: int, algo: int) -> None:
        """
        Allocate memory using:
        1 = First-Fit, 2 = Best-Fit, 3 = Worst-Fit
        """
        if req_size <= 0:
            print("[!] Error: Request size must be greater than 0.")
            return

        target_idx = -1

        if algo == 1:  # First-Fit
            for i, blk in enumerate(self.memory):
                if blk.is_free and blk.size >= req_size:
                    target_idx = i
                    break
        elif algo == 2:  # Best-Fit
            min_diff = float("inf")
            for i, blk in enumerate(self.memory):
                if blk.is_free and blk.size >= req_size:
                    diff = blk.size - req_size
                    if diff < min_diff:
                        min_diff = diff
                        target_idx = i
        elif algo == 3:  # Worst-Fit
            max_diff = -1
            for i, blk in enumerate(self.memory):
                if blk.is_free and blk.size >= req_size:
                    diff = blk.size - req_size
                    if diff > max_diff:
                        max_diff = diff
                        target_idx = i
        else:
            print("[!] Invalid algorithm selected. Defaulting to First-Fit.")
            self.allocate_mem(pid, req_size, 1)
            return

        # Check for failure
        if target_idx == -1:
            total_free = sum(b.size for b in self.memory if b.is_free)
            print(f"[!] Allocation FAILED for {pid} ({req_size} KB).")
            if total_free >= req_size:
                print(
                    f"    -> Cause: External Fragmentation "
                    f"({total_free} KB total free, but scattered across holes)."
                )
            else:
                print(
                    f"    -> Cause: Insufficient total free memory "
                    f"({total_free} KB available)."
                )
            return

        target_blk = self.memory[target_idx]

        # Exact fit vs. splitting the free hole
        if target_blk.size == req_size: 
            target_blk.is_free = False
            target_blk.pid = pid
        else:
            alloc_block = Block(target_blk.start_addr, req_size, False, pid)
            rem_hole = Block(
                target_blk.start_addr + req_size,
                target_blk.size - req_size,
                True,
                "FREE",
            )
            self.memory[target_idx : target_idx + 1] = [alloc_block, rem_hole]

        print(f"[+] Allocated {req_size} KB to {pid} at address {target_blk.start_addr} KB.")

    def free_mem(self, pid: str) -> None:
        """Deallocate all blocks belonging to a process ID and coalesce."""
        found = False
        for blk in self.memory:
            if not blk.is_free and blk.pid == pid:
                blk.is_free = True
                blk.pid = "FREE"
                print(f"[-] Freed process {pid} ({blk.size} KB at address {blk.start_addr} KB).")
                found = True

        if not found:
            print(f"[!] Process {pid} not found in memory.")
            return

        self.coalesce()

    def compact_memory(self) -> None:
        """Shift all allocated blocks to the start to eliminate external fragmentation."""
        new_memory: List[Block] = []
        curr_addr = 0
        total_free = 0

        for blk in self.memory:
            if not blk.is_free:
                new_memory.append(Block(curr_addr, blk.size, False, blk.pid))
                curr_addr += blk.size
            else:
                total_free += blk.size

        if total_free > 0:
            new_memory.append(Block(curr_addr, total_free, True, "FREE"))

        self.memory = new_memory
        print(
            f"[*] Memory Compaction Complete. "
            f"{total_free} KB combined into a single contiguous free block."
        )

    def display_memory(self) -> None:
        """Print visual ASCII memory strip and partition table."""
        free_sizes = [b.size for b in self.memory if b.is_free]
        total_free = sum(free_sizes)
        max_hole = max(free_sizes, default=0)
        ext_frag = total_free - max_hole

        print(f"\n================ MEMORY MAP ({self.total_memory} KB Total) ================")
        strip = "|" + "|".join(f" {b.pid} ({b.size}K) " for b in self.memory) + "|"
        print(strip)
        print("-" * 60)
        print(f"{'Block#':<8} {'Start(KB)':<12} {'End(KB)':<12} {'Size(KB)':<10} {'Status':<10}")
        print("-" * 60)

        for idx, b in enumerate(self.memory):
            end_addr = b.start_addr + b.size - 1
            print(f"{idx:<8} {b.start_addr:<12} {end_addr:<12} {b.size:<10} {b.pid:<10}")

        print("-" * 60)
        print(
            f"Total Free: {total_free} KB | Largest Hole: {max_hole} KB | "
            f"External Frag: {ext_frag} KB"
        )
        print("=" * 60 + "\n")


def run_demo(sim: ContiguousMemorySimulator) -> None:
    """Automated walkthrough showing External Fragmentation and Compaction."""
    print("\n[*] Starting Automated Fragmentation & Compaction Demo...")
    sim.__init__(sim.total_memory)

    sim.allocate_mem("P1", 300, 1)
    sim.allocate_mem("P2", 250, 1)
    sim.allocate_mem("P3", 300, 1)
    sim.display_memory()
    time.sleep(1.0)

    print("[*] Freeing P2 (creates a 250 KB hole in the middle)...")
    sim.free_mem("P2")
    sim.display_memory()
    time.sleep(1.0)

    print("[*] Attempting to allocate P4 (350 KB) -> Fails due to External Fragmentation:")
    sim.allocate_mem("P4", 350, 2)
    time.sleep(1.0)

    print("\n[*] Running Compaction and retrying P4 (350 KB)...")
    sim.compact_memory()
    sim.allocate_mem("P4", 350, 1)
    sim.display_memory()


def main() -> None:
    try:
        raw_size = input("Enter total physical memory size in KB [default 1024]: ").strip()
        total_size = int(raw_size) if raw_size else 1024
        if total_size <= 0:
            total_size = 1024
    except ValueError:
        total_size = 1024

    sim = ContiguousMemorySimulator(total_size)
    sim.display_memory()

    while True:
        print("1. Allocate Process   2. Free Process   3. Compact Memory")
        print("4. View Map           5. Run Auto Demo  6. Exit")
        choice = input("Select action (1-6): ").strip()

        if choice == "1":
            pid = input("Enter Process ID (e.g., P1): ").strip() or "P1"
            try:
                size = int(input("Enter Process Size (KB): ").strip())
                algo = int(input("Fit Strategy (1=First-Fit, 2=Best-Fit, 3=Worst-Fit): ").strip())
                sim.allocate_mem(pid, size, algo)
                sim.display_memory()
            except ValueError:
                print("[!] Invalid numeric input.")
        elif choice == "2":
            pid = input("Enter Process ID to free: ").strip()
            sim.free_mem(pid)
            sim.display_memory()
        elif choice == "3":
            sim.compact_memory()
            sim.display_memory()
        elif choice == "4":
            sim.display_memory()
        elif choice == "5":
            run_demo(sim)
        elif choice == "6":
            print("Exiting simulator.")
            break
        else:
            print("[!] Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()