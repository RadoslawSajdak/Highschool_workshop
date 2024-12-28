---
title: "Setting up VirtualBox"
date: 2024-12-28T16:41:57+01:00
draft: false
weight: 1
ShowToc: true
---

# Requirements
Because we wanted to provide low weight and similar environment for everyone we created a VirtualBox image. Before you download it, please install virtual box with version 7.1.14.
You can download it from the [virtualbox.org](https://www.virtualbox.org/wiki/Downloads)

Now you can download the VirtualBox image from https://ubuntu1224.hexu.pl

This image contains:
- Ubuntu 24.04
- Docker Compose
- Code
- JLink drivers
- nrfjprog tools
- VirtualBox extension pack
- Brave browser

To unzip the file, please ask for the password.

## Importing the image
TODO
- screnshots with step by step manual

## Attaching USB devices
TODO
- Screenshots how to attach USB device to the vm

## Using the environment
**If ANY image is not clear, you can click it with RB and use "Open image in new tab" :)**

Virtual Machine (VM) is set for an easy development. For making the code we'll use Code with a `dev containers` extension. It allows us to attach directly to the docker container and develop inside it. This solution is very flexible, because if you mess something you can just rebuild the container. Moreover you can quickly run exact the same container with a different setups and operating systems.

### VS Code
1. Open the VS Code
2. Choose Remote explorer extension. Make sure it's set to Dev Containers (it may be used for eg. ssh)
3. Select `zephyr_ble_lab` with right button and press "Attach in current window".
4. On the bottom you should see the container you are attached to.

You may want to use terminal which is in the middle of the screen. You can also open it from the menu on the top. In our container, terminal is in `sh`. Type `bash` to run more user friendly shell.
![first run of vscode](images/vscode_run.png#center)

If it's not opened, with file explorer (or File>Open Folder) open `hello_world` folder.

You should see the main development window.
1. It's file tree. It's usefull to navigate in your project
2. This is main window with `main.c` file opened. The project is imported from the zephyr codebase.
3. This is NRF Connect extension. We used `2023.11.3` version because the newest is not working good enough.
![VS Code view](images/vscode_main.png#center)

### NRF Connect for VS Code
First, please open the VS Code Extension. Side view will change. For this project we predefined build for `nRF52840DK` but you can change it pressing `Add build configuration`. For now it's not necessary.

In general, this extension will help us to build the examples and nothing else. For you it may be very helpfull if you want to explore different examples - it allows user to import the examples from SDK and helps with build configurations (samples are usually compatible with a few boards). On screen below we marked main 3 bookmarks:
1. Welcome - creating new samples from source
2. Applications - here you can define your builds
3. Actions - We will use `Build` and `Pristine Build` only. Other actions are helpful for more advanced development. However, nrfconnect for VS Code has the problems with handling USB while running inside the docker. That's why we'll flash from the outside.

In general, every action is just user-friendly button with `west` command below. You can read more about the west commands [here](https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html).
![NRF connect view](images/vscode_nrfconnect.png#center)

### Building and flashing
Let's build our first project to make sure everything is set up properly.

Please run `Pristine Build` based on the informations from the previous steps. On the right side you should see temporary terminal with no errors.

If you don't have **any** build configuration, please add one for `nrf52840DK/nrf52840` with all default.
![Build Hello World](images/vscode_build_hello_world.png#center)

In our example, folder PROJECTS is attached to the container so it's shared with the host. Please open terminal on the host, and go to `/home/devbox/Desktop/Codes/Zephyr_BLE_LAB/PROJECTS/hello_world` where you should see `build` directory. It's generated during the compilation. It contains entire setup and configuration of the project but for us, interesting file is `build/zephyr/zephyr.hex`. It's our compiled binary file.

To write it on development kit we will use `nrfjprog` tool from Nordic Semiconductor. It's outdated for a few weeks but is't more familiar to me. You can program the device with `nrfjprog --program build/zephyr/zephyr.hex --sectoranduicrerase --verify; nrfjprog -r`. If it doesn't find a USB device, please make sure it's attached to the VirtualBox.
![Flashing the device](images/vscode_flashing.png#center)

### Looking for the output
We have installed `cutecom` on our VM. You can use it to read serial output from the development kit. Default baudrate for serial output is set to `115200`.

Reset your board to see the output :)
![Serial output](images/vscode_cutecom.png#center)