- Source: https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

In the second half of the course you’ll work on an operating systems project of your choice in teams of two or three. The goal is to have fun and explore more advanced O / S topics; you don’t have to do novel research.

We’ll grade you on how much you got working, how elegant your design is, how well you can explain it, and how interesting and creative your solution is. We do realize that time is limited, so we don’t expect you to re-write Linux by the end of the semester. Try to make sure your goals are reasonable; perhaps set a minimum goal that’s definitely achievable and a more ambitious goal if things go well.

### Schedule and Deliverables

- Two days after lecture 12: Form groups of 2 to 3 people.
- Two days after lecture 14: Submit a proposal, just a paragraph or two.
- Week of lecture 15: First project conference with 6.828 faculty—we’ll schedule a meeting with each team to discuss your proposal.
- Weeks of lecture 19–20: Second project conference.
- Two days after lecture 23: Submit source code along with a two-page write-up. Put the write-up under the top-level source directory with the name “`README.pdf`”.
- Week of lecture 24: Final conference with faculty, with demonstration.
- Week of lecture 24: Short in-class demonstration.

### Submission Repository

Since most of you will be working in groups for this lab assignment, you may want to use git to share your project code between group members.

You will need to decide on whose source code you will use as a starting point for your group project. That group member should run the following commands to place his or her JOS (or xv6) source code into the group repository. The other members of your group can then checkouts the project from this shared group repository.

At this point, all of your group members should be able to pull and push commits from the shared repository by running `git pull` and `git push` on the `project` branch, respectively.

Keep in mind that git only tracks files that you have explicitly committed, so you may want to run `git status` periodically to see if there are any lingering files in your checkout that you haven’t committed. You can use `git add _filename_` to tell git about files you would like to commit with the next git commit command. If there are files that you will never want to commit, and you want to prevent them from showing up in the output of git status, you should create a file named `.gitignore` and add the filenames that you’d like `git status` to ignore to that file, one per line.

### Ideas

Here’s a list of ideas to get you started thinking—but you should feel free to pursue your own ideas.

- Build a virtual machine monitor that can run multiple guests (for example, multiple instances of JOS), using x86 VM support.
- Do something useful with the x86 Trusted Execution Technology. For example, run applications without having to trust the kernel. [Here (PDF)](http://www.usenix.org/system/files/conference/osdi12/osdi12-final-51.pdf) is a recent paper on this topic.
- Fix xv6 logging to support concurrent transactions, and generally have higher performance, perhaps taking ideas from Linux EXT3.
- Use file system ideas from [Soft updates (PDF)](http://www.ece.cmu.edu/~ganger/papers/osdi94.pdf), WAFL, ZFS, or another advanced file system.
- Add snapshots to a file system, so that a user can look at the file system as it appeared at various points in the past. You’ll probably want to use some kind of copy-on-write for disk storage to keep space consumption down.
- Implement [capabilities (PDF)](http://pdos.csail.mit.edu/6.828/2012/readings/mazieres-hotos6.pdf) to provide fine-grained control over what privileges processes have.
- Build a [distributed shared memory (PDF)](http://www.cise.ufl.edu/~nemo/cop5615/chow/ch7.pdf) (DSM) system, so that you can run multi-threaded shared memory parallel programs on a cluster of machines, using paging to give the appearance of real shared memory. When a thread tries to access a page that’s on another machine, the page fault will give the DSM system a chance to fetch the page over the network from whatever machine currently stores.
- Layer software [RAID-5 (PDF)](http://www.cs.cmu.edu/~garth/RAIDpaper/Patterson88.pdf) over an array of disks, to increase fault tolerance and performance.
- Allow processes to migrate from one machine to another over the network. You’ll need to do something about the various pieces of a process’s state, such as file descriptors in xv6.
- Implement paging to disk in xv6 or JOS, so that processes can be bigger than RAM. Extend your pager with swapping.
- Implement mmap() of files for JOS or xv6.
- Implement loadable kernel modules to extend the xv6 kernel to replace or extend subsystems of the xv6 kernel. For example, make the file system a kernel module so that you can add a kernel module to read DOS file systems, or replace the xv6 file system.
- Use [xfi](http://static.usenix.org/event/osdi06/tech/erlingsson.html) to sandbox code within a process.
- Support x86 2MB or 4MB pages.
- Modify xv6 to have kernel-supported threads inside processes. See in-class uthread assignment to get started. Implementing scheduler activations would be one way to do this project.
- Implement ideas from the Exokernel papers, for example the packet filter.
- Make JOS or xv6 have soft real-time behavior. You will have to identify some application for which this is useful.
- Make JOS or xv6 run on 64-bit CPUs. This includes redoing the virtual memory system to use 4–level pages tables. See reference page for some documentation.
- Port JOS or xv6 to a different microprocessor. The [osdev wiki](http://wiki.osdev.org/Main_Page) may be helpful.
- A window system for xv6 or JOS, including graphics driver and mouse. See reference page for some documentation.
- Implement [dune (PDF)](http://www.usenix.org/system/files/conference/osdi12/osdi12-final-117.pdf) to export privileged hardware instructions to user-space applications in JOS or xv6.
- The linux kernel uses read copy update to be able to perform read operations without holding locks. Explore RCU by implementing it in xv6 and use it to support a name cache with lock-free reads
- Intel recently announced for its upcoming processors. Implement support for Intel’s Transactional Synchronization Extensions in the QEMU emulator. A follow-on project would be to explore the use of Intel TSX primitives in writing concurrent software, such as extending a small multi-core operating system (based on 6.828’s xv6) to use transactional memory.
