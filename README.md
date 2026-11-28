# my-own-redis-server
This is an attempt to build a basic redis server in C# without AI in an effort to learn more about the C# language and the dotnet environement.

Below are details of implementation as well as general lessons regarding the different aspects that are necessary to understand what is happening below the layers of abstractions:

## Project structure
An interesting thing to see here is how does a build happen, what files does it rely on and how do we acheive portability.

On the portability topic: C# code is first compiled (Roslyn) into byte code (.dll) so an intermediary language, then each method gets compiled with a JIT compiler to machine code whenever it's first needed.

This is what achieves portability since the JIT compiler adapts to each machine architecture.

Compiling first into .dll files brings other aspects such as keeping references so that the garbage collector can know when there is memory allocated in the heap without a reference to it anymore.

A build is not a code compilation alone, it is a multiple step pipeline where packages are restored, references are resolved (so that all the .dll files necessary for compilation are assembled) before evening running the Roslyn compiler.

This build is run by MSBuild which is dotnet's build engine, .csproj are the config files that specify refrences and build properties, the .slnx lists the projects to build.

## Networking
The first step of this project implies managing network sessions between the redis server and its clients.

the C# language provides an abstraction to deal with network sockets, understanding that these are kernel objects is interesting.

Sockets are exposed to processes through the UNIX file interface, socket() and accept() return file descriptors, and read/write/close work on them like on files.

A particularly interesting thing is that the kernel does accept connections before the program ever calls accept(), the kernel pushes the socket with an open connection to a queue and lets the program decide whether to handle it or close it.

## Concurrency
Accepting a client connection and handling I/O operations needs to be managed concurrently.

A good opportunity to look at how async functions behave in C# vs how they'd behave in Python which I'm most familiar with.

Calling an async method in C# contrary to Python is hot, it immediately runs on the caller's thread until the first await on something unfinished then returns a task to the caller.

A task is what's more generally defined as a future (the read side of a promise) in computer science: a memory in the heap holding: state, result, exception, continuations.