# Additional Arguments

## callback

`--callback` is an optional argument which POSTs JSON data that has
the status of the test, at the end of the test to the given URL. The
URL should be a valid http(s) link that accepts POST data.

[See Callbacks Reference, for more details](../../callbacks.md)

## host

`host` is an optional argument which allows user to run the test on a different host Runner. Valid values are 'x86_64', 'x86_64_large', 'arm64_large'. 'x86_64' is the default value.

### x86_64 is 2vCPU + 4GB RAM with swap

### x86_64_large is 2vCPU + 8GB RAM with no swap

### arm64_large is 2vCPU + 8GB RAM with no swap

```
tuxsuite test --device qemu-armv7 --kernel https://storage.tuxboot.com/armv7/zImage --tests boot,ltp-smoke --host x86_64_large
```
