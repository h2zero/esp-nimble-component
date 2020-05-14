# esp-nimble-component
Updated esp-nimble fork to use as a separate ESP32 component in ESP-IDF v3.2 and v3.3.

# Purpose:
This repo is provided to allow ESP-IDF v3.2 & v3.3 users who also use Arduino   
easier access to, and a more update, NimBLE component.   

Arduino is **NOT** required to use this.   

# Why?
When using ESP-IDF v3.2 & v3.3 enabling NimBLE will disable bluedroid and when using   
Arduino as a component this results in compilation errors that require disabling many Arduino librarys.      
This repo solves that by using NimBLE as a component in the project folder. 

# Using:
Clone this into your `project/components` folder and run `menuconfig`.   
Configure settings in `main menu -> NimBLE Options`.   
   
**DO NOT** enable NimBLE in `Component config -> Bluetooth`.   
   
A CPP library is available [HERE](https://github.com/h2zero/esp-nimble-cpp) for use with NimBLE that is (mostly) compatible    
with the original cpp_utils and esp32-Arduino library.   
   
   
