# StackVM (to be renamed)

A simple stack-based virtual machine and assembler. Development in early stages, nothing should be considered stable.

## Project goals

* stack-based
* relatively simple
* quirkless
* extensible (using [Devices](#Devices))

Execution speed is not considered important. However, it would be possible to write quite performant virtual machine with current restrictions. Memory effiency is not good for string processing, though.

I'm planning to create at least one higher-level programming language that compiles to StackVM assembly. I have also been thinking about stackvm-llvm transpiler, as well as compiling to JVM, Python virtual machine, Javascript or webassembly.

## Devices

Devices add "extra" functionality, such as stdio, file system, networking, and so on. Devices are *pluggable*, meaning that they might not be available on all platforms or configurations. This makes it extremely easy to sandbox applications by disabling some devices or even by using mock devices.

They are versioned separately from the core. A program can require specific version of a device.

## Dependencies

Python 3.6 or newer.


## Running programs

To compile StackVM assembly:

    ./compile.py sourcefile.sasm

And running a StackVM binary file:

    ./run.py sourcefile.svmb


## Known issue

* Unicode support is still only partial, and sometimes even incorrect


## License

This project is released under the MIT license. See [LICENSE](/LICENSE) for more information.
